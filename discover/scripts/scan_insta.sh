#!/usr/bin/env bash
# scan_insta.sh — листинг постов Instagram-аккаунта + outlier-фильтр по лайкам.
#
# Использование:
#   scan_insta.sh <username> [period_days=30] [sample_n=30]
#
# Шаги:
#   1) gallery-dl -j на /reels/ профиля (range 1-N)
#   2) дедуп по post_url, парсинг даты, лайков, описания
#   3) медиана лайков по всем N постам (стабильный baseline)
#   4) фильтр: посты за последние period_days
#   5) сортировка по outlier_score = likes / median
#
# Вывод — строки (одна на пост), разделитель TAB:
#   <outlier_score>\t<likes>\t<median>\t<followers>\t<post_url>\t<post_date>\t<description_short>
# Первая строка — заголовок-комментарий с метаданными аккаунта:
#   # username=<u> followers=<f> sample=<N> median=<m>
# Если что-то сломалось — пишем `# ERROR ...` в stderr и выходим с ненулевым кодом.

set -u

USERNAME="${1:-}"
DAYS="${2:-30}"
N="${3:-30}"

if [ -z "$USERNAME" ]; then
  echo "USAGE: scan_insta.sh <username> [period_days=30] [sample_n=30]" >&2
  exit 2
fi

GD="$(command -v gallery-dl || true)"
if [ -z "$GD" ]; then
  for cand in "$HOME/Library/Python/3.9/bin/gallery-dl" "$HOME/Library/Python/3.10/bin/gallery-dl" "$HOME/Library/Python/3.11/bin/gallery-dl" "$HOME/Library/Python/3.12/bin/gallery-dl" "/opt/homebrew/bin/gallery-dl"; do
    if [ -x "$cand" ]; then GD="$cand"; break; fi
  done
fi
if [ -z "$GD" ]; then
  echo "# ERROR gallery-dl not found" >&2
  exit 3
fi

URL="https://www.instagram.com/${USERNAME}/reels/"

RAW=$("$GD" --cookies-from-browser chrome --range "1-${N}" -j "$URL" 2>/dev/null)

if [ -z "$RAW" ]; then
  echo "# ERROR empty response for ${USERNAME} (rate-limit?)" >&2
  exit 1
fi

THUMB_DIR="$HOME/Documents/Reels-Research/digest/_thumbs"
mkdir -p "$THUMB_DIR"

echo "$RAW" | THUMB_DIR="$THUMB_DIR" python3 -c '
import json, sys, statistics, datetime, re, os, subprocess

DAYS = int(sys.argv[1])
USERNAME = sys.argv[2]
TAB = chr(9)
THUMB_DIR = os.environ.get("THUMB_DIR", "")

try:
    data = json.loads(sys.stdin.read())
except Exception as e:
    sys.stderr.write("# ERROR json parse failed: " + str(e) + "\n")
    sys.exit(1)

seen = {}
followers_raw = None

for entry in data:
    if not isinstance(entry, list) or len(entry) < 3:
        continue
    payload = entry[-1]
    if not isinstance(payload, dict):
        continue
    user = payload.get("user") or {}
    if isinstance(user, dict) and not followers_raw:
        followers_raw = user.get("search_social_context") or user.get("social_context")
    url = payload.get("post_url") or payload.get("url")
    if not url or url in seen:
        continue
    likes = payload.get("likes")
    date_str = payload.get("post_date") or payload.get("date")
    desc = (payload.get("description") or "").strip().replace("\n", " ").replace(TAB, " ")
    desc_short = desc[:120]
    thumb_url = payload.get("display_url") or ""
    if likes is None or date_str is None:
        continue
    try:
        post_dt = datetime.datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
    except Exception:
        continue
    seen[url] = {
        "url": url,
        "likes": int(likes),
        "date": post_dt,
        "desc": desc_short,
        "thumb_url": thumb_url,
    }

posts = list(seen.values())
if not posts:
    sys.stderr.write("# ERROR no posts parsed\n")
    sys.exit(1)

likes_all = [p["likes"] for p in posts]
median = int(statistics.median(likes_all)) if likes_all else 0
if median <= 0:
    median = 1

def parse_followers(s):
    if not s:
        return None
    m = re.match(r"([\d.,]+)\s*([KMB]?)\s*follower", s, re.I)
    if not m:
        return None
    num = float(m.group(1).replace(",", ""))
    mult = {"": 1, "K": 1000, "M": 1000000, "B": 1000000000}.get(m.group(2).upper(), 1)
    return int(num * mult)

followers = parse_followers(followers_raw) or 0

cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS)
in_period = [p for p in posts if p["date"] >= cutoff]

print("# username=" + USERNAME + " followers=" + str(followers) + " sample=" + str(len(posts)) + " median=" + str(median) + " in_period=" + str(len(in_period)))

in_period.sort(key=lambda p: p["likes"], reverse=True)

def post_id_from_url(u):
    m = re.search(r"/(?:reel|p|tv)/([\w\-]+)", u)
    return m.group(1) if m else ""

def fetch_thumb(post_id, thumb_url):
    if not (post_id and thumb_url and THUMB_DIR):
        return
    dst = os.path.join(THUMB_DIR, "insta-" + post_id + ".jpg")
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        return  # уже скачан
    try:
        subprocess.run(
            ["curl", "-sSL", "--max-time", "10", "-A", "Mozilla/5.0", "-o", dst, thumb_url],
            check=False, timeout=15
        )
        if os.path.exists(dst) and os.path.getsize(dst) < 1000:
            os.remove(dst)
    except Exception as e:
        sys.stderr.write("# WARN thumb fetch failed for " + post_id + ": " + str(e) + "\n")

# скачиваем превью только для топ-5 outlier постов в окне (чтобы не тянуть лишнего)
for p in in_period[:5]:
    pid = post_id_from_url(p["url"])
    fetch_thumb(pid, p["thumb_url"])

for p in in_period:
    score = round(p["likes"] / median, 2)
    date_iso = p["date"].strftime("%Y-%m-%d")
    fields = [str(score), str(p["likes"]), str(median), str(followers), p["url"], date_iso, p["desc"]]
    print(TAB.join(fields))
' "$DAYS" "$USERNAME"
