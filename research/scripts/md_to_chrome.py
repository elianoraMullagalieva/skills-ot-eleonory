#!/usr/bin/env python3
"""md_to_chrome.py — рендерит markdown в HTML с приятным стилем и открывает в Chrome.
Использование: python3 md_to_chrome.py <file.md>
"""
import sys, os, subprocess, tempfile, html
import markdown

if len(sys.argv) < 2:
    print("USAGE: md_to_chrome.py <file.md>"); sys.exit(2)

src = os.path.abspath(sys.argv[1])
with open(src, encoding="utf-8") as f:
    md_text = f.read()

body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
  max-width: 980px; margin: 0 auto; padding: 48px 40px 120px;
  color: #1c1c1c; background: #fafaf7; line-height: 1.55; font-size: 16px;
}
h1, h2, h3, h4, h5 { line-height: 1.25; margin-top: 2.2em; margin-bottom: 0.7em; }
h1 { font-size: 2.0em; border-bottom: 2px solid #e5e2d8; padding-bottom: 0.3em; }
h2 { font-size: 1.55em; border-bottom: 1px solid #e5e2d8; padding-bottom: 0.25em; }
h3 { font-size: 1.25em; color: #444; }
h4 { font-size: 1.05em; color: #b15c1c; }
a { color: #b15c1c; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 1px dashed #d6d2c4; margin: 2.5em 0; }
code {
  background: #f1ede0; padding: 2px 6px; border-radius: 4px;
  font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 0.9em;
}
pre {
  background: #f1ede0; padding: 14px 16px; border-radius: 8px; overflow-x: auto;
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 1em 0; padding: 0.4em 1em; border-left: 3px solid #b15c1c;
  background: #f5efe1; color: #555;
}
table {
  border-collapse: collapse; margin: 1em 0; width: 100%;
  background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
th, td { border: 1px solid #e5e2d8; padding: 8px 12px; text-align: left; vertical-align: top; font-size: 0.94em; }
th { background: #f1ede0; font-weight: 600; }
tr:nth-child(even) td { background: #fafaf5; }
strong { color: #1c1c1c; }
ul, ol { padding-left: 1.4em; }
li { margin: 0.2em 0; }
"""

title = html.escape(os.path.basename(src))
out_html = f"""<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head><body>
{body}
</body></html>"""

tmp = tempfile.NamedTemporaryFile(prefix="md_", suffix=".html", delete=False, mode="w", encoding="utf-8")
tmp.write(out_html); tmp.close()
print(tmp.name)
subprocess.run(["open", "-a", "Google Chrome", tmp.name], check=False)
