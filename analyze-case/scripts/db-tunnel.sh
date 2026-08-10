#!/bin/bash
# SSH-туннель к прод-базе через bastion-хост prod.
# RDS живёт внутри VPC и снаружи не резолвится — только так.
#
# Обе системы на одном сервере, отличается только имя базы:
#   ePeople  = whereami_bb
#   Schedule = portal   (данные в схемах по тенантам: sfhcr, sfhcr2)
#
#   ./db-tunnel.sh up              — поднять туннель
#   ./db-tunnel.sh down            — закрыть
#   ./db-tunnel.sh psql            — psql к ePeople (whereami_bb)
#   ./db-tunnel.sh psql portal     — psql к Schedule
#   ./db-tunnel.sh q "SELECT 1"    — разовый запрос к ePeople
#   ./db-tunnel.sh q portal "SQL"  — разовый запрос к Schedule

set -euo pipefail

RDS=production-knowledgeloop-portal.cluster-ciygynwc56k0.us-west-2.rds.amazonaws.com
LOCAL_PORT=15433
DEFAULT_DB=whereami_bb
USER=kl_ro_user

export PATH="/opt/homebrew/opt/libpq/bin:$PATH"

ensure_up() {
  if ! lsof -nP -iTCP:$LOCAL_PORT -sTCP:LISTEN >/dev/null 2>&1; then
    ssh -o ExitOnForwardFailure=yes -f -N -L $LOCAL_PORT:$RDS:5432 prod
  fi
}

case "${1:-up}" in
  up)
    if lsof -nP -iTCP:$LOCAL_PORT -sTCP:LISTEN >/dev/null 2>&1; then
      echo "туннель уже поднят на localhost:$LOCAL_PORT"
    else
      ensure_up
      echo "туннель поднят: localhost:$LOCAL_PORT -> $RDS:5432"
    fi
    ;;
  down)
    pkill -f "ssh.*-L $LOCAL_PORT:$RDS" && echo "туннель закрыт" || echo "туннель не найден"
    ;;
  psql)
    ensure_up
    psql -h localhost -p $LOCAL_PORT -U $USER -d "${2:-$DEFAULT_DB}"
    ;;
  q)
    ensure_up
    if [ "${2:-}" = "portal" ] || [ "${2:-}" = "whereami_bb" ]; then
      db="$2"; shift 2
    else
      db="$DEFAULT_DB"; shift 1
    fi
    psql -h localhost -p $LOCAL_PORT -U $USER -d "$db" -c "$*"
    ;;
  *)
    echo "usage: $0 {up|down|psql [db]|q [db] \"SQL\"}" >&2
    exit 1
    ;;
esac
