#!/usr/bin/env python3
"""Проверка репозитория скиллов перед публикацией.

Запуск из корня репозитория:
    python3 tools/validate.py            # проверить skills/ и весь репозиторий
    python3 tools/validate.py --skills-dir ~/.claude/skills --no-repo-checks

Что проверяется:
  * каждая папка skills/<имя>/ содержит SKILL.md (Claude Code ищет скиллы ровно на один уровень вглубь);
  * у SKILL.md есть YAML-frontmatter с name и description;
  * name — [a-z0-9-]{1,64}, без дефиса в начале/конце и двойных дефисов, совпадает с именем папки;
  * description не пустой и не длиннее 1024 символов;
  * нет двух скиллов с одинаковым name;
  * в текстовых файлах скиллов нет абсолютных путей вида /Users/..., /home/..., C:\\Users\\...;
  * нигде нет указателей Git LFS и LFS-правил в .gitattributes;
  * ссылки на файлы внутри скилла (markdown-ссылки и `пути/в/обратных/кавычках`) существуют;
  * в репозитории нет файлов больше 50 МБ (GitHub их не любит);
  * по всему репозиторию нет секретов и личных данных: токенов Telegram-ботов, ключей
    sk-…/AIza…/ghp_…/github_pat_…/xox…, приватных ключей, опасных настроек (bypassPermissions,
    skipDangerousModePermissionPrompt), путей песочницы claude.ai (/mnt/user-data, /home/claude),
    незаполненных шаблонов {{переменная}}, личных путей /Users/<имя>/, имён компьютеров,
    e-mail (кроме example.com и noreply), номеров банковских карт, IBAN и телефонов +7;
  * ссылки вида ~/.claude/skills/<имя>/ ведут на скиллы, которые есть в skills/.

Код выхода: 0 — ошибок нет (предупреждения допустимы), 1 — есть ошибки.
Зависимостей нет: работает на чистом python3 (PyYAML используется, если установлен).
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TEXT_EXT = {".md", ".py", ".js", ".mjs", ".cjs", ".ts", ".html", ".htm", ".css", ".json",
            ".yaml", ".yml", ".txt", ".sh", ".ps1", ".svg", ".toml", ".xml", ".csv"}
LFS_MAGIC = b"version https://git-lfs.github.com/spec/v1"
ABS_PATH_RE = re.compile(r"(/Users/[A-Za-z0-9._-]+/|/home/[a-z][a-z0-9._-]*/|[A-Za-z]:\\\\?Users\\\\?)")
AUTHOR_HOME_RE = re.compile(r"~/(Desktop|Documents|Downloads|Library)/")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
CODE_RE = re.compile(r"`([^`\n]+)`")
PATHLIKE_RE = re.compile(r"^[\w.\-/ *А-Яа-яЁё+@]+$")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
MAX_FILE_MB_ERROR = 50

# --- секреты и личные данные (проверяются по всему репозиторию)
SECRET_PATTERNS = [
    (re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}"), "токен Telegram-бота"),
    (re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}"), "API-ключ sk-…"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "ключ Google API (AIza…)"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "токен GitHub (ghp_…)"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}"), "токен GitHub (github_pat_…)"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "токен Slack (xox…)"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "приватный ключ"),
    (re.compile(r"/mnt/user-data|/mnt/skills|/home/claude\b"), "путь песочницы claude.ai — на компьютере пользователя его нет"),
    (re.compile(r"\{\{\s*[a-z_][a-z0-9_]*\s*\}\}"), "незаполненный шаблон {{…}}"),
    (re.compile(r"/Users/(?!<|USER|you|имя|name|Shared)[A-Za-z0-9._-]+/"), "личный путь /Users/<имя>/"),
    (re.compile(r"-Users-(?!<)[a-z0-9._]+\b"), "личный путь в имени папки памяти (-Users-<имя>)"),
    (re.compile(r"MacBook-(?:Air|Pro)-|\.local\b(?=[>\s\"'])"), "имя компьютера"),
    (re.compile(r"\+7[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}\b"), "номер телефона +7"),
]
DANGEROUS_SETTINGS_RE = re.compile(r"\"?defaultMode\"?\s*:\s*\"?bypassPermissions|skipDangerousModePermissionPrompt\"?\s*:\s*true")
DANGEROUS_WORD_RE = re.compile(r"bypassPermissions|skipDangerousModePermissionPrompt")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
EMAIL_OK_RE = re.compile(r"@(example\.(com|org|net)|users\.noreply\.github\.com|anthropic\.com)$|^noreply@|^git@github\.com$", re.I)
CARD_RE = re.compile(r"(?<![\d.])(?:\d{4}[ -]?){3}\d{4}(?![\d.])")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}(?: ?[A-Z0-9]{1,4})?\b")
SKILL_REF_RE = re.compile(r"~/\.claude/skills/([a-z0-9][a-z0-9-]*)")
SCAN_EXT = TEXT_EXT | {".jsx", ".tsx", ".env", ".ini", ".cfg", ".conf", ".command", ".bat", ".swift", ".srt", ".vtt", ".plist"}
MAX_FILE_MB_WARN = 20


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"ОШИБКА  {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"ВНИМАНИЕ {where}: {msg}")


# ---------------------------------------------------------------- frontmatter
def split_frontmatter(text: str):
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        inner = v[1:-1]
        if v[0] == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        else:
            inner = inner.replace("''", "'")
        return inner
    return v


def parse_yaml_simple(src: str) -> dict:
    """Мини-парсер для плоского frontmatter (если нет PyYAML)."""
    data: dict = {}
    lines = src.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2)
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = (" " if val.startswith(">") else "\n").join(b for b in block if b).strip()
            continue
        if val == "":
            # список или вложенная структура
            items = []
            i += 1
            while i < len(lines) and lines[i].startswith((" ", "\t", "-")):
                s = lines[i].strip()
                if s.startswith("- "):
                    items.append(_unquote(s[2:]))
                i += 1
            data[key] = items
            continue
        data[key] = _unquote(val)
        i += 1
    return data


def parse_frontmatter(src: str):
    try:
        import yaml  # type: ignore

        try:
            d = yaml.safe_load(src)
        except Exception as e:  # noqa: BLE001
            return None, f"frontmatter не парсится как YAML: {e}".replace("\n", " ")
        if not isinstance(d, dict):
            return None, "frontmatter не является словарём ключ: значение"
        return d, None
    except ImportError:
        for line in src.splitlines():
            m = re.match(r"^[A-Za-z0-9_-]+:\s+(.*)$", line)
            if m:
                v = m.group(1).strip()
                if v and v[0] not in "\"'>|[{" and (": " in v or " #" in v):
                    return None, ("в значении есть ': ' или ' #' без кавычек — это невалидный YAML, "
                                  "оберни значение в двойные кавычки: " + line[:80])
        return parse_yaml_simple(src), None


# ---------------------------------------------------------------- helpers
def is_text(p: Path) -> bool:
    return p.suffix.lower() in TEXT_EXT or p.name in {"LICENSE", "NOTICE", ".gitignore"}


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            yield Path(dirpath) / f


def rel(p: Path, base: Path) -> str:
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)


def check_ref(skill_dir: Path, base_dir: Path, target: str) -> bool:
    """True если путь существует (поддерживаются * и ?)."""
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return True
    cand = (base_dir / target)
    if any(ch in target for ch in "*?"):
        return bool(glob.glob(str(cand)))
    return cand.exists() or (skill_dir / target).exists()


# ---------------------------------------------------------------- checks
def check_skill(skill_dir: Path, rep: Report, names: dict, base: Path) -> None:
    where = rel(skill_dir, base)
    skill_md = skill_dir / "SKILL.md"
    if len(skill_dir.name) > 64 or not NAME_RE.match(skill_dir.name):
        rep.err(where, "имя папки должно быть латиницей [a-z0-9-] (как name в SKILL.md)")
    if not skill_md.is_file():
        nested = [p for p in skill_dir.rglob("SKILL.md")]
        hint = f" (найдено глубже: {', '.join(rel(n, base) for n in nested[:3])})" if nested else ""
        rep.err(where, "нет SKILL.md — Claude Code не увидит скилл" + hint)
        return

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm_src = split_frontmatter(text)
    if fm_src is None:
        rep.err(rel(skill_md, base), "нет YAML-frontmatter (файл должен начинаться с '---', затем name/description, затем '---')")
        return
    fm, perr = parse_frontmatter(fm_src)
    if perr:
        rep.err(rel(skill_md, base), perr)
        return

    name = fm.get("name")
    desc = fm.get("description")
    if not isinstance(name, str) or not name.strip():
        rep.err(rel(skill_md, base), "нет поля name")
    else:
        name = name.strip()
        if len(name) > 64 or not NAME_RE.match(name):
            rep.err(rel(skill_md, base), f"name '{name}' не соответствует [a-z0-9-]{{1,64}} (латиница в нижнем регистре, цифры, дефисы)")
        if name != skill_dir.name:
            rep.err(rel(skill_md, base), f"name '{name}' не совпадает с именем папки '{skill_dir.name}'")
        if name in names:
            rep.err(rel(skill_md, base), f"дубль имени '{name}' (уже есть в {names[name]})")
        else:
            names[name] = where
    if not isinstance(desc, str) or not desc.strip():
        rep.err(rel(skill_md, base), "нет поля description (или оно пустое)")
    else:
        if len(desc) > 1024:
            rep.err(rel(skill_md, base), f"description длиннее 1024 символов ({len(desc)})")
        if re.search(r"<[A-Za-z/][^>]*>", desc):
            rep.warn(rel(skill_md, base), "в description есть XML/HTML-теги — лучше убрать")

    for extra in skill_dir.rglob("SKILL.md"):
        if extra != skill_md:
            rep.warn(rel(extra, base), "вложенный SKILL.md — Claude Code его не подхватит как отдельный скилл")

    # содержимое файлов скилла
    top_entries = {p.name for p in skill_dir.iterdir()}
    for f in iter_files(skill_dir):
        try:
            head = f.open("rb").read(200)
        except OSError:
            continue
        if head.startswith(LFS_MAGIC):
            rep.err(rel(f, base), "это указатель Git LFS, а не настоящий файл")
            continue
        if not is_text(f):
            continue
        try:
            body = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for ln, line in enumerate(body.splitlines(), 1):
            if ABS_PATH_RE.search(line):
                rep.err(f"{rel(f, base)}:{ln}", "абсолютный путь к чужому компьютеру: " + line.strip()[:120])
            if f.suffix == ".md" and AUTHOR_HOME_RE.search(line):
                rep.warn(f"{rel(f, base)}:{ln}", "путь к личной папке автора (~/Desktop, ~/Documents…): " + line.strip()[:120])
        if f.suffix.lower() == ".md":
            md_dir = f.parent
            for m in list(MD_LINK_RE.finditer(body)) + list(MD_IMG_RE.finditer(body)):
                t = m.group(1).strip("<>")
                if re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) or t.startswith(("#", "/", "~", "{")):
                    continue
                if not check_ref(skill_dir, md_dir, t):
                    rep.err(rel(f, base), f"ссылка на несуществующий файл: {t}")
        if f == skill_md:
            for m in CODE_RE.finditer(body):
                t = m.group(1).strip()
                if ("/" not in t or "://" in t or t.startswith(("/", "~", "$", "..", ".")) or
                        "…" in t or "<" in t or not PATHLIKE_RE.match(t)):
                    continue
                first = t.split("/", 1)[0]
                if first not in top_entries:
                    continue  # путь не про эту папку (например, в проекте пользователя)
                if not check_ref(skill_dir, skill_dir, t.rstrip("/")):
                    rep.err(rel(f, base), f"упомянут несуществующий файл скилла: `{t}`")


def check_repo(repo: Path, rep: Report) -> None:
    ga = repo / ".gitattributes"
    if ga.is_file() and "filter=lfs" in ga.read_text(encoding="utf-8", errors="replace"):
        rep.err(".gitattributes", "есть правила Git LFS (filter=lfs) — у людей без LFS скачаются заглушки")
    for f in iter_files(repo):
        if "tools" in f.relative_to(repo).parts[:1] and f.name == "validate.py":
            continue
        try:
            size = f.stat().st_size
            head = f.open("rb").read(200)
        except OSError:
            continue
        if head.startswith(LFS_MAGIC):
            rep.err(rel(f, repo), "указатель Git LFS вместо файла")
        mb = size / 1024 / 1024
        if mb > MAX_FILE_MB_ERROR:
            rep.err(rel(f, repo), f"файл {mb:.0f} МБ — больше {MAX_FILE_MB_ERROR} МБ, пережми или убери")
        elif mb > MAX_FILE_MB_WARN:
            rep.warn(rel(f, repo), f"файл {mb:.0f} МБ — тяжеловато для репозитория")


def _luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def _iban_ok(s: str) -> bool:
    s = s.replace(" ", "")
    if not 15 <= len(s) <= 34:
        return False
    r = s[4:] + s[:4]
    try:
        num = "".join(str(int(c, 36)) for c in r)
    except ValueError:
        return False
    return int(num) % 97 == 1


def check_sensitive(repo: Path, skills_dir: Path, rep: Report) -> None:
    """Секреты, личные данные и опасные настройки — по всем текстовым файлам репозитория."""
    skill_names = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.is_dir() else set()
    self_path = Path(__file__).resolve()
    for f in iter_files(repo):
        if f.resolve() == self_path:
            continue
        if not (f.suffix.lower() in SCAN_EXT or f.name in {"LICENSE", "NOTICE", ".gitignore", ".gitattributes"}
                or f.suffix == ""):
            continue
        try:
            body = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        where_f = rel(f, repo)
        for ln, line in enumerate(body.splitlines(), 1):
            where = f"{where_f}:{ln}"
            for rx, what in SECRET_PATTERNS:
                m = rx.search(line)
                if m:
                    rep.err(where, f"{what}: {m.group(0)[:60]}")
            if DANGEROUS_SETTINGS_RE.search(line) or (f.suffix.lower() != ".md" and DANGEROUS_WORD_RE.search(line)):
                rep.err(where, "опасная настройка Claude Code (bypassPermissions / skipDangerousModePermissionPrompt) — отключает запросы разрешений")
            for m in EMAIL_RE.finditer(line):
                e = m.group(0)
                if EMAIL_OK_RE.search(e) or e.split("@", 1)[1].lower().endswith((".png", ".jpg", ".svg", ".webp", ".webm", ".mp4")):
                    continue
                rep.err(where, f"e-mail в файле (замени на name@example.com): {e}")
            for m in CARD_RE.finditer(line):
                digits = re.sub(r"\D", "", m.group(0))
                if _luhn_ok(digits) and len(set(digits)) > 1:
                    rep.err(where, f"похоже на номер банковской карты: {m.group(0)}")
                elif " " in m.group(0) or "-" in m.group(0):
                    rep.warn(where, f"16 цифр группами по 4 — проверь, не номер ли это карты: {m.group(0)}")
            for m in IBAN_RE.finditer(line):
                if _iban_ok(m.group(0)):
                    rep.err(where, f"похоже на IBAN: {m.group(0)}")
            for m in SKILL_REF_RE.finditer(line):
                if skill_names and m.group(1) not in skill_names:
                    rep.err(where, f"ссылка на скилл, которого нет в skills/: ~/.claude/skills/{m.group(1)}")


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Проверка скиллов")
    ap.add_argument("--skills-dir", type=Path, default=repo / "skills")
    ap.add_argument("--no-repo-checks", action="store_true", help="не проверять .gitattributes, размеры файлов, секреты и личные данные")
    args = ap.parse_args()

    skills_dir = args.skills_dir.expanduser().resolve()
    rep = Report()
    if not skills_dir.is_dir():
        print(f"Нет папки со скиллами: {skills_dir}")
        return 1

    base = skills_dir.parent
    names: dict = {}
    dirs = sorted(p for p in skills_dir.iterdir()
                  if p.is_dir() and not p.name.startswith((".", "_")))
    for f in skills_dir.iterdir():
        if f.is_file() and f.name not in {".DS_Store", "README.md"}:
            rep.warn(rel(f, base), "файл прямо в skills/ — сюда кладут только папки скиллов")
    for d in dirs:
        check_skill(d, rep, names, base)
    if not args.no_repo_checks:
        check_repo(repo, rep)
        check_sensitive(repo, skills_dir, rep)

    for w in rep.warnings:
        print(w)
    for e in rep.errors:
        print(e)
    print()
    print(f"Скиллов проверено: {len(dirs)} | ошибок: {len(rep.errors)} | предупреждений: {len(rep.warnings)}")
    if names:
        print("Скиллы: " + ", ".join(sorted(names)))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
