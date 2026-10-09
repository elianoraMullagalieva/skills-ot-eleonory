# Third-Party Notices — impeccable

Source: https://github.com/pbakaus/impeccable — Copyright 2025 Paul Bakaus, licensed under the Apache License 2.0 (see `LICENSE`).

## Based on Anthropic's frontend-design skill

Impeccable is based on the `frontend-design` skill by Anthropic
(https://github.com/anthropics/skills/tree/main/skills/frontend-design), licensed under the Apache License 2.0.

## Upstream notices

This project includes content derived from third-party work, used under the terms of its original license.

### Platform Design Skills

The `skill/reference/ios.md` and `skill/reference/android.md` platform reference files are distilled from ehmo's `platform-design-skills` (Apple Human Interface Guidelines and Material Design 3 rules), rewritten in Impeccable's voice.

**Original work:** https://github.com/ehmo/platform-design-skills
**Original license:** MIT
**Author:** ehmo

## Modifications in this repository

The source templates were rendered for Claude Code: placeholders such as `command_prefix`, `scripts_path`,
`ask_instruction`, `config_file`, `model`, `command_hint` and `available_commands` were replaced
with `/`, `~/.claude/skills/impeccable/scripts`, an AskUserQuestion instruction, `CLAUDE.md`, `Claude`
and the list of impeccable commands. No other changes.
