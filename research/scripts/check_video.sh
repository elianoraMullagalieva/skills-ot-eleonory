#!/usr/bin/env bash
# check_video.sh — берёт URL ролика, возвращает реальные метаданные через yt-dlp.
# Использование: check_video.sh <url>
# Вывод (одна строка, поля через |):
#   <view_count>|<title>|<uploader>|<duration_sec>|<upload_date>|<platform>|<followers>|<channel_url>
# Если что-то не удалось — поле "?".

URL="${1:-}"
if [ -z "$URL" ]; then
  echo "USAGE: check_video.sh <url>" >&2
  exit 2
fi

# Найти yt-dlp — он у Ули поставлен через pip --user или brew
YTDLP="$(command -v yt-dlp || true)"
if [ -z "$YTDLP" ]; then
  for cand in "$HOME/Library/Python/3.9/bin/yt-dlp" "$HOME/Library/Python/3.10/bin/yt-dlp" "$HOME/Library/Python/3.11/bin/yt-dlp" "$HOME/Library/Python/3.12/bin/yt-dlp" "/opt/homebrew/bin/yt-dlp"; do
    if [ -x "$cand" ]; then YTDLP="$cand"; break; fi
  done
fi

if [ -z "$YTDLP" ]; then
  echo "?|yt-dlp not installed|?|?|?|?|?|?" >&2
  exit 3
fi

# Платформа из URL
case "$URL" in
  *youtube.com*|*youtu.be*) PLATFORM="YouTube" ;;
  *instagram.com*)          PLATFORM="Instagram" ;;
  *tiktok.com*)             PLATFORM="TikTok" ;;
  *twitter.com*|*x.com*)    PLATFORM="Twitter/X" ;;
  *)                        PLATFORM="other" ;;
esac

# Для Instagram/TikTok нужны куки браузера (Chrome, как стоит у Ули)
COOKIE_ARGS=()
if [ "$PLATFORM" = "Instagram" ] || [ "$PLATFORM" = "TikTok" ]; then
  COOKIE_ARGS=(--cookies-from-browser chrome)
fi

# Запрос метаданных. Используем TAB как внутренний разделитель — title/uploader
# часто содержат символ `|`, поэтому через pipe split ломается.
META=$("$YTDLP" --skip-download --no-warnings \
  --print $'%(view_count)s\t%(title)s\t%(uploader)s\t%(duration)s\t%(upload_date)s\t%(channel_follower_count)s\t%(channel_url)s' \
  "${COOKIE_ARGS[@]}" "$URL" 2>/dev/null | head -1)

if [ -z "$META" ]; then
  echo "?|fetch failed|?|?|?|$PLATFORM|?|?"
  exit 1
fi

# yt-dlp подставляет "NA" если поле недоступно — заменим на "?",
# вставим платформу в нужную позицию и переведём разделитель TAB → "|" для вывода.
echo "$META" | awk -F'\t' -v p="$PLATFORM" 'BEGIN{OFS="|"} {
  for(i=1;i<=NF;i++) {
    if($i=="NA" || $i=="") $i="?";
    gsub(/\|/, "/", $i);  # на всякий случай — заменим оставшиеся | в значениях на /
  }
  # Порядок --print: 1=view 2=title 3=uploader 4=duration 5=date 6=followers 7=channel_url
  # Нужный вывод:    view|title|uploader|duration|date|PLATFORM|followers|channel_url
  print $1,$2,$3,$4,$5,p,$6,$7
}'
