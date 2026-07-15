#!/usr/bin/env python3
# render_digest.py — превращает _data/<DATE>/*.tsv + *.log в один HTML-отчёт.
#
# Аргументы:
#   sys.argv[1]  data_dir   путь к _data/<DATE>/
#   sys.argv[2]  html_out   куда положить итоговый HTML
#   sys.argv[3]  days       период (для шапки)

import os
import re
import sys
import html
import glob
import datetime
from collections import defaultdict

DATA_DIR = sys.argv[1]
HTML_OUT = sys.argv[2]
DAYS = int(sys.argv[3]) if len(sys.argv) > 3 else 7

NICHE_LABELS = {
    # Опциональный словарь "slug → красивое название" для шапки секции.
    # Если ниша отсутствует в словаре — берётся сам slug.
    # Пример:
    # "nalogi": "Налоги и бухгалтерия",
    # "yur-biznes": "Юристы для бизнеса",
}

SCORE_THRESHOLD = 3.0
TOP_PER_NICHE = 15
MAX_PER_AUTHOR = 3


def parse_log(log_path):
    """Парсит run_niche.sh → (meta-dict, sources-list).

    meta:    {key → {sample, median, followers, in_period}}  только живые
    sources: [{spec, key, status}]  все объявленные в niche-файле, по порядку
             status: "ok" | "silent" (живой, но in_period=0) | "error" (упал)
    """
    meta = {}
    sources = []
    if not os.path.exists(log_path):
        return meta, sources

    current_spec = None  # последняя `# === <prefix>:<value> ===` шапка
    current_key = None   # username/channel из следующей за ней строки
    current_status = None
    current_error = None

    def flush():
        if current_spec is None:
            return
        key = current_key or current_spec.split(":", 1)[-1]
        status = current_status or "error"
        sources.append({
            "spec": current_spec,
            "key": key,
            "status": status,
            "error": current_error,
        })

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            if not line.startswith("#"):
                continue

            m_head = re.match(r"#\s*===\s*(\S+)\s*===\s*$", line)
            if m_head:
                flush()
                current_spec = m_head.group(1)
                current_key = None
                current_status = None
                current_error = None
                continue

            m_user = re.search(r"username=(\S+)", line)
            m_chan = re.search(r"channel=(\S+)", line)
            key = None
            if m_user:
                key = m_user.group(1)
            elif m_chan:
                key = m_chan.group(1)

            if key:
                m_period = re.search(r"in_period=(\d+)", line)
                in_period = int(m_period.group(1)) if m_period else 0
                row = {"sample": 0, "median": 0, "followers": 0, "in_period": in_period}
                for field in ("sample", "median", "followers", "subs"):
                    m = re.search(rf"{field}=(\d+)", line)
                    if m:
                        val = int(m.group(1))
                        if field == "subs":
                            row["followers"] = val
                        else:
                            row[field] = val
                meta[key] = row
                current_key = key
                current_status = "ok" if in_period > 0 else "silent"
                continue

            m_err = re.search(r"ERROR\s+(.*)$", line)
            if m_err:
                current_status = "error"
                current_error = m_err.group(1).strip()

    flush()
    return meta, sources


def parse_tsv(tsv_path):
    """Каждая строка run_niche → словарь."""
    rows = []
    if not os.path.exists(tsv_path):
        return rows
    with open(tsv_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 9:
                continue
            platform, source, score_s, metric, median_s, followers_s, url, date_s, title = parts[:9]
            try:
                score = float(score_s)
            except ValueError:
                continue
            if score < SCORE_THRESHOLD:
                continue
            try:
                metric_val = 0
                # metric_val хранит само число лайков/просмотров — у нас его нет напрямую,
                # но score = likes/median → likes = score * median
                median_int = int(median_s) if median_s.isdigit() else 0
                metric_val = int(round(score * median_int)) if median_int else 0
            except Exception:
                metric_val = 0
            rows.append({
                "platform": platform,
                "source": source,
                "score": score,
                "metric_name": metric,
                "metric_val": metric_val,
                "median": int(median_s) if median_s.isdigit() else 0,
                "followers": int(followers_s) if followers_s.isdigit() else 0,
                "url": url,
                "date": date_s,
                "title": title,
            })
    return rows


def stars(score):
    if score >= 10:
        return "⭐⭐⭐⭐⭐"
    if score >= 5:
        return "⭐⭐⭐⭐"
    return "⭐⭐⭐"


def star_class(score, median):
    # Small-base ловушка: median<100 → не выше ⭐⭐⭐
    if median < 100:
        return "lvl3"
    if score >= 10:
        return "lvl5"
    if score >= 5:
        return "lvl4"
    return "lvl3"


THUMBS_DIR = os.path.expanduser("~/Documents/Reels-Research/digest/_thumbs")
# HTML лежит в digest/, превью в digest/_thumbs/ — путь относительный
THUMBS_REL = "_thumbs"


def thumbnail_for(row):
    """YouTube → hqdefault. Insta → локальный путь если файл скачан, иначе None."""
    url = row["url"]
    m = re.search(r"youtube\.com/(?:watch\?v=|shorts/)([\w\-]+)", url)
    if m:
        vid = m.group(1)
        return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    m = re.search(r"instagram\.com/(?:reel|p|tv)/([\w\-]+)", url)
    if m:
        pid = m.group(1)
        local_path = os.path.join(THUMBS_DIR, f"insta-{pid}.jpg")
        if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            return f"{THUMBS_REL}/insta-{pid}.jpg"
    return None


def short_source(source):
    """@handle для YouTube URL → просто @handle, иначе оставить."""
    m = re.search(r"@([\w\-\.]+)", source)
    if m:
        return "@" + m.group(1)
    if source.startswith("http"):
        return source.split("/")[-1] or source
    return source


def fmt_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def dedup_and_balance(rows):
    """Дедуп по URL → balanced top по автору."""
    seen = set()
    uniq = []
    for r in rows:
        if r["url"] in seen:
            continue
        seen.add(r["url"])
        uniq.append(r)
    uniq.sort(key=lambda r: r["score"], reverse=True)

    by_author = defaultdict(int)
    balanced = []
    overflow = []
    for r in uniq:
        if by_author[r["source"]] < MAX_PER_AUTHOR:
            balanced.append(r)
            by_author[r["source"]] += 1
        else:
            overflow.append(r)
        if len(balanced) >= TOP_PER_NICHE:
            break

    return balanced


def render_niche(niche_key, rows, meta, sources):
    label = NICHE_LABELS.get(niche_key, niche_key)
    n_sources = len(sources) if sources else len(meta)
    total_in_period = sum(m.get("in_period", 0) for m in meta.values())
    total_outliers = len(rows)

    silent = [s for s in sources if s["status"] == "silent"]
    errored = [s for s in sources if s["status"] == "error"]
    dead_html = ""
    if silent or errored:
        chips = []
        for s in silent:
            name = html.escape(short_source(s["key"]).lstrip("@"))
            chips.append(f'<span class="dead-chip silent">@{name}</span>')
        for s in errored:
            name = html.escape(short_source(s["key"]).lstrip("@"))
            err_short = html.escape((s.get("error") or "недоступен")[:40])
            chips.append(f'<span class="dead-chip errored" title="{err_short}">@{name} ✗</span>')
        n_dead = len(silent) + len(errored)
        dead_html = f"""
  <div class="dead-row">
    <span class="dead-label">{n_dead} из {n_sources} молчат за {DAYS}д:</span>
    {' '.join(chips)}
  </div>"""

    if not rows:
        return f"""
<section class="niche empty">
  <header class="niche-head">
    <h2>{html.escape(label)}</h2>
    <div class="niche-stats">{n_sources} источников · {total_in_period} постов за период · <strong>0 outlier'ов</strong></div>
  </header>{dead_html}
  <div class="empty-note">За {DAYS} дней в этой нише никто не выбился сильно из своего ряда. Это нормально — можно расширить период или добавить аккаунты.</div>
</section>"""

    balanced = dedup_and_balance(rows)

    cards_html = []
    for i, r in enumerate(balanced, 1):
        title_safe = html.escape(r["title"]) if r["title"] else "(без описания)"
        url = html.escape(r["url"])
        plat_label = {"insta": "Instagram", "yt": "YouTube", "yts": "YouTube Shorts"}.get(r["platform"], r["platform"])
        metric_label = "лайков" if r["metric_name"] == "likes" else "просмотров"
        src = html.escape(short_source(r["source"]))
        thumb = thumbnail_for(r)
        thumb_html = f'<img class="thumb" src="{thumb}" loading="lazy" alt="">' if thumb else f'<div class="thumb-placeholder">{plat_label[0]}</div>'

        score_disp = f"{r['score']:.1f}×"
        small_base_warn = ""
        if r["median"] < 100:
            small_base_warn = '<span class="warn-chip">маленький канал — проверь повторяемость</span>'

        cards_html.append(f"""
    <article class="card {star_class(r['score'], r['median'])}">
      <a class="thumb-link" href="{url}" target="_blank" rel="noopener">{thumb_html}</a>
      <div class="card-body">
        <div class="rank">#{i}</div>
        <div class="stars">{stars(r['score'])}</div>
        <div class="score-pill">{score_disp} от медианы</div>
        <h3><a href="{url}" target="_blank" rel="noopener">{title_safe}</a></h3>
        <div class="meta-row">
          <span class="src">{src}</span>
          <span class="dot">·</span>
          <span class="plat">{plat_label}</span>
          <span class="dot">·</span>
          <span class="date">{html.escape(r['date'])}</span>
        </div>
        <div class="num-row">
          <span><strong>{fmt_num(r['metric_val'])}</strong> {metric_label}</span>
          <span class="muted">медиана {fmt_num(r['median'])}</span>
          {('<span class="muted">' + fmt_num(r['followers']) + ' подписчиков</span>') if r['followers'] else ''}
        </div>
        {small_base_warn}
      </div>
    </article>""")

    return f"""
<section class="niche">
  <header class="niche-head">
    <h2>{html.escape(label)}</h2>
    <div class="niche-stats">{n_sources} источников · {total_in_period} постов за период · <strong>{total_outliers} outlier'ов</strong> (score ≥ 3)</div>
  </header>{dead_html}
  <div class="cards">{''.join(cards_html)}
  </div>
</section>"""


def main():
    today = datetime.date.today()
    weekday_ru = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"][today.weekday()]
    months_ru = ["января", "февраля", "марта", "апреля", "мая", "июня",
                 "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    date_human = f"{today.day} {months_ru[today.month-1]} {today.year}, {weekday_ru}"

    tsvs = sorted(glob.glob(os.path.join(DATA_DIR, "*.tsv")))

    niche_sections = []
    total_niches = 0
    total_sources = 0
    total_posts = 0
    total_outliers = 0

    for tsv_path in tsvs:
        niche_key = os.path.basename(tsv_path)[:-4]
        log_path = os.path.join(DATA_DIR, niche_key + ".log")
        meta, sources = parse_log(log_path)
        rows = parse_tsv(tsv_path)

        total_niches += 1
        total_sources += len(sources) if sources else len(meta)
        total_posts += sum(m.get("in_period", 0) for m in meta.values())
        total_outliers += len([r for r in rows])

        niche_sections.append(render_niche(niche_key, rows, meta, sources))

    summary_html = f"""
    <div class="summary">
      <div class="summary-grid">
        <div class="stat"><div class="v">{total_niches}</div><div class="l">ниш</div></div>
        <div class="stat"><div class="v cyan">{total_sources}</div><div class="l">источников</div></div>
        <div class="stat"><div class="v lime">{total_posts}</div><div class="l">постов за {DAYS}д</div></div>
        <div class="stat"><div class="v orange">{total_outliers}</div><div class="l">outlier'ов</div></div>
      </div>
    </div>"""

    html_doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Reels Outlier Digest · {today.isoformat()}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", system-ui, sans-serif;
  background: #f6f4ed;
  color: #1c1c1c;
  padding: 24px 32px 64px;
  max-width: 1200px;
  margin: 0 auto;
  line-height: 1.45;
}}
header.top {{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e5e0;
}}
header.top h1 {{
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}}
header.top .sub {{ color: #6b7280; font-size: 13px; margin-top: 4px; }}
header.top .right {{ text-align: right; color: #6b7280; font-size: 12px; font-style: italic; }}
.summary {{
  background: #ffffff;
  border-radius: 14px;
  padding: 18px 22px;
  margin-bottom: 32px;
  border: 1px solid #e5e5e0;
}}
.summary-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.stat {{
  background: #faf8f3;
  border-radius: 10px;
  padding: 14px 16px;
}}
.stat .v {{ font-size: 28px; font-weight: 700; color: #1c1c1c; }}
.stat .v.cyan {{ color: #0891b2; }}
.stat .v.lime {{ color: #16a34a; }}
.stat .v.orange {{ color: #ea580c; }}
.stat .l {{ font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }}
section.niche {{ margin-bottom: 40px; }}
section.niche.empty {{ opacity: 0.7; }}
.niche-head {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e5e0;
}}
.niche-head h2 {{
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
}}
.niche-stats {{
  color: #6b7280;
  font-size: 12px;
}}
.niche-stats strong {{ color: #1c1c1c; }}
.empty-note {{
  color: #9ca3af;
  font-style: italic;
  font-size: 13px;
  padding: 12px 16px;
  background: #faf8f3;
  border-radius: 10px;
}}
.dead-row {{
  background: #faf8f3;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  font-size: 12px;
}}
.dead-label {{
  color: #6b7280;
  font-weight: 600;
  margin-right: 4px;
}}
.dead-chip {{
  background: #ffffff;
  border: 1px solid #e5e5e0;
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 11px;
  color: #6b7280;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}}
.dead-chip.errored {{
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}}
.cards {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 14px;
}}
.card {{
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid #e5e5e0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.15s, box-shadow 0.15s;
}}
.card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 6px 20px -10px rgba(28,28,28,0.18);
}}
.card.lvl5 {{ border-left: 4px solid #dc2626; }}
.card.lvl4 {{ border-left: 4px solid #ea580c; }}
.card.lvl3 {{ border-left: 4px solid #16a34a; }}
.thumb-link {{ display: block; aspect-ratio: 16/9; overflow: hidden; background: #faf8f3; }}
.thumb {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.thumb-placeholder {{
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 48px; color: #c9c7bf;
  background: #faf8f3;
  font-weight: 700;
}}
.card-body {{
  padding: 14px 16px;
  display: flex; flex-direction: column; gap: 8px;
}}
.rank {{
  font-size: 11px; color: #9ca3af; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px;
}}
.stars {{ font-size: 14px; }}
.score-pill {{
  display: inline-block;
  background: #faf8f3;
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 12px;
  font-weight: 700;
  color: #1c1c1c;
  width: fit-content;
}}
.card.lvl5 .score-pill {{ background: #fef2f2; color: #dc2626; }}
.card.lvl4 .score-pill {{ background: #fff7ed; color: #ea580c; }}
.card.lvl3 .score-pill {{ background: #f0fdf4; color: #16a34a; }}
.card h3 {{
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  letter-spacing: -0.1px;
}}
.card h3 a {{ color: #1c1c1c; text-decoration: none; }}
.card h3 a:hover {{ color: #0891b2; text-decoration: underline; }}
.meta-row {{ font-size: 12px; color: #6b7280; display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }}
.meta-row .src {{ color: #1c1c1c; font-weight: 600; }}
.meta-row .dot {{ color: #c9c7bf; }}
.num-row {{ font-size: 12px; color: #1c1c1c; display: flex; gap: 12px; flex-wrap: wrap; }}
.num-row .muted {{ color: #6b7280; }}
.num-row strong {{ color: #1c1c1c; }}
.warn-chip {{
  font-size: 11px;
  background: #fff7ed;
  color: #ea580c;
  padding: 2px 8px;
  border-radius: 6px;
  width: fit-content;
}}
footer.bottom {{
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid #e5e5e0;
  color: #9ca3af;
  font-size: 11px;
  text-align: center;
}}
footer.bottom code {{ background: #ececea; padding: 1px 6px; border-radius: 4px; font-size: 11px; }}
</style>
</head>
<body>

<header class="top">
  <div>
    <h1>🎯 Outlier Digest</h1>
    <div class="sub">{date_human} · последние {DAYS} дней · только ролики, выбившиеся из своего ряда</div>
  </div>
  <div class="right">Reels-Research<br>weekly</div>
</header>

{summary_html}

{''.join(niche_sections)}

<footer class="bottom">
  Сгенерировано <code>~/.claude/skills/discover/scripts/digest_all.sh</code> · следующий запуск — понедельник 8:00<br>
  Outlier_Score = лайки/просмотры ÷ медиана последних N постов автора · порог ≥ 3×
</footer>

</body>
</html>"""

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_doc)

    print(f"render_digest: wrote {HTML_OUT} ({total_outliers} outliers across {total_niches} niches)")


if __name__ == "__main__":
    main()
