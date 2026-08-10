# States in Vue

Read before phase 1. This project's web app is Vue 3 + ant-design-vue.

## Find the existing convention first

| Look for | Tells you |
|---|---|
| `data()` returning `loading`, `error` flags | flag-based state, the common case |
| Vuex/Pinia module state shape | whether state is centralised or per-component |
| `try/catch` versus `.then().catch()` around the store dispatch | where failures are caught |
| `notification.error` / `message.error` calls | failures surface as toasts, not screen states |

Follow what is there. Introducing a state machine into a codebase built on boolean flags
makes the blueprint unimplementable.

## The flag trap

Two booleans give four combinations, three of which are meaningless and one of which is
unreachable:

```js
data() { return { loading: false, error: null, items: [] } }
```

`loading && error` — undefined. `!loading && !error && items.length === 0` — is that
empty, or never-loaded? The blueprint must say which combination renders which state,
because the code cannot.

State this explicitly in the blueprint's States section, one line per combination the
screen can actually reach.

## ant-design-vue defaults are unanswered states

| Component | Silent default | Consequence |
|---|---|---|
| `a-table`, `a-list` | `No Data` | all three empty states collapse into one |
| `a-table :loading` | spinner overlay | no skeleton, layout jumps |
| `a-modal` | `OK` / `Cancel` | confirmation buttons name no action |
| `a-empty` | default illustration and text | generic where specific was needed |

A screen using these without overrides has not answered its empty state — it has
inherited one. The blueprint names the override for each.

## Offline

`internet-connection-alert.vue` exists in this repository's components. A screen that
loads remote data and does not use it has no offline state. Check for the import; its
absence is a finding, not a detail.

## Permission

`permission-provider.vue` and the `no-permissions.vue` view exist. A screen with
role-dependent data that references neither has no no-access state — it will render an
empty table to a user who simply lacks the right.

## Placement

`src/router` defines routes and guards. The blueprint's Placement section names: the
route path, the guard that protects it, the parent in `recursive-menu`, and where the
back path leads.
