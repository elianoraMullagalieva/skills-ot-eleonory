# Скиллы Эли Аноры — библиотека для Claude Code

Открытая библиотека скиллов для [Claude Code](https://claude.com/claude-code): монтаж Reels, SVG и моушен, дизайн интерфейсов и лендингов, генерация изображений и видео, формы для сайтов.

Скилл — это папка с `SKILL.md` (инструкции) и файлами, которые ему нужны (шаблоны, шрифты, скрипты). Claude Code ищет скиллы в `~/.claude/skills/<имя>/SKILL.md` и сам подключает нужный, когда задача подходит. Здесь **30 скиллов**, все лежат плоско в `skills/<имя>/`.

## Установка в одну команду

### macOS / Linux

```bash
git clone https://github.com/elianoraMullagalieva/skills-ot-eleonory.git
cd skills-ot-eleonory && ./install.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/elianoraMullagalieva/skills-ot-eleonory.git
cd skills-ot-eleonory
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### Без git — через ZIP

1. На GitHub нажми **Code → Download ZIP**.
2. Распакуй архив и открой терминал в папке `skills-ot-eleonory-main`.
3. macOS/Linux: `bash install.sh` · Windows: `powershell -ExecutionPolicy Bypass -File .\install.ps1`

Git LFS не нужен: все файлы лежат в репозитории как обычные, ZIP скачивается целиком.

### Что делает установщик

1. Копирует каждую папку из `skills/` в `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills\`). Если там уже есть скилл с таким же именем и он отличается, старая версия переносится в `~/.claude/skills/_backup_<дата>/`. Одинаковые скиллы пропускаются, поэтому скрипт можно запускать повторно (например, после `git pull`).
2. Ставит зависимости для монтажа и рендера, если их ещё нет: `ffmpeg`, `playwright` + `pillow` + Chromium, `mlx-whisper` (Mac на Apple Silicon) или `faster-whisper` (остальные), `cairosvg` (необязательно). Если что-то не поставилось, скрипт предупреждает и продолжает.
3. Спрашивает, включить ли приветствие помощника монтажа (`reels-montazh-pro`): при первом сообщении он расскажет, что умеет. Для этого в `~/.claude/CLAUDE.md` добавляются 5 строк — только с твоего согласия.
4. Проверяет, что у каждого скилла на месте `SKILL.md`.

| macOS/Linux | Windows | Что делает |
|---|---|---|
| `./install.sh --no-deps` | `.\install.ps1 -NoDeps` | только скопировать скиллы |
| `./install.sh --deps-only` | `.\install.ps1 -DepsOnly` | только зависимости |
| `./install.sh --dest ПАПКА` | `.\install.ps1 -Dest ПАПКА` | установить в другую папку (например, `.claude/skills` проекта) |
| `./install.sh --onboarding` | `.\install.ps1 -Onboarding` | включить приветствие без вопроса |
| `./install.sh --no-onboarding` | `.\install.ps1 -NoOnboarding` | не спрашивать про приветствие |

После установки **перезапусти Claude Code** (или открой новую сессию) и проверь: спроси «какие у тебя есть скиллы?» или набери `/skills`.

### Установить один скилл вручную

```bash
mkdir -p ~/.claude/skills
cp -R skills/svg-creator ~/.claude/skills/
```

Путь должен получиться ровно `~/.claude/skills/<имя>/SKILL.md` — без лишних вложенных папок. Копируй папку целиком, вместе с `fonts/`, скриптами и шаблонами.

## Скиллы

### Монтаж и Reels

| Скилл | Для чего |
|---|---|
| `reels-montazh-pro` | Монтаж Reels из длинной записи с дублями: нарезка по словам (whisper), без пауз и повторов, раскладка под CapCut, FCPXML для DaVinci, готовый 4K |
| `reels-infografika` | SVG-инфографика 1080×1040 над говорящей головой в стиле бренда, синхрон по словам речи |
| `montazh-prozrachnaya-tipografika` | Прозрачный субтитр-монтаж с кинетической типографикой поверх видео, рендер в mp4 и ProRes с альфой |
| `montazh-zagolovok-rvanyi` | Монтаж «заголовок + рваный»: крупное вступление, затем мелкие пословные субтитры по краям |
| `eli-reels-graphics` | Графика-подложка для Reels за говорящей головой: жёсткая типо-шкала, SVG-анимации, рендер `record.py` |
| `premium-motion-infographics` | Дорогая смысловая SVG/HTML-инфографика для Reels и презентаций, с визуальным планом и QA |

### SVG и анимация

| Скилл | Для чего |
|---|---|
| `svg-creator` | Иконки, иллюстрации, логотипы, диаграммы в SVG с циклом «нарисовал → отрендерил → проверил» (англ.) |
| `svg-animations` | SVG-анимации: SMIL, CSS, отрисовка контуров, морфинг, маски и фильтры (англ.) |
| `animejs` | Anime.js: таймлайны, stagger, морфинг; шаблон Reels-анимации 1080×1920 и запись в mp4 (`record.py`) |

### Дизайн и UI

| Скилл | Для чего |
|---|---|
| `design-team-standards` | Стандарты студии для сайтов и лендингов: пропорции медиа, контраст, фоны, цвета из Figma, отступы, чек-лист |
| `dizayn-futuristik` | Футуристичные лендинги и hero-секции «как на Awwwards / Apple / Linear», чек-лист антипаттернов |
| `frontend-design` | Выразительные продакшн-интерфейсы без «AI-шаблонности» (англ., Anthropic) |
| `impeccable` | Дизайн, аудит, критика и полировка интерфейсов: 20+ команд (`/impeccable craft`, `audit`, `polish`…) (англ.) |
| `design-taste-frontend` | Senior UI/UX-инженер: метрические правила вёрстки, компонентная архитектура (англ.) |
| `emil-design-eng` | Философия UI-полировки Эмиля Ковальски: детали, анимации, ощущение качества (англ.) |
| `gpt-taste` | Редакционная типографика, bento-сетки, GSAP ScrollTrigger, структура AIDA (англ.) |
| `high-end-visual-design` | Шрифты, отступы, тени и карточки «как у дорогого агентства» (англ.) |
| `industrial-brutalist-ui` | Брутализм: швейцарская типографика и эстетика военного терминала (англ.) |
| `minimalist-ui` | Редакционный минимализм: тёплый монохром, плоские bento-сетки (англ.) |
| `redesign-existing-projects` | Апгрейд существующего сайта до премиум-уровня без поломки функциональности (англ.) |
| `stitch-design-taste` | DESIGN.md для Google Stitch с анти-шаблонными правилами (англ.) |

### Генерация изображений и видео

| Скилл | Для чего |
|---|---|
| `nano-banana-imagegen` | Промпты для Nano Banana (Gemini Image): портреты, предметка, баннеры, замена фона, сохранение лица |
| `kling-video` | Промпт-инженерия для Kling 3.0: видео, оживление фото, камера, стили, аудио |
| `brandkit` | Брендбук-доски, логосистемы, айдентика (англ.) |
| `image-to-code` | Сначала генерирует макет картинкой, потом верстает по нему (англ., написан под Codex) |
| `imagegen-frontend-web` | Референсы веб-страниц: по картинке на каждую секцию (англ.) |
| `imagegen-frontend-mobile` | Концепты экранов мобильного приложения (англ.) |

У `brandkit`, `image-to-code` и `imagegen-*` в Claude Code нет встроенного генератора картинок: они работают как гайд по промптам или вместе с внешним инструментом генерации (MCP или сервис).

### Сайты и формы

| Скилл | Для чего |
|---|---|
| `forms-telegram-bot` | Анкеты и формы заявок для Tilda и статичных сайтов с отправкой в Telegram-бота и блоком согласий по 152-ФЗ / 38-ФЗ |

В шаблонах `forms-telegram-bot` стоят плейсхолдеры `YOUR_BOT_TOKEN` и `YOUR_CHAT_ID`. Свой токен подставляй только в копию, которую выкладываешь на сайт, и никогда не коммить его в git. Для серьёзных форм используй серверный прокси — подробности в `SKILL.md` скилла.

### Claude Code

| Скилл | Для чего |
|---|---|
| `help-ru` | Все команды Claude Code на русском (`/help-ru`) |
| `full-output-enforcement` | Запрещает модели обрезать код и вставлять заглушки (англ.) |

## Что ещё в репозитории

```
skills/                 скиллы: по одной папке на скилл (это и ставит установщик)
extras/                 не скиллы — справочные материалы, установщик их не трогает
  etalony-html/           эталонные HTML-ролики и видео-примеры (открываются в браузере)
  fonts/commercial-safe/  Manrope и JetBrains Mono + лицензии OFL-1.1
  fonts/display/          как скачать Bebas Neue Cyrillic и Gogol (в репозиторий не входят)
  tipografika-v-tekstah/  правила типографики в текстах
  figma-instrukcii/       уроки по Figma
  gaidy-generacii/        гайды по Higgsfield и Nano Banana
  veb-gaidy/              как сделать сайт с видео на фоне (скролл-эффект)
  claude-code/            инструкции по Claude Code и статусная строка (безопасный пример настроек)
tools/validate.py       проверка репозитория перед публикацией
install.sh / install.ps1
THIRD_PARTY_LICENSES.md лицензии сторонних скиллов
```

## Зависимости

Нужны не всем скиллам — только монтажу, рендеру и превью. Установщик ставит их сам.

| Что | Кому нужно | Как поставить вручную |
|---|---|---|
| Python 3.8+ | все скрипты рендера | python.org или `brew install python` |
| ffmpeg | рендер видео, нарезка | macOS: `brew install ffmpeg` · Ubuntu: `sudo apt install ffmpeg` · Windows: `winget install Gyan.FFmpeg` |
| playwright + Chromium, pillow | HTML → видео, снимки сцен (`animejs`, `eli-reels-graphics`, `montazh-*`, `reels-*`) | `python3 -m pip install --user playwright pillow && python3 -m playwright install chromium` |
| mlx-whisper / faster-whisper | пословные таймкоды речи | Apple Silicon: `pip install --user mlx-whisper` · остальные: `pip install --user faster-whisper` |
| cairosvg + библиотека cairo | PNG-превью в `svg-creator` (необязательно) | `brew install cairo` / `sudo apt install libcairo2`, затем `pip install --user cairosvg` |
| Node.js 18+ | скрипты `impeccable` (`node …/scripts/*.mjs`) | nodejs.org или `brew install node` |
| jq | статусная строка из `extras/claude-code` | `brew install jq` / `sudo apt install jq` |

## Если что-то не работает

| Проблема | Решение |
|---|---|
| Claude Code не видит скиллы | Файлы должны лежать ровно так: `~/.claude/skills/<имя>/SKILL.md` (без лишней папки `skills` внутри и не глубже). Перезапусти Claude Code. Проверка: `ls ~/.claude/skills/*/SKILL.md` |
| `./install.sh: Permission denied` | Запусти через bash: `bash install.sh` |
| Windows: «выполнение сценариев отключено» | `powershell -ExecutionPolicy Bypass -File .\install.ps1` |
| Windows: кракозябры вместо русского | Используй Windows Terminal или PowerShell 7; установке это не мешает |
| Вместо видео или шрифтов маленькие текстовые файлы `version https://git-lfs…` | Это старая версия репозитория с Git LFS. Скачай заново (`git clone` или ZIP) |
| `git clone` ругается на LFS / «over its data quota» | Скачай свежую версию — в ней LFS нет. Если ошибка осталась: `GIT_LFS_SKIP_SMUDGE=1 git clone …` |
| `ffmpeg: command not found` | Поставь ffmpeg (см. «Зависимости») и открой новое окно терминала |
| `error: externally-managed-environment` при pip | Установщик сам повторяет с `--break-system-packages` для `--user`. Вручную — то же или используй venv |
| `Executable doesn't exist … ms-playwright` | Не скачан браузер: `python3 -m playwright install chromium` |
| `mlx_whisper: command not found` | Добавь папку пользовательских скриптов Python в PATH: `export PATH="$(python3 -m site --user-base)/bin:$PATH"` |
| mlx-whisper не ставится на Intel Mac / Windows / Linux | Это нормально: mlx работает только на Apple Silicon. Используй `faster-whisper` |
| svg-creator: `no library called "cairo"` | macOS: `brew install cairo` · Ubuntu: `sudo apt install libcairo2` · Windows: нужен GTK3 runtime |
| Шрифты в HTML-шаблоне не подхватились | Шаблон ищет их в `fonts/` рядом с HTML. Копируя шаблон в свой проект, копируй и папку `fonts/` |
| Эталон с Bebas/Gogol выглядит иначе | Эти шрифты не входят в репозиторий (лицензия не подтверждена). См. `extras/fonts/display/СКАЧАТЬ_BEBAS_И_GOGOL.md` |
| Форма не шлёт заявки в Telegram | Проверь, что вместо `YOUR_BOT_TOKEN` / `YOUR_CHAT_ID` стоят твои значения и что ты написал(а) боту `/start` |
| После обновления скилл ведёт себя по-старому | Запусти установщик ещё раз — старые версии уйдут в `~/.claude/skills/_backup_<дата>/` |

## Приватность

Личные данные и материалы клиентов в репозиторий не входят. Здесь нет личных баз, переписок, таблиц, рабочих регламентов, ключей Figma-файлов клиентов, токенов и паролей. В шаблонах — только плейсхолдеры (`YOUR_BOT_TOKEN`, `example.com`, `<FIGMA_FILE_KEY>`).

Перед каждой публикацией `tools/validate.py` проверяет репозиторий на токены и ключи API, опасные настройки Claude Code, личные пути, e-mail, телефоны, номера карт и IBAN. Если нашёл в репозитории что-то личное — напиши в Issues.

Пример настроек статусной строки (`extras/claude-code/statusline/settings.example.json`) не меняет режим разрешений Claude Code. Не копируй к себе чужие `settings.json` целиком.

## Для авторов: проверка перед публикацией

```bash
python3 tools/validate.py                          # 0 ошибок — можно публиковать
HOME=$(mktemp -d) bash install.sh --no-deps --no-onboarding   # установка «как у нового человека»
```

`validate.py` проверяет каждый `skills/<имя>/SKILL.md` (frontmatter, `name` = имя папки, `description` до 1024 символов, дубли, ссылки на файлы скилла и на другие скиллы), а по всему репозиторию — Git LFS, файлы больше 50 МБ, секреты и личные данные, незаполненные шаблоны, пути песочницы claude.ai.

## Лицензии

Часть скиллов написана другими авторами и распространяется по их лицензиям — тексты лежат внутри папок скиллов, сводка в [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md):

- `design-taste-frontend`, `gpt-taste`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, `redesign-existing-projects`, `stitch-design-taste`, `full-output-enforcement`, `brandkit`, `image-to-code`, `imagegen-frontend-web`, `imagegen-frontend-mobile` — [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT;
- `emil-design-eng` — [emilkowalski/skills](https://github.com/emilkowalski/skills), MIT;
- `impeccable` — [pbakaus/impeccable](https://github.com/pbakaus/impeccable), Apache-2.0 (см. `LICENSE` и `NOTICE.md`; шаблоны отрендерены под Claude Code);
- `frontend-design` — [anthropics/skills](https://github.com/anthropics/skills), Apache-2.0 (`LICENSE.txt`);
- `svg-creator` — Apache-2.0 (`LICENSE` в папке скилла);
- `svg-animations` — источник не указан, лицензия не подтверждена.

Шрифты Manrope и JetBrains Mono — SIL Open Font License 1.1 (тексты лицензий рядом со шрифтами). Bebas Neue Cyrillic и Gogol в репозиторий не входят. Перед коммерческим проектом отдельно проверь лицензию любого шрифта и ассета.
