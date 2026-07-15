#!/usr/bin/env bash
# channel_baseline.sh — медиана просмотров последних N роликов канала.
# На вход: URL канала ИЛИ URL отдельного ролика (тогда сам вытащит channel_url).
# Использование: channel_baseline.sh <url> [N=20]
# Вывод (одна строка): <median_views>|<sample_size>|<platform>|<channel_url>
# Если не удалось — "?|0|<platform>|<url>".
#
# Поддержка платформ:
#   YouTube — через yt-dlp --flat-playlist (быстро, не качает)
#   TikTok  — через yt-dlp --flat-playlist (нужны куки Chrome)
#   Instagram — через yt-dlp tab=reels (best effort, может упасть — тогда "?")

URL="${1:-}"
N="${2:-20}"
if [ -z "$URL" ]; then
  echo "USAGE: channel_baseline.sh <url> [N=20]" >&2
  exit 2
fi

# Найти yt-dlp
YTDLP="$(command -v yt-dlp || true)"
if [ -z "$YTDLP" ]; then
  for cand in "$HOME/Library/Python/3.9/bin/yt-dlp" "$HOME/Library/Python/3.10/bin/yt-dlp" "$HOME/Library/Python/3.11/bin/yt-dlp" "$HOME/Library/Python/3.12/bin/yt-dlp" "/opt/homebrew/bin/yt-dlp"; do
    if [ -x "$cand" ]; then YTDLP="$cand"; break; fi
  done
fi
if [ -z "$YTDLP" ]; then
  echo "?|0|?|$URL" >&2
  exit 3
fi

# Платформа
case "$URL" in
  *youtube.com*|*youtu.be*) PLATFORM="YouTube" ;;
  *instagram.com*)          PLATFORM="Instagram" ;;
  *tiktok.com*)             PLATFORM="TikTok" ;;
  *)                        PLATFORM="other" ;;
esac

COOKIE_ARGS=()
if [ "$PLATFORM" = "Instagram" ] || [ "$PLATFORM" = "TikTok" ]; then
  COOKIE_ARGS=(--cookies-from-browser chrome)
fi

# Если на вход URL ролика — вытащим channel_url
CHANNEL_URL="$URL"
case "$URL" in
  *youtube.com/watch*|*youtu.be/*|*youtube.com/shorts/*|*tiktok.com/*/video/*|*tiktok.com/t/*|*instagram.com/reel/*|*instagram.com/p/*)
    CHANNEL_URL=$("$YTDLP" --skip-download --no-warnings --print "%(channel_url)s" \
      "${COOKIE_ARGS[@]}" "$URL" 2>/dev/null | head -1)
    if [ -z "$CHANNEL_URL" ] || [ "$CHANNEL_URL" = "NA" ]; then
      CHANNEL_URL="$URL"  # не удалось — попробуем как есть
    fi
    ;;
esac

# Для YouTube — добавим /videos если URL канала без раздела (для попадания на длинные)
CHANNEL_PROBE="$CHANNEL_URL"
case "$PLATFORM:$CHANNEL_URL" in
  YouTube:*"/@"*) [[ "$CHANNEL_URL" != *"/videos" && "$CHANNEL_URL" != *"/shorts" ]] && CHANNEL_PROBE="${CHANNEL_URL%/}/videos" ;;
esac

# Попытка 1: --flat-playlist (быстро, но для YouTube channel pages часто отдаёт NA)
VIEWS_RAW=$("$YTDLP" --skip-download --no-warnings --flat-playlist \
  --playlist-end "$N" --print "%(view_count)s" \
  "${COOKIE_ARGS[@]}" "$CHANNEL_PROBE" 2>/dev/null)

VIEWS=$(echo "$VIEWS_RAW" | awk '/^[0-9]+$/ && $1>0 {print $1}')

# Если ничего полезного не пришло — fallback БЕЗ flat-playlist (медленнее ~2с/ролик,
# но даёт реальные view_count для YouTube-каналов)
if [ -z "$VIEWS" ]; then
  VIEWS_RAW=$("$YTDLP" --skip-download --no-warnings \
    --playlist-end "$N" --print "%(view_count)s" \
    "${COOKIE_ARGS[@]}" "$CHANNEL_PROBE" 2>/dev/null)
  VIEWS=$(echo "$VIEWS_RAW" | awk '/^[0-9]+$/ && $1>0 {print $1}')
fi

if [ -z "$VIEWS" ]; then
  echo "?|0|$PLATFORM|$CHANNEL_URL"
  exit 1
fi

# Считаем медиану через awk
MEDIAN=$(echo "$VIEWS" | sort -n | awk '
  { a[NR]=$1 }
  END {
    if (NR==0) { print "?"; exit }
    if (NR%2==1) { print a[(NR+1)/2] }
    else { print int((a[NR/2]+a[NR/2+1])/2) }
  }
')
SIZE=$(echo "$VIEWS" | wc -l | tr -d ' ')

echo "$MEDIAN|$SIZE|$PLATFORM|$CHANNEL_URL"
