#!/usr/bin/env bash
# digest_all.sh — еженедельный сканер всех ниш.
#
# Обходит все ~/.claude/skills/discover/niches/*.md (кроме пустых/закомментированных),
# для каждой запускает run_niche.sh, собирает stdout/stderr в _data/<DATE>/.
# В конце вызывает render_digest.py чтобы собрать общий HTML.
#
# Использование:
#   digest_all.sh [period_days=7] [sample_n=30] [insta_pause=35]
#
# Артефакты:
#   ~/Documents/Reels-Research/digest/_data/<DATE>/<niche>.tsv  — outlier-строки
#   ~/Documents/Reels-Research/digest/_data/<DATE>/<niche>.log  — шапки + ошибки
#   ~/Documents/Reels-Research/digest/<DATE>.html               — финальный отчёт
#   ~/Documents/Reels-Research/digest/_logs/<DATE>.log          — общий лог запуска

set -u

DAYS="${1:-7}"
N="${2:-30}"
PAUSE="${3:-35}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NICHES_DIR="${SCRIPT_DIR%/scripts}/niches"
RUN_NICHE="$SCRIPT_DIR/run_niche.sh"
RENDER="$SCRIPT_DIR/render_digest.py"

DIGEST_ROOT="$HOME/Documents/Reels-Research/digest"
DATE="$(date +%Y-%m-%d)"
DATA_DIR="$DIGEST_ROOT/_data/$DATE"
LOG_FILE="$DIGEST_ROOT/_logs/$DATE.log"
HTML_OUT="$DIGEST_ROOT/$DATE.html"

mkdir -p "$DATA_DIR" "$DIGEST_ROOT/_logs"

# PATH для launchd-окружения (gallery-dl и yt-dlp могут быть в ~/Library/Python/...)
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/Library/Python/3.9/bin:$HOME/Library/Python/3.11/bin:$PATH"

log() {
  echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"
}

log "=== digest_all start · period=${DAYS}d · sample=${N} · pause=${PAUSE}s ==="

NICHE_COUNT=0
SKIPPED_COUNT=0
PROCESSED_LIST=()

for nf in "$NICHES_DIR"/*.md; do
  [ -f "$nf" ] || continue
  base="$(basename "$nf" .md)"

  # Сколько живых строк (insta:/yt:/yts:) в файле?
  live=$(grep -E '^[[:space:]]*(insta|yt|yts):' "$nf" | wc -l | tr -d ' ')
  if [ "$live" -lt 1 ]; then
    log "skip $base — пустой niche-файл"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    continue
  fi

  NICHE_COUNT=$((NICHE_COUNT + 1))
  PROCESSED_LIST+=("$base")
  log "→ $base (${live} источников)"

  out_tsv="$DATA_DIR/$base.tsv"
  out_log="$DATA_DIR/$base.log"

  # run_niche.sh → stdout в tsv, stderr в log (с шапками)
  bash "$RUN_NICHE" "$nf" "$DAYS" "$N" "$PAUSE" >"$out_tsv" 2>"$out_log" || \
    log "  ⚠ $base — run_niche вернул ненулевой код, см. $out_log"

  rows=$(wc -l <"$out_tsv" | tr -d ' ')
  log "  ← $base: $rows строк сырых"
done

log "=== собрано $NICHE_COUNT ниш (пропущено пустых: $SKIPPED_COUNT) ==="

if [ "$NICHE_COUNT" -eq 0 ]; then
  log "Нет ни одной заполненной ниши — выхожу без HTML"
  exit 0
fi

# Рендер HTML
log "→ render_digest.py → $HTML_OUT"
if python3 "$RENDER" "$DATA_DIR" "$HTML_OUT" "$DAYS" >>"$LOG_FILE" 2>&1; then
  log "✓ HTML готов: $HTML_OUT"
else
  log "✗ render_digest.py упал, см. лог"
  exit 4
fi

# Открытие в Chrome (выбрано Улей вместо нотификаций 2026-05-21 — надёжнее)
if [ -z "${LAUNCHD_RUN:-}" ] || [ "${DIGEST_OPEN_BROWSER:-1}" = "1" ]; then
  log "→ открываю $HTML_OUT в Chrome"
  if open -a "Google Chrome" "$HTML_OUT" 2>>"$LOG_FILE"; then
    log "  ✓ Chrome получил команду открыть"
  else
    log "  ✗ open -a Chrome вернул ошибку"
  fi
fi

log "=== digest_all done ==="
