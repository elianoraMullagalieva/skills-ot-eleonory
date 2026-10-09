# Claude Code — инструкции и статусная строка

- `parallelnye-agenty.md` — как раздавать задачи нескольким агентам.
- `skill-v-pamyat-claude.md` — как работает память Claude Code и как просить её что-то запомнить.
- `statusline/` — статусная строка: папка, модель, заполненность контекста, лимиты 5 ч / 7 дней.

## Как подключить статусную строку

1. Нужна утилита `jq` (macOS: `brew install jq`, Ubuntu: `sudo apt install jq`).
2. Скопируй скрипт: `cp statusline/statusline-command.sh ~/.claude/statusline-command.sh`
3. Добавь в `~/.claude/settings.json` блок `statusLine` из `statusline/settings.example.json`
   (не заменяй весь файл — допиши только этот ключ).

В примере нет никаких настроек разрешений. Не включай `bypassPermissions` и
`skipDangerousModePermissionPrompt`, если не понимаешь последствий: Claude перестанет спрашивать
подтверждение перед командами.
