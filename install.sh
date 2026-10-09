#!/usr/bin/env bash
# Установка скиллов «Скиллы Эли Аноры» (skills-ot-eleonory) в Claude Code (macOS / Linux).
#
#   ./install.sh               скиллы + зависимости (ffmpeg, playwright, whisper)
#   ./install.sh --no-deps     только скопировать скиллы
#   ./install.sh --deps-only   только зависимости
#   ./install.sh --dest DIR    своя папка скиллов (по умолчанию ~/.claude/skills)
#   ./install.sh --onboarding  включить приветствие помощника при первом сообщении (без вопроса)
#   ./install.sh --no-onboarding  не спрашивать про приветствие
#
# Скрипт можно запускать сколько угодно раз: одинаковые скиллы пропускаются,
# изменённые одноимённые копии уходят в ~/.claude/skills/_backup_<дата>/.
# Если какая-то зависимость не ставится — скрипт предупреждает и идёт дальше.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/skills"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DO_SKILLS=1
DO_DEPS=1
DO_ONB=ask

while [ $# -gt 0 ]; do
  case "$1" in
    --no-deps)   DO_DEPS=0 ;;
    --deps-only) DO_SKILLS=0 ;;
    --onboarding)    DO_ONB=1 ;;
    --no-onboarding) DO_ONB=0 ;;
    --dest)      shift; DEST="${1:?после --dest укажи папку}" ;;
    -h|--help)   sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "Неизвестный параметр: $1 (см. ./install.sh --help)"; exit 2 ;;
  esac
  shift
done

if [ -t 1 ]; then
  C_OK=$'\033[32m'; C_WARN=$'\033[33m'; C_ERR=$'\033[31m'; C_B=$'\033[1m'; C_0=$'\033[0m'
else
  C_OK=""; C_WARN=""; C_ERR=""; C_B=""; C_0=""
fi
WARNINGS=()
say()  { printf '%s\n' "$*"; }
ok()   { printf '%s[OK]%s %s\n' "$C_OK" "$C_0" "$*"; }
warn() { printf '%s[ВНИМАНИЕ]%s %s\n' "$C_WARN" "$C_0" "$*"; WARNINGS+=("$*"); }
fail() { printf '%s[ОШИБКА]%s %s\n' "$C_ERR" "$C_0" "$*"; }
step() { printf '\n%s== %s ==%s\n' "$C_B" "$*" "$C_0"; }
have() { command -v "$1" >/dev/null 2>&1; }

OS="$(uname -s)"; ARCH="$(uname -m)"

# ------------------------------------------------------------------ скиллы
INSTALLED=()
install_skills() {
  step "Копирую скиллы в $DEST"
  if [ ! -d "$SRC" ]; then
    fail "Не найдена папка skills/ рядом со скриптом ($SRC). Запускай install.sh из корня скачанного репозитория."
    exit 1
  fi
  # Заглушки Git LFS (бывает при скачивании старых версий репозитория)
  if grep -rlsI --exclude-dir=.git "^version https://git-lfs.github.com/spec/v1" "$SCRIPT_DIR" >/dev/null 2>&1; then
    warn "В репозитории есть заглушки Git LFS вместо файлов. Скачай свежую версию репозитория."
  fi

  mkdir -p "$DEST" || { fail "Не могу создать $DEST"; exit 1; }
  local backup="$DEST/_backup_$(date +%Y%m%d-%H%M%S)"
  local copied=0 same=0 backed=0

  for dir in "$SRC"/*/; do
    [ -d "$dir" ] || continue
    local name; name="$(basename "$dir")"
    case "$name" in _*|.*) continue ;; esac
    if [ ! -f "$dir/SKILL.md" ]; then
      warn "Пропускаю $name: в папке нет SKILL.md"
      continue
    fi
    local target="$DEST/$name"
    if [ -e "$target" ] || [ -L "$target" ]; then
      if [ ! -L "$target" ] && diff -rq -x .DS_Store -x __pycache__ "$dir" "$target" >/dev/null 2>&1; then
        say "  = $name (уже установлен, без изменений)"
        INSTALLED+=("$name"); same=$((same+1))
        continue
      fi
      mkdir -p "$backup"
      if mv "$target" "$backup/$name"; then
        say "  ~ $name: старая версия сохранена в $backup/$name"
        backed=$((backed+1))
      else
        warn "Не смог убрать в бэкап $target — пропускаю $name"
        continue
      fi
    fi
    if cp -R "$dir" "$target"; then
      find "$target" \( -name .DS_Store -o -name __pycache__ \) -prune -exec rm -rf {} + 2>/dev/null
      say "  + $name"
      INSTALLED+=("$name"); copied=$((copied+1))
    else
      warn "Не удалось скопировать $name"
    fi
  done
  ok "Скопировано: $copied, без изменений: $same, в бэкап: $backed"
}

# ------------------------------------------------------------------ зависимости
pip_install() {
  # pip install --user с запасным вариантом для «externally managed» Python (Debian/Ubuntu/Homebrew)
  "$PY" -m pip install --user --upgrade "$@" >/tmp/skills-pip.log 2>&1 && return 0
  if grep -q "externally-managed-environment" /tmp/skills-pip.log 2>/dev/null; then
    "$PY" -m pip install --user --upgrade --break-system-packages "$@" >>/tmp/skills-pip.log 2>&1 && return 0
  fi
  return 1
}

install_ffmpeg() {
  if have ffmpeg; then ok "ffmpeg уже есть ($(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3))"; return; fi
  say "Ставлю ffmpeg…"
  if [ "$OS" = "Darwin" ]; then
    if have brew; then brew install ffmpeg && { ok "ffmpeg установлен"; return; }
    else warn "Нет Homebrew. Поставь его с https://brew.sh, затем: brew install ffmpeg"; return; fi
  elif have apt-get; then
    if [ "$(id -u)" = 0 ]; then apt-get update -qq && apt-get install -y ffmpeg && { ok "ffmpeg установлен"; return; }
    elif have sudo; then sudo apt-get update -qq && sudo apt-get install -y ffmpeg && { ok "ffmpeg установлен"; return; }
    fi
  elif have dnf; then sudo dnf install -y ffmpeg && { ok "ffmpeg установлен"; return; }
  elif have pacman; then sudo pacman -S --noconfirm ffmpeg && { ok "ffmpeg установлен"; return; }
  fi
  warn "ffmpeg не установился. Поставь вручную (macOS: brew install ffmpeg; Ubuntu: sudo apt install ffmpeg) — без него не будет рендера видео."
}

install_python_deps() {
  PY=""
  for c in python3 python; do
    if have "$c" && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null; then PY="$c"; break; fi
  done
  if [ -z "$PY" ]; then
    warn "Не найден Python 3.8+. Поставь Python (macOS: brew install python или https://www.python.org), затем перезапусти ./install.sh --deps-only"
    return
  fi
  ok "Python: $("$PY" --version 2>&1)"
  if ! "$PY" -m pip --version >/dev/null 2>&1; then
    "$PY" -m ensurepip --user >/dev/null 2>&1 || true
  fi
  if ! "$PY" -m pip --version >/dev/null 2>&1; then
    warn "Нет pip для $PY (Ubuntu: sudo apt install python3-pip). Python-зависимости пропущены."
    return
  fi

  say "Ставлю playwright и pillow (рендер HTML → видео, снимки сцен)…"
  if pip_install playwright pillow; then
    ok "playwright и pillow установлены"
    say "Скачиваю Chromium для playwright (~150 МБ)…"
    if "$PY" -m playwright install chromium >/tmp/skills-playwright.log 2>&1; then
      ok "Chromium для playwright готов"
    else
      warn "Chromium не скачался (лог: /tmp/skills-playwright.log). Повтори: $PY -m playwright install chromium"
    fi
  else
    warn "playwright не установился (лог: /tmp/skills-pip.log). Повтори: $PY -m pip install --user playwright pillow"
  fi

  if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
    say "Apple Silicon — ставлю mlx-whisper (пословные таймкоды речи)…"
    if pip_install mlx-whisper; then ok "mlx-whisper установлен"; else warn "mlx-whisper не установился (лог: /tmp/skills-pip.log). Повтори: $PY -m pip install --user mlx-whisper"; fi
  else
    say "Ставлю faster-whisper (пословные таймкоды речи)…"
    if pip_install faster-whisper; then ok "faster-whisper установлен"; else warn "faster-whisper не установился (лог: /tmp/skills-pip.log). Повтори: $PY -m pip install --user faster-whisper"; fi
  fi

  say "Ставлю cairosvg (превью для svg-creator, необязательно)…"
  if [ "$OS" = "Darwin" ] && have brew && ! brew list cairo >/dev/null 2>&1; then brew install cairo >/dev/null 2>&1 || true; fi
  if pip_install cairosvg; then ok "cairosvg установлен"; else warn "cairosvg не установился — svg-creator не сможет делать PNG-превью (нужна библиотека cairo)."; fi

  local userbin; userbin="$("$PY" -m site --user-base 2>/dev/null)/bin"
  case ":$PATH:" in
    *":$userbin:"*) ;;
    *) warn "Папки $userbin нет в PATH — команды вроде mlx_whisper могут не находиться. Добавь в ~/.zshrc или ~/.bashrc: export PATH=\"$userbin:\$PATH\"" ;;
  esac
}

install_deps() {
  step "Зависимости для монтажа и рендера"
  install_ffmpeg
  install_python_deps
}

# ------------------------------------------------------------------ проверка
verify() {
  step "Проверка установки"
  local bad=0 n=0
  for dir in "$SRC"/*/; do
    local name; name="$(basename "$dir")"
    case "$name" in _*|.*) continue ;; esac
    [ -f "$dir/SKILL.md" ] || continue
    n=$((n+1))
    if [ -f "$DEST/$name/SKILL.md" ] && head -1 "$DEST/$name/SKILL.md" | grep -q '^---'; then
      printf '  %s[OK]%s %s\n' "$C_OK" "$C_0" "$name"
    else
      printf '  %s[НЕТ]%s %s — нет %s\n' "$C_ERR" "$C_0" "$name" "$DEST/$name/SKILL.md"; bad=$((bad+1))
    fi
  done
  if [ "$bad" -eq 0 ]; then
    ok "Все $n скиллов на месте: $DEST/<имя>/SKILL.md"
  else
    fail "$bad из $n скиллов не установились — смотри сообщения выше"
  fi
  return "$bad"
}

say "${C_B}Скиллы Эли Аноры — установка скиллов Claude Code${C_0}"
say "Система: $OS $ARCH"
RC=0
if [ "$DO_SKILLS" = 1 ]; then install_skills; fi
if [ "$DO_DEPS" = 1 ]; then install_deps; else say ""; say "Зависимости пропущены (--no-deps). Поставить позже: ./install.sh --deps-only"; fi
if [ "$DO_SKILLS" = 1 ]; then verify || RC=1; fi

# Приветствие помощника при первом сообщении (правка ~/.claude/CLAUDE.md — только с согласия)
if [ "$DO_SKILLS" = 1 ] && [ -f "$DEST/reels-montazh-pro/scripts/onboarding_hook.py" ]; then
  if [ "$DO_ONB" = ask ] && [ -t 0 ]; then
    say ""
    printf 'Включить приветствие: при первом сообщении помощник расскажет, что умеет (добавит 5 строк в ~/.claude/CLAUDE.md)? [Д/н] '
    read -r ans || ans=""
    case "$ans" in [НнNn]*) DO_ONB=0 ;; *) DO_ONB=1 ;; esac
  fi
  if [ "$DO_ONB" = 1 ]; then
    if python3 "$DEST/reels-montazh-pro/scripts/onboarding_hook.py" --onboarding --yes; then ok "Приветствие включено"; else warn "Не удалось включить приветствие — можно позже: python3 $DEST/reels-montazh-pro/scripts/onboarding_hook.py --onboarding"; fi
  else
    say "Приветствие можно включить позже: python3 $DEST/reels-montazh-pro/scripts/onboarding_hook.py --onboarding"
  fi
fi

if [ "${#WARNINGS[@]}" -gt 0 ]; then
  step "Предупреждения (${#WARNINGS[@]})"
  for w in "${WARNINGS[@]}"; do say "  - $w"; done
fi
say ""
if [ "$DO_SKILLS" = 1 ]; then
  say "Готово. Перезапусти Claude Code (или открой новую сессию) — скиллы подхватятся автоматически."
  say "Проверка в Claude Code: спроси «какие у тебя есть скиллы?» или набери /skills."
fi
exit "$RC"
