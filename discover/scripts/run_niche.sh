#!/usr/bin/env bash
# run_niche.sh — оркестратор: проходит по аккаунтам/каналам ниши и собирает outlier-кандидатов.
#
# Использование:
#   run_niche.sh <niche_file> [period_days=30] [sample_n=30] [insta_pause=35]
#
# niche_file — путь к ~/.claude/skills/discover/niches/<niche>.md
#   Формат: одна сущность на строку:
#     insta:<username>             # @username Instagram
#     yt:<channel_url>             # YouTube канал/handle
#     yts:<channel_url>            # YouTube shorts (откроется /shorts)
#   Пустые строки и строки с # игнорируются.
#
# insta_pause — пауза между Insta-запросами (по умолчанию 35 сек), чтобы не словить rate-limit.
#
# Вывод — общий TSV-поток (на stdout), формат строк:
#   <platform>\t<source>\t<score>\t<metric>\t<median>\t<followers>\t<url>\t<date>\t<title>
# где platform = insta|yt|yts, metric = "likes" для Insta, "views" для YT, source = аккаунт/канал.
#
# Шапки `# username=...` из под-скриптов попадают в stderr.

set -u

NICHE_FILE="${1:-}"
DAYS="${2:-30}"
N="${3:-30}"
PAUSE="${4:-35}"

if [ -z "$NICHE_FILE" ] || [ ! -f "$NICHE_FILE" ]; then
  echo "USAGE: run_niche.sh <niche_file> [period_days=30] [sample_n=30] [insta_pause=35]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCAN_INSTA="$SCRIPT_DIR/scan_insta.sh"
SCAN_YT="$SCRIPT_DIR/scan_youtube.sh"

INSTA_FIRST=1

while IFS= read -r raw_line || [ -n "$raw_line" ]; do
  line="${raw_line%%#*}"
  line="$(echo "$line" | awk '{$1=$1;print}')"
  [ -z "$line" ] && continue

  case "$line" in
    insta:*)
      USERNAME="${line#insta:}"
      if [ "$INSTA_FIRST" -eq 0 ]; then
        echo "# sleeping ${PAUSE}s before next Insta to avoid rate-limit" >&2
        sleep "$PAUSE"
      fi
      INSTA_FIRST=0
      echo "# === insta:${USERNAME} ===" >&2
      bash "$SCAN_INSTA" "$USERNAME" "$DAYS" "$N" 2> >(sed "s/^/  /" >&2) | \
        awk -v u="$USERNAME" -F'\t' 'BEGIN{OFS="\t"} {
          if ($0 ~ /^#/) { print $0 > "/dev/stderr"; next }
          print "insta", u, $1, "likes", $3, $4, $5, $6, $7
        }'
      ;;
    yt:*|yts:*)
      KIND="${line%%:*}"
      CHURL="${line#*:}"
      if [ "$KIND" = "yts" ]; then
        case "$CHURL" in
          *"/shorts"*) : ;;
          *"/videos"*) CHURL="${CHURL%/videos}/shorts" ;;
          *)           CHURL="${CHURL%/}/shorts" ;;
        esac
      fi
      echo "# === ${KIND}:${CHURL} ===" >&2
      bash "$SCAN_YT" "$CHURL" "$DAYS" "$N" 2> >(sed "s/^/  /" >&2) | \
        awk -v k="$KIND" -v u="$CHURL" -F'\t' 'BEGIN{OFS="\t"} {
          if ($0 ~ /^#/) { print $0 > "/dev/stderr"; next }
          print k, u, $1, "views", $3, $4, $5, $6, $7
        }'
      ;;
    *)
      echo "# WARN unknown entry: $line" >&2
      ;;
  esac
done < "$NICHE_FILE"
