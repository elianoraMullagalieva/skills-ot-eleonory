---
name: kling-video
description: Промпт-инженерия для Kling 3.0 — полный гайд по созданию видео, оживлению фото, настройке камеры, стилей и аудио с готовыми шаблонами.
---

# Kling 3.0 — промпт-инженерия для видео

> Источники: Habr (StudyAI, ЦНИС), atlabs.ai (×2), kling3-ai.com, kling3.online, kod.ru, vc.ru — синтез 9 статей.

---

## Главный принцип

**Думайте как режиссёр, а не как фотограф.**

Видео требует понимания временной структуры, движения камеры и кинематографического языка. Статичное красивое описание без указания движения даст статичный скучный кадр.

Ключевая мысль из источников: *"закройте глаза и представьте себя за монитором, дающим указания оператору и актёрам — именно это нужно Kling 3.0."*

Модель обучена на кинематографических произведениях, поэтому профессиональная терминология кино работает значительно лучше, чем бытовые описания.

---

## Формула промпта (универсальная)

### Базовая (для новичков)
```
[Объект/персонаж] + [Окружение] + [Действие] + [Камера] + [Стиль]
```
Пример: *"Крупный план, кот пьёт молоко, утренний свет на кухне, медленный dolly push-in, кинематографично"*

### Расширенная SCALE-формула (рекомендуемая)
```
Shot → Character → Action → Lighting & Location → Extra (Audio/Style)
```

| Слой | Слабо | Сильно |
|------|-------|--------|
| **Scene** | "пляж" | "тропический берег на golden hour, мокрый песок отражает небо" |
| **Subject** | "женщина" | "молодая женщина в белом платье, босая, чёрные волосы развеваются" |
| **Action** | "она идёт" | "медленно идёт по линии волн, смотрит на пену, поднимает взгляд" |
| **Camera** | "камера следует за ней" | "медленный tracking shot сзади, постепенный dolly push-in" |
| **Audio** | "хорошая музыка" | "волны, крики чаек, мягкий ветер" |

### Multi-shot (для нарратива)
```
Shot 1 (0–3 сек): [тип + движение + сцена]
Shot 2 (3–6 сек): [тип + движение + сцена]
Shot 3 (6–9 сек): [тип + движение + сцена]
```
Оптимальный темп: 4–6 кадров за 10–15 секунд. Максимум — 6 кадров в одном поколении.

### Диалог (lip-sync)
```
[Персонаж А, тон голоса]: "Реплика"
Immediately, [Персонаж Б, тон]: "Ответ"
```
Всегда используйте конкретные имена и описание голоса, а не местоимения.

### Звуковые эффекты
```
SFX: [описание звука]
```

### Negative prompt
```
[Negative: morphing, distorted face, extra limbs, low resolution, flickering, warped hands, glitch artifacts]
```

---

## Движения камеры (полный список с описанием)

### Линейные движения
| Термин | Описание |
|--------|----------|
| **Dolly push-in** | Плавный наезд вперёд к объекту |
| **Dolly pull-out** | Отъезд камеры назад от объекта |
| **Tracking shot** | Камера движется параллельно объекту, сбоку |
| **Crane shot** | Подъём камеры вверх, открывает окружение |

### Вращательные
| Термин | Описание |
|--------|----------|
| **Slow orbit** | Плавное вращение вокруг объекта (360°) |
| **Whip-pan** | Быстрый горизонтальный свип, используется для перехода |
| **Crash zoom** | Резкое изменение фокусного расстояния для шока/акцента |
| **Dutch angle** | Наклонный кадр для создания напряжения |

### Специальные
| Термин | Описание |
|--------|----------|
| **Handheld / shoulder-cam** | Органичное лёгкое покачивание, ощущение реальности |
| **Static tripod** | Полная неподвижность, стабильность |
| **FPV drone** | Вид от первого лица, стремительное движение |
| **Rack focus** | Смена фокуса между передним и задним планом |
| **Speed ramp** | Ускорение с 40% до 100% интенсивности |
| **Tilt up / tilt down** | Вертикальный поворот камеры вверх/вниз |
| **Pan** | Горизонтальный поворот на месте |

### Эффекты кадра
| Термин | Описание |
|--------|----------|
| **Shallow focus / depth of field** | Малая глубина резкости, f/1.8 — f/2.8 |
| **Anamorphic lens flare** | Горизонтальные блики от анаморфного объектива |
| **Rack focus** | Перефокусировка между слоями сцены |

### Практическое правило
- Большие скачки между кадрами (широкий → крупный план) работают лучше, чем два похожих средних плана.
- Наречия (slowly, rapidly, gradually) работают как коэффициенты интенсивности движения.

---

## Стили и настроение

### Кинематографические эстетики
| Референс | Как прописывать |
|----------|----------------|
| Плёнка 35mm | `shot on 35mm film with shallow focus and glowing bokeh` |
| VHS / ретро | `VHS camcorder aesthetic with heavy grain and chromatic aberration` |
| Super 8 | `Super 8 film look with warm vintage tones` |
| Цифровое кино | `digital cinema with anamorphic lens flare` |
| Аниме | `Studio Ghibli style` / `Sailor Moon aesthetic` |
| Документальное | `nature documentary style` / `handheld documentary` |
| Коммерческое | `product photography, beauty lighting, slow elegant moves` |

### Освещение (конкретные источники)
- `golden hour` — тёплый закатный свет
- `volumetric god rays` — объёмные лучи сквозь атмосферу
- `neon signs` — неоновые вывески (городской ночной)
- `candlelight` — свеча, тёплый мерцающий
- `LED panels` — холодный промышленный
- `three-point lighting` — ключ 45° слева, заполняющий справа, контровый на волосах
- `spotlight` — точечный акцент

### Тактильные детали (дают реализм)
- `grain, lens flares, reflections, fabric sheen`
- `condensation, smoke, sweat, rain beading, visible breath`
- `steam rising, light flickering, drifting dust`
- `breathing, blinking, subtle hand movements, hair in wind`

### Атмосферные эффекты
- `particles, bioluminescence, mist, ground fog`
- `volumetric` — для дыма, тумана (дополняется любым эффектом)

---

## Параметры (длительность, соотношение сторон, CFG)

### Длительность
| Значение | Когда использовать |
|----------|-------------------|
| **5 сек** | Продуктовая съёмка, ASMR, простая анимация фото |
| **10 сек** | Короткий нарратив, 2–3 shot |
| **15 сек** | Полноценная сцена, до 6 shots, диалог |

### Соотношение сторон
| Формат | Платформа |
|--------|-----------|
| **16:9** | YouTube, кино, широкий экран |
| **9:16** | TikTok, Reels, вертикальное видео |
| **1:1** | Instagram, продукты |

### Качество рендера
- **Standard mode** — быстро, для тестирования
- **Professional mode** — максимальное качество, используйте для финала

### Разрешение и FPS
- До 4K (1080p по умолчанию в большинстве режимов)
- До 60 FPS

### Совет по workflow
1. Сначала генерируйте в Standard для проверки концепции
2. Финал рендерите в Professional
3. Собирайте длинные видео из нескольких 5–10 секундных сегментов

---

## Image-to-video (оживление фото)

### Принцип работы
Загружаете фото как стартовый кадр → описываете **изменения и движение** → нейросеть оживляет.

**Ключевое правило:** НЕ описывайте то, что уже видно на фото. Фокусируйтесь на том, как сцена **развивается** — движение, атмосфера, динамика.

### Структура промпта для I2V
```
[Foreground: действие] + [Background: static] + [Camera] + [Physical details]
```

Разделение переднего плана (динамика) и заднего (статика) помогает DiT-архитектуре корректно обработать векторы движения.

### Требования к исходному изображению
- Минимум **2048px** по длинной стороне
- Загружайте в целевом соотношении сторон (16:9 или 9:16)
- Старые фото предварительно **апскейлируйте**
- **Не используйте** фото с обрезанными конечностями — модель попытается их достроить с артефактами
- Избегайте кадрированных частей тела на краях

### Открывающая фраза для сохранения персонажа
```
Strictly preserve the facial features and clothing from the original photo.
```

### Режим двух кадров (Start/End frame)
Загрузите два логически связанных кадра — начальный и конечный. Kling просчитывает плавный переход между ними. Работает как морфинг-анимация с физически корректной интерполяцией.

### Уровни движения
| Интенсивность | Ключевые слова |
|---------------|----------------|
| Минимальная | `subtle, slow-motion, natural blinking, gentle` |
| Средняя | `moderate movement, soft sway, gradual shift` |
| Активная | `dynamic movement, fast-paced, intense, rapid` |

### Пример для портрета
```
Strictly preserve the facial features and clothing from the original photo.
Foreground: gentle smile appears, eyes blink naturally, hair sways slightly in wind.
Background: static soft-focus bokeh.
Camera: slow subtle push-in toward face.
Add: realistic skin texture with visible pores, consistent lighting.
[Negative: morphing, distorted face, extra limbs, flickering]
```

### Сравнение с конкурентами (из atlabs.ai)
- Kling 3.0 vs **Runway Gen-3**: меньше замыливает текстуру кожи
- Kling 3.0 vs **Luma**: на ~30% реже деформирует конечности
- Kling 3.0 vs **Sora**: лучше обрабатывает источники света и пересчитывает блики
- Kling 3.0 vs **Kling 2.x**: нативное аудио с lip-sync, до 6 multi-shot кадров, консистентность персонажей

---

## Character consistency (сохранение персонажа между кадрами)

### Основные стратегии

**1. Точные дескрипторы**
Определите персонажа один раз и используйте дословно во всех shots:
```
"the woman in red coat with silver earrings"  — всегда именно так, не "she" или "the woman"
```

**2. Ранее введённые метки**
Вводите персонажа в Shot 1 с полным описанием, в следующих shots используйте ту же метку:
```
Shot 1: [Anna, 30s, red blazer, short blonde hair] enters the office...
Shot 2: Close-up of Anna's face as she reads the letter...
Shot 3: Anna walks to the window, the red blazer catching light...
```

**3. Image-to-video как якорь**
Для максимальной консистентности используйте один и тот же стартовый кадр для всех сегментов с персонажем.

**4. Motion Control режим**
Загружаете видео-референс движения → Kling переносит это движение на вашего персонажа.
- Промпт для Motion Control НЕ описывает движения — только внешность персонажа и окружение
- Модель берёт кинематику из видео-источника

### Важные правила
- Избегайте местоимений "он", "она", "они" в multi-shot промптах
- Описывайте отличительные детали: одежда, цвет волос, аксессуары, особенности
- Чем более специфично — тем стабильнее результат

---

## Антипаттерны

### Промпт-ошибки

| Ошибка | Плохо | Хорошо |
|--------|-------|--------|
| **Пустые прилагательные** | `cinematic, beautiful, 4K, masterpiece` | `35mm film с anamorphic lens flare, f/2.0` |
| **Нет описания камеры** | *(движение не указано)* | `slow dolly push-in, handheld shoulder-cam` |
| **Наложенные действия** | `она бежит, смеётся, машет, волосы развеваются` | `начинает бегать → смех срывается → поворачивается и машет` |
| **Местоимения в диалоге** | `он говорит... потом она отвечает` | `[Морис, грубый баритон]: "..."` |
| **I2V: описание видимого** | описывать то, что уже на фото | описывать только **изменения** |
| **Абстрактный запрос** | `красивое видео` | конкретная сцена с действием и камерой |
| **Слишком много за раз** | 10 действий в 5 секунд | 1–2 действия на кадр |

### Технические ограничения Kling 3.0
- **Сложная моторика**: набор текста на клавиатуре, игра на гитаре пальцами — ненадёжно
- **Длинный текст в кадре**: более 3 слов — плохо читается; используйте короткие слова с пометкой `четкая гравированная надпись`
- **Множество мелких движущихся объектов** (толпа, стая птиц) — возможны артефакты
- **Резкие смены физики** в одном промпте (вода → огонь → ткань) — нежелательно
- **Синхронизация диалога на русском** — менее точна, чем на английском
- **Быстрые движения** → анатомические артефакты конечностей

### Что работает плохо вне зависимости от промпта
- Зима→лето переход без логической связи
- Перекрытие/наложение частей тела без чёткого референса
- Обрезанные конечности на входном фото (I2V)

---

## Диагностика артефактов

| Симптом | Причина | Решение в промпте |
|---------|---------|-------------------|
| Нереалистичное лицо | Недостаточно деталей | `photorealistic skin texture, natural facial expressions, visible pores` |
| Дёрганые движения | Несколько действий одновременно | Одно действие за кадр + `smooth movement, gradual` |
| Деформированные руки | Сложная моторика | Упростить движения рук, добавить в negative prompt `warped hands, distorted fingers` |
| Мерцание текстур | Нет стабилизации | `stable textures, consistent lighting, no flicker` в negative prompt |
| Несовпадение озвучки | Нечёткие реплики | Короткие реплики, чёткие метки персонажей, `[Name, voice tone]: "text"` |
| Нечитаемый текст | Длинная надпись | Максимум 1–3 слова, `sharp legible text, clean typography` |
| Фон двигается в I2V | Нет разделения планов | `[Foreground: action] + [Background: static soft focus]` |
| Артефакты при переходе | Слишком похожие shots | Контрастируйте: wide → close-up, а не medium → medium |

---

## Готовые шаблоны

### Шаблон 1: Кинематографический нарратив (multi-shot)
*Источник: kling3-ai.com*
```
Shot 1: Wide aerial drone shot descending toward a foggy mountain
village at dawn. Chimney smoke, river through valley. Muted earth tones.

Shot 2: Medium tracking shot following an old man with wooden cane
on cobblestone path. Weathered brown jacket, flat cap. Morning dew.

Shot 3: Close-up of weathered hands pushing open a heavy wooden door.
Peeling paint, iron hinges. Camera follows inside.

Shot 4: Interior medium shot. Amber firelight on cluttered workshop.
He sits, picks up a half-finished wooden carving, examines it.

Shot 5: Macro of hands carving with small knife. Wood shavings curl.
Firelight on detailed bird carving. Crackling fire, faint wind.
```

### Шаблон 2: Диалоговая сцена с lip-sync
*Источник: kling3-ai.com*
```
Medium shot, warm coffee shop with exposed brick. Two women at a
small wooden table.

[Anna, cheerful mid-range voice]: "I finally quit my job yesterday."
She leans back with relieved smile, wrapping hands around her mug.

[Maya, surprised, slightly high-pitched]: "Wait, seriously?"
Maya sets down her cup, leans forward. Camera slowly pushes in.
Ambient cafe noise, soft jazz, ceramic clinking.
```

### Шаблон 3: Высокоскоростное действие
*Источник: kling3-ai.com*
```
Dynamic FPV drone shot through narrow urban alley at night. Parkour
runner in black gear sprints, vaults dumpsters, slides under
scaffolding. Sparks from hand dragging metal railing. Camera barrel
rolls as he leaps between rooftops. Neon blur, rain on lens. Motion
blur, high contrast. Heavy breathing, concrete impacts, distant sirens.
```

### Шаблон 4: Макро ASMR / еда
*Источник: kling3-ai.com*
```
Extreme macro, shallow depth of field. Hand slowly drizzles warm
honey over golden pancakes. Honey catches morning window light,
forming glossy ribbon pooling between layers. Steam rises. Static
tripod, then slow push-in as butter melts and slides. Crispy sizzle,
viscous drip, soft plate clink. Macro 100mm lens, warm grade.
```

### Шаблон 5: Демонстрация продукта / реклама
*Источник: kling3-ai.com*
```
Slow orbit around matte black wireless headphones floating against
dark gradient background. Subtle rim lighting in cool white. 180-degree
rotation revealing cushion detail and brushed metal. Camera pulls back
as volumetric light rays sweep frame. Minimal, premium. Clean electronic
ambient, soft bass pulse.
```

### Шаблон 6: Уличный документализм / атмосфера
*Источник: kling3-ai.com*
```
Handheld shoulder-cam following street musician playing saxophone on
rainy Paris sidewalk at dusk. Worn leather jacket, fedora tilted low.
Camera sways naturally, rack-focusing between musician and blurred
pedestrians with umbrellas. Wet cobblestones reflect warm streetlamp
and blue twilight. 35mm film grain. Raw saxophone, rain on pavement,
distant cafe chatter.
```

### Шаблон 7: Sci-Fi / киберпанк
*Источник: kling3-ai.com*
```
Slow tracking through massive cyberpunk marketplace. Holographic signs
in Mandarin and English. Woman with chrome cybernetic arm browses stall
of glowing circuit boards. Ground fog, magenta and cyan neon on metallic
implants. She picks up component, inspects, nods to vendor. Camera cranes
up revealing megastructure. Synth drone, electronic chatter, servo whirr.
```

### Шаблон 8: Оживление портретного фото (I2V)
*Синтез: kod.ru + atlabs.ai*
```
Strictly preserve the facial features and clothing from the original photo.
Foreground: gentle natural smile appears slowly, eyes blink naturally,
hair sways subtly in a light breeze.
Background: static soft bokeh, no movement.
Camera: slow gentle dolly push-in toward the face.
Lighting: consistent warm key light from the left, natural skin texture,
visible pores.
[Negative: morphing, distorted face, extra limbs, flickering, shaky camera]
```

### Шаблон 9: Природный ландшафт / тайм-лапс стиль
*Источник: kling3-ai.com*
```
Timelapse-style wide shot of Tuscan hills at golden hour. Cypress shadows
across wheat fields. Clouds drift, light shifts gold to amber. Dirt road
winds through landscape. Slow dolly track with parallax depth. Transition
to normal speed as birds lift from distant tree line. Wind through grass,
distant church bell, birdsong.
```

### Шаблон 10: Motion Control (подмена персонажа)
*Источник: kling3-ai.com*
```
Professional female news anchor in navy blazer and pearl earrings,
natural makeup, warm skin. Modern broadcast studio with LED world map
screen. Three-point lighting: key at 45 degrees left, fill right,
backlight rim on hair. Sharp subject, soft background. Broadcast quality,
16:9, color-calibrated.
```
*(Для Motion Control не описываем движения — только внешность и окружение)*

---

## Противоречия между источниками (с решением)

### 1. Длина промпта: длинный vs короткий

**Противоречие:**
- Habr (StudyAI): "фокусируйтесь на одном действии, не перегружайте"
- atlabs.ai: "длинные промпты работают эффективно, если логично структурированы"

**Решение:** Длина не важна — важна **структура**. Длинный промпт с чёткими блоками (Shot 1 / Shot 2 / SFX) работает. Длинный промпт-поток сознания без структуры — нет. Короткий промпт для одной сцены — отлично. Универсальное правило: одно действие на кадр, структура обязательна.

---

### 2. Язык промпта: русский vs английский

**Противоречие:**
- Habr (StudyAI): "пишите промпты на английском для лучшего понимания"
- vc.ru: приводит примеры на русском как рабочие

**Решение:** Английский даёт более точные результаты, особенно для диалогов (lip-sync) и кинематографических терминов. Русский работает для базовых сцен. **Рекомендация**: пишите промпты на английском, особенно для аудио и multi-shot.

---

### 3. Negative prompts: нужны ли они

**Противоречие:**
- kod.ru / atlabs.ai: активно рекомендуют negative prompts
- kling3.online / daily-prompts: не упоминают их вовсе

**Решение:** Negative prompts работают в Kling 3.0, но менее критичны, чем в Stable Diffusion. Используйте для I2V (оживление фото) и диалоговых сцен — там риск артефактов выше. Для простых text-to-video часто достаточно хорошего позитивного промпта.

---

### 4. CFG Scale (творческая свобода модели)

**Противоречие:**
- Некоторые источники рекомендуют высокое CFG для точного следования промпту
- Другие не упоминают этот параметр вовсе

**Решение:** Kling 3.0 не экспортирует CFG как явный параметр пользователю в большинстве интерфейсов (в отличие от SD). Управление "следованием промпту" происходит через **конкретность описания**, а не через числовой параметр. Чем конкретнее детали — тем точнее результат.

---

### 5. Image-to-video: описывать фото или нет

**Противоречие:**
- kling3-ai.com: в I2V не описывайте то, что уже видно на фото
- kod.ru: рекомендует открывать промпт фразой о сохранении черт

**Решение:** Оба совета верны и не противоречат. Открывающая фраза `Strictly preserve the facial features...` — это инструкция модели о режиме, а не описание содержимого фото. После неё — только движение и изменения, не пересказывайте внешность.

---

## Быстрая шпаргалка (для ежедневного использования)

```
✓ Shot type → ✓ Subject → ✓ Action (sequential) → ✓ Camera → ✓ Light → ✓ Audio

Камера: dolly push-in / tracking shot / handheld / crane shot / rack focus
Свет: golden hour / volumetric / three-point / neon / candlelight
Стиль: 35mm film / VHS / anamorphic / Studio Ghibli / nature documentary
Детали: grain / lens flare / condensation / fabric sway / visible breath
Аудио: SFX: ... / [Character, voice tone]: "..."
Negative: morphing, distorted face, warped hands, flickering, extra limbs

Параметры: Professional mode, 10–15s, 16:9 (YouTube) / 9:16 (TikTok)
I2V: min 2048px, целевой aspect ratio, без обрезанных конечностей
```
