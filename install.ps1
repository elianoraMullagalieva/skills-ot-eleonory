# Установка скиллов «Скиллы Эли Аноры» (skills-ot-eleonory) в Claude Code (Windows PowerShell 5.1+ / PowerShell 7).
#
# Запуск из папки репозитория:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1              # скиллы + зависимости
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -NoDeps      # только скиллы
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -DepsOnly    # только зависимости
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -Dest D:\my-skills
#
# Скрипт можно запускать повторно: одинаковые скиллы пропускаются, изменённые
# одноимённые копии уходят в %USERPROFILE%\.claude\skills\_backup_<дата>\.
# Если зависимость не ставится — скрипт предупреждает и продолжает.

[CmdletBinding()]
param(
    [switch]$NoDeps,
    [switch]$Onboarding,
    [switch]$NoOnboarding,
    [switch]$DepsOnly,
    [string]$Dest = ""
)

$ErrorActionPreference = "Continue"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Src = Join-Path $ScriptDir "skills"
if (-not $Dest) {
    if ($env:CLAUDE_SKILLS_DIR) { $Dest = $env:CLAUDE_SKILLS_DIR }
    else { $Dest = Join-Path (Join-Path $env:USERPROFILE ".claude") "skills" }
}
$Warnings = New-Object System.Collections.Generic.List[string]

function Say([string]$m)  { Write-Host $m }
function Ok([string]$m)   { Write-Host "[OK] $m" -ForegroundColor Green }
function Warn([string]$m) { Write-Host "[ВНИМАНИЕ] $m" -ForegroundColor Yellow; $script:Warnings.Add($m) }
function Fail([string]$m) { Write-Host "[ОШИБКА] $m" -ForegroundColor Red }
function Step([string]$m) { Write-Host ""; Write-Host "== $m ==" -ForegroundColor Cyan }
function Have([string]$c) { return [bool](Get-Command $c -ErrorAction SilentlyContinue) }

function Get-DirHash([string]$Path) {
    # Сравнение папок по содержимому (относительный путь + SHA256 каждого файла)
    $items = Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne ".DS_Store" -and $_.FullName -notmatch "__pycache__" } |
        Sort-Object FullName
    $sb = New-Object System.Text.StringBuilder
    foreach ($f in $items) {
        $rel = $f.FullName.Substring($Path.TrimEnd('\','/').Length)
        $h = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
        [void]$sb.AppendLine("$rel|$h")
    }
    return $sb.ToString()
}

# ------------------------------------------------------------------ скиллы
function Install-Skills {
    Step "Копирую скиллы в $Dest"
    if (-not (Test-Path -LiteralPath $Src)) {
        Fail "Не найдена папка skills рядом со скриптом ($Src). Запускай install.ps1 из корня скачанного репозитория."
        exit 1
    }
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $backup = Join-Path $Dest ("_backup_" + (Get-Date -Format "yyyyMMdd-HHmmss"))
    $copied = 0; $same = 0; $backed = 0

    foreach ($dir in Get-ChildItem -LiteralPath $Src -Directory | Sort-Object Name) {
        $name = $dir.Name
        if ($name.StartsWith("_") -or $name.StartsWith(".")) { continue }
        if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName "SKILL.md"))) {
            Warn "Пропускаю ${name}: в папке нет SKILL.md"
            continue
        }
        $target = Join-Path $Dest $name
        if (Test-Path -LiteralPath $target) {
            if ((Get-DirHash $dir.FullName) -eq (Get-DirHash $target)) {
                Say "  = $name (уже установлен, без изменений)"
                $same++
                continue
            }
            New-Item -ItemType Directory -Force -Path $backup | Out-Null
            try {
                Move-Item -LiteralPath $target -Destination (Join-Path $backup $name) -ErrorAction Stop
                Say "  ~ ${name}: старая версия сохранена в $backup\$name"
                $backed++
            } catch {
                Warn "Не смог убрать в бэкап $target — пропускаю $name ($($_.Exception.Message))"
                continue
            }
        }
        try {
            Copy-Item -LiteralPath $dir.FullName -Destination $target -Recurse -Force -ErrorAction Stop
            Get-ChildItem -LiteralPath $target -Recurse -Force -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -eq ".DS_Store" -or $_.Name -eq "__pycache__" } |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Say "  + $name"
            $copied++
        } catch {
            Warn "Не удалось скопировать ${name}: $($_.Exception.Message)"
        }
    }
    Ok "Скопировано: $copied, без изменений: $same, в бэкап: $backed"
}

# ------------------------------------------------------------------ зависимости
function Find-Python {
    foreach ($cand in @(@("py", "-3"), @("python"), @("python3"))) {
        $exe = $cand[0]
        if (-not (Have $exe)) { continue }
        $pre = @()
        if ($cand.Length -gt 1) { $pre = $cand[1..($cand.Length - 1)] }
        try {
            & $exe @pre -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>$null
            if ($LASTEXITCODE -eq 0) { return ,$cand }
        } catch {}
    }
    return $null
}

function Invoke-Py([string[]]$PyArgs) {
    $exe = $script:Py[0]
    $pre = @()
    if ($script:Py.Length -gt 1) { $pre = $script:Py[1..($script:Py.Length - 1)] }
    & $exe @pre @PyArgs | Out-Host
    return ($LASTEXITCODE -eq 0)
}

function Pip-Install([string[]]$Pkgs) {
    $log = Join-Path $env:TEMP "skills-pip.log"
    $exe = $script:Py[0]
    $pre = @()
    if ($script:Py.Length -gt 1) { $pre = $script:Py[1..($script:Py.Length - 1)] }
    & $exe @pre -m pip install --user --upgrade @Pkgs *> $log
    return ($LASTEXITCODE -eq 0)
}

function Install-FFmpeg {
    if (Have "ffmpeg") { Ok "ffmpeg уже есть"; return }
    Say "Ставлю ffmpeg через winget…"
    if (Have "winget") {
        winget install --id Gyan.FFmpeg -e --silent --accept-source-agreements --accept-package-agreements
        if ($LASTEXITCODE -eq 0) {
            Ok "ffmpeg установлен (если команда ffmpeg не находится — открой новое окно терминала)"
            return
        }
    }
    Warn "ffmpeg не установился. Поставь вручную: winget install Gyan.FFmpeg (или скачай с https://www.gyan.dev/ffmpeg/builds/ и добавь bin в PATH)."
}

function Install-PythonDeps {
    $script:Py = Find-Python
    if (-not $script:Py) {
        Warn "Не найден Python 3.8+. Поставь его: winget install Python.Python.3.12 (или с https://www.python.org, галочка «Add to PATH»), затем запусти install.ps1 -DepsOnly"
        return
    }
    Ok ("Python: " + ($script:Py -join " "))
    if (-not (Invoke-Py @("-m", "pip", "--version"))) {
        Invoke-Py @("-m", "ensurepip", "--user") | Out-Null
    }

    Say "Ставлю playwright и pillow (рендер HTML → видео, снимки сцен)…"
    if (Pip-Install @("playwright", "pillow")) {
        Ok "playwright и pillow установлены"
        Say "Скачиваю Chromium для playwright (~150 МБ)…"
        if (Invoke-Py @("-m", "playwright", "install", "chromium")) { Ok "Chromium для playwright готов" }
        else { Warn "Chromium не скачался. Повтори: python -m playwright install chromium" }
    } else {
        Warn "playwright не установился (лог: $env:TEMP\skills-pip.log). Повтори: python -m pip install --user playwright pillow"
    }

    Say "Ставлю faster-whisper (пословные таймкоды речи)…"
    if (Pip-Install @("faster-whisper")) { Ok "faster-whisper установлен" }
    else { Warn "faster-whisper не установился (лог: $env:TEMP\skills-pip.log). Повтори: python -m pip install --user faster-whisper" }

    Say "cairosvg (превью для svg-creator) на Windows требует GTK3 runtime — ставлю пакет, но превью может не заработать…"
    if (-not (Pip-Install @("cairosvg"))) { Warn "cairosvg не установился — svg-creator не сможет делать PNG-превью." }
}

function Install-Deps {
    Step "Зависимости для монтажа и рендера"
    Install-FFmpeg
    Install-PythonDeps
}

# ------------------------------------------------------------------ проверка
function Test-Install {
    Step "Проверка установки"
    $bad = 0; $n = 0
    foreach ($dir in Get-ChildItem -LiteralPath $Src -Directory | Sort-Object Name) {
        $name = $dir.Name
        if ($name.StartsWith("_") -or $name.StartsWith(".")) { continue }
        if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName "SKILL.md"))) { continue }
        $n++
        $md = Join-Path (Join-Path $Dest $name) "SKILL.md"
        $okFile = $false
        if (Test-Path -LiteralPath $md) {
            $first = Get-Content -LiteralPath $md -TotalCount 1 -Encoding UTF8
            if ($first -and $first.TrimStart([char]0xFEFF).StartsWith("---")) { $okFile = $true }
        }
        if ($okFile) { Write-Host "  [OK] $name" -ForegroundColor Green }
        else { Write-Host "  [НЕТ] $name — нет $md" -ForegroundColor Red; $bad++ }
    }
    if ($bad -eq 0) { Ok "Все $n скиллов на месте: $Dest\<имя>\SKILL.md" }
    else { Fail "$bad из $n скиллов не установились — смотри сообщения выше" }
    return $bad
}

Write-Host "Скиллы Эли Аноры — установка скиллов Claude Code" -ForegroundColor White
$rc = 0
if (-not $DepsOnly) { Install-Skills }
if (-not $NoDeps) { Install-Deps } else { Say ""; Say "Зависимости пропущены (-NoDeps). Поставить позже: .\install.ps1 -DepsOnly" }

# Приветствие помощника при первом сообщении (правка ~/.claude/CLAUDE.md — только с согласия)
$hook = Join-Path $Dest "reels-montazh-pro\scripts\onboarding_hook.py"
if ((Test-Path $hook) -and -not $NoOnboarding) {
    $doOnb = $Onboarding.IsPresent
    if (-not $doOnb) {
        $ans = Read-Host "Включить приветствие: при первом сообщении помощник расскажет, что умеет (5 строк в ~/.claude/CLAUDE.md)? [Д/н]"
        $doOnb = -not ($ans -match '^[НнNn]')
    }
    if ($doOnb) { & python $hook --onboarding --yes; if ($LASTEXITCODE -eq 0) { Say "[OK] Приветствие включено" } else { Say "[ВНИМАНИЕ] Не удалось включить приветствие: python $hook --onboarding" } }
}
if (-not $DepsOnly) { if ((Test-Install) -ne 0) { $rc = 1 } }

if ($Warnings.Count -gt 0) {
    Step "Предупреждения ($($Warnings.Count))"
    foreach ($w in $Warnings) { Say "  - $w" }
}
Say ""
if (-not $DepsOnly) {
    Say "Готово. Перезапусти Claude Code (или открой новую сессию) — скиллы подхватятся автоматически."
    Say "Проверка в Claude Code: спроси «какие у тебя есть скиллы?» или набери /skills."
}
exit $rc
