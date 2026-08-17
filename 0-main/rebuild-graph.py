#!/usr/bin/env python3
"""Пересобрать граф взаимосвязей скиллов.

Детерминированно и без обращений к модели: TF-IDF по описаниям скиллов,
косинусная близость как рёбра, Louvain для сообществ.

**Семантические рёбра сохраняются.** Прогон июля 2026 стоил 693К токенов на
субагентах и дал рёбрам типы (`complements`, `synergizes_with`) и уверенность.
Скрипт переносит те из них, у которых оба конца ещё существуют, и достраивает
статистикой только там, где семантического ребра нет. Провенанс у каждого ребра
проставлен, так что два слоя всегда различимы.

Формат вывода — networkx node_link_data (`nodes` / `links`), как и раньше:
то, что читает graph.json, продолжает работать.

Запуск из корня репозитория:  python3 0-main/rebuild-graph.py

Пишет в 0-main/: .skill_catalog.json, graph.json, GRAPH_REPORT.md, cost.json
"""
import json, math, re, sys, datetime, collections
from pathlib import Path

import numpy as np
import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "0-main"

# Параметры подобраны прогоном по сетке на 404 скиллах: этот набор даёт
# модулярность 0.62 при плотности ~3.9 ребра на узел (прошлый прогон — 3.1).
# Ниже 0.11 граф размывается, выше — рассыпается на изолированные узлы.
SIM_THRESHOLD = 0.11
MAX_EDGES_PER_NODE = 12
# Разрешение Louvain: ниже 1.0 укрупняет сообщества до навигабельного числа.
RESOLUTION = 0.8
# Сообщества мельче этого в отчёт не идут (в graph.json остаются).
THIN_COMMUNITY = 4

STOP = set("""a an the and or of to in for on with when use used using this that
it is are be as by from at into your you их или для the skill should when user
wants asks trigger phrases include also help helps create creating make making
run runs use uses used using need needs any all each per via more most other
than then them they what which who how why can could would should will not no
new one two three via etc eg ie about after before during over under
это как что для при или его их когда пользователь хочет просит нужно можно
также если чтобы после перед через между только уже ещё все всё был была быть""".split())


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    out = {}
    for key in ("name", "description"):
        km = re.search(rf"^{key}:\s*(.+?)\s*$", fm, re.M)
        if km:
            v = km.group(1).strip()
            if v.startswith(("'", '"')) and v.endswith(("'", '"')) and len(v) > 1:
                v = v[1:-1]
            out[key] = v
    return out or None


def collect():
    """Скиллы верхнего уровня репозитория — та же область, что и в прошлом прогоне."""
    skills = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in {"0-main", "agents"}:
            continue
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        try:
            fm = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        if not fm or not fm.get("description"):
            continue
        skills.append({
            "folder": d.name,
            "name": fm.get("name", d.name),
            "desc": fm["description"],
        })
    return skills


def tokenize(s):
    toks = re.findall(r"[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ\-]{2,}", s.lower())
    return [t for t in toks if t not in STOP and len(t) > 2]


def tfidf(docs):
    tokenized = [tokenize(d) for d in docs]
    df = collections.Counter()
    for toks in tokenized:
        df.update(set(toks))
    n = len(docs)
    kept = [t for t in sorted(df) if 1 < df[t] < n * 0.4]
    vocab = {t: i for i, t in enumerate(kept)}
    M = np.zeros((n, len(vocab)), dtype=np.float32)
    for i, toks in enumerate(tokenized):
        tf = collections.Counter(t for t in toks if t in vocab)
        for t, c in tf.items():
            M[i, vocab[t]] = (1 + math.log(c)) * math.log(n / df[t])
    norms = np.linalg.norm(M, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return M / norms, vocab


def carry_over_semantic(G, present):
    """Перенести семантические рёбра прошлого прогона, у которых оба конца живы."""
    path = OUT / "graph.json"
    if not path.is_file():
        return 0, 0
    try:
        old = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, 0
    kept = dropped = 0
    for link in old.get("links", []):
        a, b = link.get("source"), link.get("target")
        if not a or not b or a == b:
            continue
        if link.get("provenance") == "STATISTICAL":
            continue  # статистику пересчитываем заново, не наследуем
        if a in present and b in present:
            if not G.has_edge(a, b):
                G.add_edge(a, b,
                           relation=link.get("relation", "relates_to"),
                           provenance=link.get("provenance", "INFERRED"),
                           confidence=link.get("confidence"),
                           weight=float(link.get("confidence") or 0.5))
                kept += 1
        else:
            dropped += 1
    return kept, dropped


def build():
    skills = collect()
    if not skills:
        sys.exit("Скиллы не найдены — запускай из корня репозитория.")
    names = [s["folder"] for s in skills]
    present = set(names)
    desc_of = {s["folder"]: s["desc"] for s in skills}
    M, vocab = tfidf([f"{s['name']} {s['desc']}" for s in skills])
    S = M @ M.T
    np.fill_diagonal(S, 0.0)

    G = nx.Graph()
    for s in skills:
        G.add_node(s["folder"], label=s["folder"], name=s["name"], summary=s["desc"])

    semantic_kept, semantic_dropped = carry_over_semantic(G, present)

    stat_added = 0
    for i in range(len(names)):
        order = np.argsort(-S[i])[:MAX_EDGES_PER_NODE]
        for j in order:
            w = float(S[i, j])
            if w < SIM_THRESHOLD:
                break
            a, b = names[i], names[int(j)]
            if a != b and not G.has_edge(a, b):
                G.add_edge(a, b, relation="similar_to", provenance="STATISTICAL",
                           confidence=None, weight=round(w, 4))
                stat_added += 1

    communities = nx.community.louvain_communities(
        G, weight="weight", seed=42, resolution=RESOLUTION)
    communities = sorted(communities, key=len, reverse=True)

    inv_vocab = {i: t for t, i in vocab.items()}
    idx = {n: i for i, n in enumerate(names)}

    comm_of, labels, comm_info = {}, [], []
    for cid, members in enumerate(communities):
        for m in members:
            comm_of[m] = cid
        rows = [idx[m] for m in members]
        centroid = M[rows].mean(axis=0)
        top = [inv_vocab[i] for i in np.argsort(-centroid)[:4] if centroid[i] > 0]
        label = " / ".join(t.capitalize() for t in top) or f"Cluster {cid}"
        labels.append(label)
        sub = G.subgraph(members)
        possible = len(members) * (len(members) - 1) / 2
        comm_info.append({
            "id": cid,
            "label": label,
            "size": len(members),
            "cohesion": round(sub.number_of_edges() / possible, 3) if possible else 0.0,
            "nodes": sorted(members),
        })

    deg = dict(G.degree())
    btw = nx.betweenness_centrality(G, weight=None)
    isolated = sorted(n for n in G if deg[n] <= 1)

    # networkx node_link_data — тот же формат, что и у прошлого графа,
    # чтобы всё, что читает graph.json, продолжало работать.
    graph = {
        "directed": False,
        "multigraph": False,
        "graph": {
            "generated": datetime.datetime.now(datetime.UTC).isoformat(),
            "method": "semantic edges carried over + tfidf-cosine fill + louvain",
            "params": {"sim_threshold": SIM_THRESHOLD,
                       "max_edges_per_node": MAX_EDGES_PER_NODE,
                       "resolution": RESOLUTION},
            "counts": {"nodes": G.number_of_nodes(), "links": G.number_of_edges(),
                       "communities": len(communities),
                       "semantic_kept": semantic_kept,
                       "semantic_dropped_dead_endpoint": semantic_dropped,
                       "statistical_added": stat_added},
            "communities": comm_info,
        },
        "nodes": [{"id": n, "label": n, "name": G.nodes[n]["name"],
                   "summary": G.nodes[n]["summary"], "community": comm_of[n],
                   "community_label": labels[comm_of[n]],
                   "degree": deg[n], "betweenness": round(btw[n], 4)}
                  for n in sorted(G)],
        "links": [{"source": a, "target": b,
                   "relation": d.get("relation", "similar_to"),
                   "provenance": d.get("provenance", "STATISTICAL"),
                   "confidence": d.get("confidence"),
                   "weight": d["weight"]}
                  for a, b, d in sorted(G.edges(data=True))],
        "hyperedges": [],
    }
    return (skills, G, graph, comm_info, deg, btw, isolated, labels, comm_of,
            semantic_kept, semantic_dropped, stat_added)


def report(skills, G, graph, comm_info, deg, btw, isolated):
    today = datetime.date.today().isoformat()
    top_deg = sorted(deg.items(), key=lambda kv: -kv[1])[:10]
    top_btw = sorted(btw.items(), key=lambda kv: -kv[1])[:5]
    L = []
    A = L.append
    A(f"# Graph Report — skill relationships ({today})\n")
    A("## Summary")
    c = graph["graph"]["counts"]
    A(f"- {c['nodes']} nodes · {c['links']} edges · {c['communities']} communities")
    A(f"- Edges: {c['semantic_kept']} semantic (carried over from the July run), "
      f"{c['statistical_added']} statistical (TF-IDF cosine)")
    A(f"- {c['semantic_dropped_dead_endpoint']} semantic edges dropped — one endpoint "
      "no longer exists")
    A("- Token cost of this run: 0 — rebuild with `python3 0-main/rebuild-graph.py`\n")
    substantive = [ci for ci in comm_info if ci["size"] >= THIN_COMMUNITY]
    thin = len(comm_info) - len(substantive)
    A(f"## Communities ({len(substantive)} substantive, {thin} thin omitted)\n")
    for ci in substantive:
        shown = ", ".join(ci["nodes"][:8])
        extra = f" (+{ci['size'] - 8} more)" if ci["size"] > 8 else ""
        A(f"### {ci['id']} — {ci['label']}")
        A(f"Size {ci['size']} · cohesion {ci['cohesion']}")
        A(f"Nodes: {shown}{extra}\n")
    A("## God nodes (most connected)\n")
    for i, (n, d) in enumerate(top_deg, 1):
        A(f"{i}. `{n}` — {d} edges")
    A("\n## Bridges (highest betweenness — cross-community connectors)\n")
    for n, b in top_btw:
        A(f"- `{n}` — {b:.4f}")
    A("\n## Knowledge gaps\n")
    if isolated:
        A(f"**{len(isolated)} weakly-connected node(s)** (≤1 edge): "
          + ", ".join(f"`{n}`" for n in isolated[:25])
          + (" …" if len(isolated) > 25 else ""))
        A("\nA skill with no neighbours is either genuinely unique or described in words "
          "nothing else uses — check the description before assuming it is the former.")
    else:
        A("None — every skill has at least two neighbours.")
    return "\n".join(L) + "\n"


# Tableau 10 — как в прошлой версии графа; при >10 сообществ цвета повторяются.
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
           "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]


def html_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))


def write_html(G, graph, comm_info, deg, comm_of, labels):
    """Залить актуальные данные в graph-template.html.

    Шаблон хранит всю разметку и логику (поиск, панель узла, соседи, легенда);
    здесь подменяются только данные. Так правка визуала живёт в одном месте.
    """
    tpl_path = OUT / "graph-template.html"
    if not tpl_path.is_file():
        print("graph-template.html не найден — HTML пропущен", file=sys.stderr)
        return False

    nodes = []
    for n in sorted(G):
        d = deg[n]
        size = round(min(10.0 + 1.15 * d, 40.0), 1)
        cid = comm_of[n]
        nodes.append({
            "id": n, "label": n,
            "color": {"background": PALETTE[cid % len(PALETTE)],
                      "border": PALETTE[cid % len(PALETTE)],
                      "highlight": {"background": "#ffffff",
                                    "border": PALETTE[cid % len(PALETTE)]}},
            "size": size,
            # мелкие узлы без подписи — иначе центр графа нечитаем
            "font": {"size": 12 if d >= 4 else 0, "color": "#ffffff"},
            "title": f"{n} — {G.nodes[n]['summary'][:160]}",
            "community": cid, "community_name": labels[cid],
            "source_file": f"{n}/SKILL.md", "file_type": "concept",
            "degree": d,
        })

    edges = []
    for a, b, d in sorted(G.edges(data=True)):
        stat = d.get("provenance") == "STATISTICAL"
        conf = d.get("confidence")
        edges.append({
            "from": a, "to": b,
            "label": d.get("relation", "similar_to"),
            "title": (f"{d.get('relation')} [{d['weight']:.2f}]" if stat
                      else f"{d.get('relation')} [{conf}] · {d.get('provenance')}"),
            # пунктир и приглушение — статистический слой; сплошные — семантика
            "dashes": stat,
            "width": 1,
            "color": {"opacity": 0.20 if stat else 0.45},
            "confidence": conf if conf is not None else round(d["weight"], 3),
        })

    sizes = collections.Counter(comm_of.values())
    legend = [{"cid": ci["id"], "color": PALETTE[ci["id"] % len(PALETTE)],
               "label": html_escape(ci["label"]), "count": sizes[ci["id"]]}
              for ci in comm_info]

    c = graph["graph"]["counts"]
    stats = (f"{c['nodes']} nodes &middot; {c['links']} edges &middot; "
             f"{c['communities']} communities &middot; "
             f"{c['semantic_kept']} semantic / {c['statistical_added']} statistical")

    out = tpl_path.read_text(encoding="utf-8")
    for token, value in (
        ("__RAW_NODES__", json.dumps(nodes, ensure_ascii=False)),
        ("__RAW_EDGES__", json.dumps(edges, ensure_ascii=False)),
        ("__LEGEND__", json.dumps(legend, ensure_ascii=False)),
        ("__STATS__", stats),
        ("__TITLE__", f"skill graph — {c['nodes']} skills"),
    ):
        if token not in out:
            print(f"плейсхолдер {token} отсутствует в шаблоне", file=sys.stderr)
            return False
        out = out.replace(token, value, 1)

    (OUT / "graph.html").write_text(out, encoding="utf-8")
    return True


def main():
    (skills, G, graph, comm_info, deg, btw, isolated, labels, comm_of,
     semantic_kept, semantic_dropped, stat_added) = build()

    (OUT / ".skill_catalog.json").write_text(
        json.dumps(skills, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / ".graphify_labels.json").write_text(
        json.dumps({str(i): l for i, l in enumerate(labels)}, ensure_ascii=False),
        encoding="utf-8")
    (OUT / "GRAPH_REPORT.md").write_text(
        report(skills, G, graph, comm_info, deg, btw, isolated), encoding="utf-8")

    cost_path = OUT / "cost.json"
    cost = json.loads(cost_path.read_text()) if cost_path.is_file() else {"runs": []}
    cost["runs"].append({
        "date": datetime.datetime.now(datetime.UTC).isoformat(),
        "input_tokens": 0, "output_tokens": 0, "subagent_tokens": 0,
        "files": len(skills),
        "note": "deterministic rebuild: tfidf-cosine + louvain, no model calls",
    })
    cost["total_subagent_tokens"] = sum(r.get("subagent_tokens", 0) for r in cost["runs"])
    cost_path.write_text(json.dumps(cost, ensure_ascii=False, indent=2), encoding="utf-8")

    html_ok = write_html(G, graph, comm_info, deg, comm_of, labels)

    c = graph["graph"]["counts"]
    print(f"{c['nodes']} nodes · {c['links']} edges · {c['communities']} communities")
    print(f"  semantic kept: {semantic_kept}  (dropped, dead endpoint: {semantic_dropped})")
    print(f"  statistical added: {stat_added}")
    print(f"  weakly connected: {len(isolated)}")
    print(f"  graph.html: {'updated' if html_ok else 'SKIPPED'}")


if __name__ == "__main__":
    main()
