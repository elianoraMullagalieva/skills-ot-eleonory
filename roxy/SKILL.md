---
name: roxy
description: Всё необходимое для генерации новых сцен с роботом Рокси в Nano Banana (Higgsfield). Используй когда нужно написать промпт для кадра А или Б с Рокси — в любой локации, любом действии. Содержит: описание персонажа, UUID, описание всех готовых локаций, чек-лист промпта, шаблоны кадров А→Б, таблицу артефактов и их лечение. Загружай эту папку целиком перед написанием любого промпта с Рокси.
---

# Рокси — полный гид по генерации сцен

---

## Персонаж

**Имя:** Roxy  
**UUID в Higgsfield:** `<<<7409f64f-b662-4a73-bddf-f9cabac34e7d>>>`  
**Всегда первая строка промпта:** `Use <<<7409f64f-b662-4a73-bddf-f9cabac34e7d>>> Roxy exactly as provided.`

### Внешность (для справки, не вставлять в промпт)
- Робот-гуманоид, матово-тёмный корпус антрацит/тёмно-серый
- Одежда: длинное кимоно-халат тёмно-серого цвета, пояс-оби, свободные рукава
- Надпись "Roxy" на груди (левая сторона халата)
- Голова: гладкая овальная, без носа и ушей, иероглиф-символ на лбу
- Лицо: LED-глаза (синяя дуга), LED-рот (синяя дуга-улыбка)
- Руки: механические, тёмные, с артикулированными пальцами
- Ноги: минималистичные, тёмные, без обуви

### LED-выражения (только через существующие световые линии)
- Нейтральное: глаза-дуги ровные, рот слегка изогнут
- Улыбка: `LED mouth indicator shows a gentle upward arc at both ends`
- Озабоченное: `LED eyes slightly angled inward, mouth arc flat`

---

## Правило персонажа в промпте

**Описание черт лица НЕ вставлять** — UUID уже содержит всю информацию. Любое описание черт конкурирует с референсом и ломает лицо.

Единственная фраза для сохранения:
> `Keep the exact same face, identity and design as the reference. Do not alter any facial features, proportions, or materials.`

При многошаговой генерации (A→B→C) — повторять эту фразу **в каждом промпте**.

---

## Готовые локации

### 🍳 Кухня
**Статус:** отработана, есть готовые кадры A и B  
**Стиль:** современный минималистичный, тёмные матовые фасады, бетонный пол, большое окно слева с дневным светом  
**Ракурс:** продольный коридорный кадр, камера смотрит вглубь кухни, холодильник слева у окна, стойка справа  
**Референс для локации:** Image #2 (Рокси входит с продуктами) и Image #4 (Рокси у раковины)  
**Зафиксированные объекты:**
- Холодильник — у левой стены рядом с окном, дверь открывается влево (ручка справа)
- Раковина — в левой части стойки, рядом с холодильником
- Окно — слева, дневной свет падает справа налево
- Проход в другую комнату — в глубине кадра

**Якорная фраза:**
> `Same kitchen from the reference image — same camera angle, same lighting from the left window, same dark matte cabinets and concrete floor.`

---

### 🛏 Спальня
**Статус:** отработана, есть кадры A (мятая кровать) и B (в процессе застилания)  
**Стиль:** тёмный премиум-минимализм, тёмная фактурная стена, тёплая LED-подсветка за изголовьем  
**Ракурс:** фронтальный, кровать по центру-левее, Рокси справа в трети кадра  
**Референс:** Image #6 (Рокси стоит у застеленной кровати) и Image #8 (начало застилания)  
**Зафиксированные объекты:**
- Кровать — тёмно-серое льняное покрывало, два серых квадратных подарка
- Прикроватная тумба слева — низкая, тёмная, ваза с ветками, книга
- Регулируемый торшер слева — металл, тонкая ножка
- Тёплая LED-лента за изголовьем — горизонтальная, amber-тон
- Пол — светлый дуб

**Якорная фраза:**
> `Same bedroom from the reference image — same dark textured accent wall, same warm LED strip behind the headboard, same floor lamp on the left, same light oak floor, same camera angle.`

---

### 🧸 Детская (запланирована, кадры не готовы)
**Стиль:** тот же дом, тёплые угольные стены, светлый дуб, тёплый ambient  
**Планируемые объекты:** деревянные игрушки (не пластик), мягкий мишка, кубики, открытая книга  
**Корзина:** тёмная плетёная, для уборки игрушек

---

## Сюжет — полная раскадровка

| # | Локация | Кадр A | Кадр B | Статус |
|---|---|---|---|---|
| 1 | Кухня | Рокси входит с продуктами | Ставит пакет на стойку | A готов ✅ |
| 2 | Кухня | Пакет на стойке | Открывает холодильник, кладёт овощи | — |
| 3 | Кухня | Овощи у раковины | Рокси моет овощи | B готов ✅ |
| 4 | Кухня | Рокси у раковины | Чистая раковина, овощи на полотенце | — |
| 5 | Спальня | Мятая кровать | Рокси начинает застилать | A готов ✅ |
| 6 | Спальня | В процессе застилания | Кровать идеально застелена, Рокси улыбается | нужен новый B |
| 7 | Детская | Игрушки разбросаны | Рокси собирает в корзину | — |
| 8 | Детская | Рокси собирает | Детская убрана, Рокси у двери | — |

---

## Чек-лист перед написанием промпта

**5 вопросов:**
- [ ] Что меняется? (максимум 1-3 объекта)
- [ ] Что НЕ меняется? (не упоминать в промпте вообще)
- [ ] Какое физическое состояние объекта в финале? (материал, форма, текстура — не "идеально")
- [ ] Есть ли слово, которое встречается 3+ раз? (уберёт — нарисует дважды)
- [ ] Есть ли запреты NO / NOT / must NOT? (переформулировать позитивно)

---

## Чек-лист написания промпта

**Структура — строго в этом порядке:**
1. Персонаж (одна строка с UUID)
2. Локация (одна строка — якорная фраза из раздела выше)
3. Действие Рокси (где стоит, что делает, как держит руки)
4. Изменяемый объект (физика финального состояния)
5. Стиль съёмки (одна строка)

**Правила:**
- [ ] UUID — первая строка
- [ ] Локация — одно предложение, якорная фраза
- [ ] Неизменяемые объекты — **молчание** (не упоминать = сохранить)
- [ ] Объект упомянут **один раз** в действии
- [ ] Нет эмодзи, нет CAPS LOCK, нет разделов CONSTRAINTS
- [ ] Нет негативов: вместо "no handles" — просто не писать про ручки
- [ ] Длина: **5-8 предложений максимум**
- [ ] Читается как **режиссёрская ремарка**, не технический контракт

---

## Физические описания объектов (готовые формулировки)

### Овощи (не пластиковые)
> `hand-sized, organic surface with natural color variation, slight waxy sheen, small natural green stem, visible water droplets`

### Кровать — идеально застелена
> `blanket flat and taut across the entire mattress, no wrinkles, no creases, fabric pulled smooth to all four corners. Both pillows upright against the headboard, corners sharp, fully filled, no compression dents, pillowcase surface smooth`

### Кровать — мятая (начальный кадр)
> `blanket visibly crumpled with natural folds and disorder, pillows dented and casually placed, bed clearly unmade`

### Холодильник открыт
> `door hinged on the left side of the unit, handle on the right edge, open approximately 60 degrees, warm interior light visible, clean dark shelves`

### Движение (живое, не позирование)
> `caught mid-step`, `casual effortless movement`, `documentary style, not posing`, `natural working posture, slight forward lean`

### Руки с предметом
> `both articulated hands gripping [объект] naturally, fingers wrapped around it, slight pressure visible in finger joints`

### LED-улыбка
> `LED mouth indicator shows a gentle upward arc at both ends — subtle smile using only the existing light lines`

---

## Диагностика артефактов

| Проблема | Причина | Лечение |
|---|---|---|
| Лишние ручки на двери | "handle" в запрете → модель его рисует | Не упоминать ручки вообще |
| Дублируется раковина / объект | Объект упомянут 4+ раз | Упомянуть один раз, в действии |
| Кровать осталась мятой | "perfectly made" — абстракция | Описать физику: flat, taut, no creases |
| Овощи пластиковые | Нет описания материала | Добавить: organic surface, waxy sheen |
| Кухня перестроилась | Структура с CONSTRAINTS → список объектов для рисования | Убрать структуру, писать прозой |
| Персонаж изменился | UUID не первый, или описание черт конкурирует | UUID в первую строку, черты лица не описывать |
| Глаз покосился | Несколько ракурсов в одном кадре | Каждый ракурс — отдельный промпт |
| Дорисовались детали окружения | Слишком много запретов → модель «видит» запрещённые объекты | Убрать все NOT/NO, молчание = сохранение |

---

## Минимальный рабочий шаблон (5 предложений)

```
Use <<<7409f64f-b662-4a73-bddf-f9cabac34e7d>>> Roxy exactly as provided.

[Якорная фраза локации из раздела выше.]

Roxy [где стоит], [что делает], [как держит руки / поза].

[Изменяемый объект]: [физическое описание — материал, форма, размер, текстура].

Documentary photography, [объектив], [свет].
```

### Пример — кухня, мытьё овощей

```
Use <<<7409f64f-b662-4a73-bddf-f9cabac34e7d>>> Roxy exactly as provided.

Same kitchen from the reference image — same camera angle, same lighting from the left window, same dark matte cabinets and concrete floor.

Roxy stands at the sink on the left side, facing it, both articulated hands holding vegetables under running water, slight forward lean in natural working posture.

In her hands: one red bell pepper and one yellow bell pepper — hand-sized, organic shape, natural color variation, faint wet sheen, small green stems. On the counter beside her: one cabbage and one tomato, already washed, placed casually.

Documentary photography, 35mm, natural window light from the left.
```

### Пример — спальня, застеленная кровать

```
Use <<<7409f64f-b662-4a73-bddf-f9cabac34e7d>>> Roxy exactly as provided.

Same bedroom from the reference image — same dark textured accent wall, same warm LED strip behind the headboard, same floor lamp on the left, same light oak floor, same camera angle.

Roxy stands at the foot of the bed, facing the camera, both hands relaxed at her sides, task completed.

The blanket lies flat and taut across the entire mattress with no wrinkles or creases, fabric pulled smooth to all four corners. Both pillows stand upright against the headboard, corners sharp, fully filled, pillowcase surface smooth with no compression marks.

Documentary photography, same lens and lighting as reference image.
```

---

## Важные выводы (из опыта генераций)

1. **Молчание = сохранение.** Не упоминай объект — он останется как в оригинале.
2. **Запреты рисуют.** `NO handles` → модель видит слово "handles" и рисует их.
3. **Абстракции не работают.** "Perfectly made" → описывай физику ткани.
4. **Один объект — одно упоминание.** Дважды упомянул → нарисует дважды.
5. **Структура с CONSTRAINTS ломает кухню.** Промпт — режиссёрская ремарка, не контракт.
6. **При многошаговой генерации** — каждый раз заново подавать UUID и напоминать про сохранение лица.
7. **Каждый ракурс — отдельный промпт.** Несколько ракурсов в одном → артефакты.
