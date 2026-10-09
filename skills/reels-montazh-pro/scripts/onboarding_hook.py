#!/usr/bin/env python3
"""Добавить (или убрать) в ~/.claude/CLAUDE.md короткий блок «представься по ONBOARDING.md при первом сообщении».
Только с согласия пользователя: без --onboarding ничего не делает; без --yes спрашивает подтверждение.

  python3 onboarding_hook.py --onboarding            # добавить (спросит «да/нет»)
  python3 onboarding_hook.py --onboarding --yes      # добавить без вопроса (установщик, когда пользователь уже согласился)
  python3 onboarding_hook.py --onboarding --remove   # убрать блок
  --claude-md путь   другой файл (для проверки)"""
import argparse, os, re, sys

START, END = '<!-- reels-montazh-pro:onboarding -->', '<!-- /reels-montazh-pro:onboarding -->'
BLOCK = f"""{START}
## Приветствие при первом сообщении (скилл reels-montazh-pro)
При первом сообщении в новой сессии, если пользователь работает с видео/рилсами (или пишет «привет», «что ты умеешь»,
«как пользоваться»), — представься по ONBOARDING.md скилла reels-montazh-pro (~/.claude/skills/reels-montazh-pro/ONBOARDING.md):
коротко перечисли возможности и предложи 3 стартовые команды. Один раз за сессию.
{END}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--onboarding', action='store_true', help='явное согласие на изменение CLAUDE.md')
    ap.add_argument('--remove', action='store_true')
    ap.add_argument('--yes', action='store_true')
    ap.add_argument('--claude-md', default=os.path.join(os.path.expanduser('~'), '.claude', 'CLAUDE.md'))
    a = ap.parse_args()
    if not a.onboarding:
        print('Ничего не меняю: нужен флаг --onboarding (это согласие на правку ~/.claude/CLAUDE.md).')
        return
    p = os.path.abspath(a.claude_md)
    old = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    clean = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', old, flags=re.S)
    if a.remove:
        if clean == old:
            print('Блока нет — нечего убирать.')
            return
        open(p, 'w', encoding='utf-8').write(clean)
        print('✓ блок приветствия убран из', p)
        return
    if START in old:
        print('Блок уже есть в', p, '— не дублирую.')
        return
    if not a.yes:
        print(f'Добавлю в {p}:\n\n{BLOCK}')
        if input('Добавить? [да/нет] ').strip().lower() not in ('да', 'д', 'yes', 'y'):
            print('Отменено.')
            return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    sep = '' if not old or old.endswith('\n\n') else ('\n' if old.endswith('\n') else '\n\n')
    open(p, 'w', encoding='utf-8').write(old + sep + BLOCK)
    print('✓ блок приветствия добавлен в', p)


if __name__ == '__main__':
    main()
