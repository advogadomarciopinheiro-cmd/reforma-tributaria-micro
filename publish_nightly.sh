#!/usr/bin/env bash
# Publica uma página nova no GitHub Pages, se o roteiro noturno tiver gerado mudança.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

export BASE_URL="${BASE_URL:-/reforma-tributaria-micro/}"
export SITE_URL="${SITE_URL:-https://advogadomarciopinheiro-cmd.github.io/reforma-tributaria-micro}"

REMOTE="${REMOTE:-origin}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"
PAGES_BRANCH="${PAGES_BRANCH:-gh-pages}"
WORKTREE="$ROOT/.gh-pages"
PUBLISH_LOG="$ROOT/data/processed/publish_log.jsonl"

log() { printf '%s\n' "$*"; }

ts_br() {
  python3 -c 'from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M") + " (horário de Brasília, UTC-3)")'
}

append_publish_log() {
  python3 - "$PUBLISH_LOG" "$1" <<'PY'
import json, sys
from datetime import datetime
from zoneinfo import ZoneInfo
path, payload = sys.argv[1], json.loads(sys.argv[2])
payload.setdefault(
    "quando",
    datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M") + " (horário de Brasília, UTC-3)",
)
with open(path, "a", encoding="utf-8") as fh:
    fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
PY
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "Erro: este diretório não é um repositório git."
  exit 1
fi

log "== roteiro noturno =="
python3 "$ROOT/nightly.py"

# Última entrada do log do nightly (página nova, se houver)
LAST_JSON="$(python3 - <<'PY'
import json
from pathlib import Path
p = Path("data/processed/nightly_log.jsonl")
if not p.exists():
    print("{}")
    raise SystemExit
lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
print(lines[-1] if lines else "{}")
PY
)"

NEW_HREF="$(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(d.get("href") or "")' "$LAST_JSON")"
NEW_TITLE="$(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(d.get("titulo") or "")' "$LAST_JSON")"
NEW_URL="${SITE_URL}/${NEW_HREF#/}"

log "Última página do roteiro: ${NEW_TITLE:-—}"
log "URL prevista: ${NEW_URL}"

# Reconstrói de novo (garante BASE_URL/SITE_URL mesmo se nightly.py já tiver gerado o site)
log "== rebuild com BASE_URL=${BASE_URL} =="
python3 "$ROOT/scripts/build.py"
touch "$ROOT/site/.nojekyll"

log "== commit em ${MAIN_BRANCH}, se houver mudança no código ou nos dados processados =="
git add -A -- \
  README.md \
  requirements.txt \
  .gitignore \
  nightly.py \
  publish_nightly.sh \
  scripts \
  data/processed
# data/processed/publish_log is appended later; that's fine on next run

MAIN_CHANGED=0
if ! git diff --cached --quiet; then
  MSG="Roteiro noturno: ${NEW_TITLE:-atualização do diretório}"
  git commit -m "$MSG"
  git push "$REMOTE" "$MAIN_BRANCH"
  MAIN_CHANGED=1
else
  log "Nada novo para commitar em ${MAIN_BRANCH}."
fi

log "== publicar site em ${PAGES_BRANCH} =="
ORIGIN_URL="$(git remote get-url "$REMOTE")"

publish_pages_branch() {
  if git show-ref --verify --quiet "refs/remotes/${REMOTE}/${PAGES_BRANCH}" || git ls-remote --heads "$REMOTE" "$PAGES_BRANCH" | grep -q "$PAGES_BRANCH"; then
    if git worktree list --porcelain | grep -q "^worktree ${WORKTREE}$"; then
      git -C "$WORKTREE" fetch "$REMOTE" "$PAGES_BRANCH" || true
      git -C "$WORKTREE" checkout "$PAGES_BRANCH"
      git -C "$WORKTREE" reset --hard "${REMOTE}/${PAGES_BRANCH}" || true
    else
      rm -rf "$WORKTREE"
      git fetch "$REMOTE" "$PAGES_BRANCH"
      git worktree add --force "$WORKTREE" "${REMOTE}/${PAGES_BRANCH}"
      git -C "$WORKTREE" checkout -B "$PAGES_BRANCH"
    fi
  else
    rm -rf "$WORKTREE"
    mkdir -p "$WORKTREE"
    git worktree add --detach "$WORKTREE"
    git -C "$WORKTREE" checkout --orphan "$PAGES_BRANCH"
    git -C "$WORKTREE" rm -rf . >/dev/null 2>&1 || true
  fi

  # Limpa o worktree (exceto .git) e copia o site gerado
  find "$WORKTREE" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp -a "$ROOT/site/." "$WORKTREE/"
  touch "$WORKTREE/.nojekyll"

  git -C "$WORKTREE" add -A
  if git -C "$WORKTREE" diff --cached --quiet; then
    log "Nenhuma mudança no site publicado."
    return 1
  fi
  git -C "$WORKTREE" commit -m "GitHub Pages: ${NEW_TITLE:-atualização do site}"
  git -C "$WORKTREE" push "$REMOTE" "HEAD:${PAGES_BRANCH}"
  return 0
}

PAGES_CHANGED=0
if publish_pages_branch; then
  PAGES_CHANGED=1
fi

append_publish_log "$(python3 -c 'import json,sys; print(json.dumps({"titulo":sys.argv[1],"url":sys.argv[2],"main_changed":sys.argv[3]=="1","pages_changed":sys.argv[4]=="1"}, ensure_ascii=False))' "${NEW_TITLE}" "${NEW_URL}" "${MAIN_CHANGED}" "${PAGES_CHANGED}")"

if [[ "$PAGES_CHANGED" -eq 1 || "$MAIN_CHANGED" -eq 1 ]]; then
  log "Publicado. Página nova: ${NEW_URL}"
else
  log "Nada foi enviado: o roteiro não gerou mudança pendente."
fi
