#!/usr/bin/env bash
# scan_youtube.sh — листинг последних видео YouTube-канала + outlier-фильтр.
#
# Использование:
#   scan_youtube.sh <channel_url> [period_days=30] [sample_n=30]
#
# channel_url — это либо
#   https://www.youtube.com/@handle
#   https://www.youtube.com/channel/UCxxx
#   https://www.youtube.com/@handle/videos
#   https://www.youtube.com/@handle/shorts
#
# Шаги:
#   1) yt-dlp --flat-playlist (если NA — fallback на полный режим)
#   2) для каждого id вытаскиваем view_count + upload_date + title + duration
#   3) медиана просмотров по sample_n постам
#   4) фильтр: даты за последние period_days
#   5) сортировка по outlier_score
#
# Вывод — TAB-разделённые строки:
#   <outlier_score>\t<views>\t<median>\t<followers>\t<video_url>\t<upload_date>\t<title_short>
# Шапка:
#   # channel=<url> subs=<f> sample=<N> median=<m> in_period=<k>

set -u

CHANNEL="${1:-}"
DAYS="${2:-30}"
N="${3:-30}"

if [ -z "$CHANNEL" ]; then
  echo "USAGE: scan_youtube.sh <channel_url> [period_days=30] [sample_n=30]" >&2
  exit 2
fi

YTDLP="$(command -v yt-dlp || true)"
if [ -z "$YTDLP" ]; then
  for cand in "$HOME/Library/Python/3.9/bin/yt-dlp" "$HOME/Library/Python/3.10/bin/yt-dlp" "$HOME/Library/Python/3.11/bin/yt-dlp" "$HOME/Library/Python/3.12/bin/yt-dlp" "/opt/homebrew/bin/yt-dlp"; do
    if [ -x "$cand" ]; then YTDLP="$cand"; break; fi
  done
fi
if [ -z "$YTDLP" ]; then
  echo "# ERROR yt-dlp not found" >&2
  exit 3
fi

# Если URL канала «голый» (без /videos), добавим /videos
PROBE="$CHANNEL"
case "$CHANNEL" in
  *"/@"*|*"/channel/"*|*"/user/"*|*"/c/"*)
    if [[ "$CHANNEL" != *"/videos" && "$CHANNEL" != *"/shorts" && "$CHANNEL" != *"/streams" && "$CHANNEL" != *"/playlists" ]]; then
      PROBE="${CHANNEL%/}/videos"
    fi
    ;;
esac

# 1-я попытка — flat-playlist (быстро). На многих каналах view_count = NA, тогда fallback.
ERR_TMP=$(mktemp)
RAW=$("$YTDLP" --skip-download --no-warnings --flat-playlist \
  --playlist-end "$N" \
  --print $'%(id)s\t%(view_count)s\t%(upload_date)s\t%(title)s\t%(duration)s\t%(channel_follower_count)s' \
  "$PROBE" 2>"$ERR_TMP")

HAVE_VIEWS=$(echo "$RAW" | awk -F'\t' '$2 ~ /^[0-9]+$/ {c++} END{print c+0}')

if [ "$HAVE_VIEWS" -lt 3 ]; then
  # Fallback — без --flat-playlist (медленно: ~2 сек на видео × N)
  RAW=$("$YTDLP" --skip-download --no-warnings \
    --playlist-end "$N" \
    --print $'%(id)s\t%(view_count)s\t%(upload_date)s\t%(title)s\t%(duration)s\t%(channel_follower_count)s' \
    "$PROBE" 2>"$ERR_TMP")
fi

if [ -z "$RAW" ]; then
  # Разбираем причину из stderr yt-dlp
  ERR_LINE=$(head -1 "$ERR_TMP" 2>/dev/null | tr -d '\n')
  rm -f "$ERR_TMP"
  case "$ERR_LINE" in
    *"404"*)
      echo "# ERROR handle устарел (404) для ${CHANNEL}" >&2 ;;
    *"does not have a videos tab"*)
      echo "# ERROR у канала нет вкладки Videos: ${CHANNEL}" >&2 ;;
    *"Private"*|*"private"*)
      echo "# ERROR приватный канал: ${CHANNEL}" >&2 ;;
    *)
      echo "# ERROR empty response for ${CHANNEL}" >&2 ;;
  esac
  exit 1
fi
rm -f "$ERR_TMP"

echo "$RAW" | python3 -c '
import sys, statistics, datetime

DAYS = int(sys.argv[1])
CHANNEL = sys.argv[2]
TAB = chr(9)

rows = []
subs = 0

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    parts = line.split(TAB)
    if len(parts) < 6:
        continue
    vid_id, views_s, date_s, title, dur_s, subs_s = parts[:6]
    if not views_s or views_s in ("NA", "?"):
        continue
    try:
        views = int(views_s)
    except ValueError:
        continue
    if not date_s or date_s == "NA":
        continue
    try:
        dt = datetime.datetime.strptime(date_s[:8], "%Y%m%d")
    except ValueError:
        continue
    if subs_s and subs_s not in ("NA", "?") and not subs:
        try:
            subs = int(subs_s)
        except ValueError:
            pass
    try:
        dur = int(float(dur_s)) if dur_s and dur_s != "NA" else 0
    except ValueError:
        dur = 0
    is_short = (dur and dur <= 60) or "/shorts/" in CHANNEL
    path = "shorts/" if is_short else "watch?v="
    url = "https://www.youtube.com/" + path + vid_id
    rows.append({
        "views": views,
        "date": dt,
        "title": title.replace(TAB, " ")[:120],
        "url": url,
    })

if not rows:
    sys.stderr.write("# ERROR no parsable rows\n")
    sys.exit(1)

views_all = [r["views"] for r in rows]
median = int(statistics.median(views_all)) if views_all else 0
if median <= 0:
    median = 1

cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS)
in_period = [r for r in rows if r["date"] >= cutoff]

print("# channel=" + CHANNEL + " subs=" + str(subs) + " sample=" + str(len(rows)) + " median=" + str(median) + " in_period=" + str(len(in_period)))

in_period.sort(key=lambda r: r["views"], reverse=True)
for r in in_period:
    score = round(r["views"] / median, 2)
    date_iso = r["date"].strftime("%Y-%m-%d")
    fields = [str(score), str(r["views"]), str(median), str(subs), r["url"], date_iso, r["title"]]
    print(TAB.join(fields))
' "$DAYS" "$CHANNEL"
