---
name: animejs
description: Versatile JavaScript animation engine for DOM, CSS, SVG, and JavaScript objects. Use when creating timeline-based animations, stagger effects, SVG morphing, keyframe sequences, or complex choreographed animations. Triggers on tasks involving Anime.js, timeline animations, staggered sequences, SVG path animations, morphing, or multi-step animation choreography. Alternative to GSAP for SVG-heavy animations and React-independent projects.
---

# Anime.js

Lightweight JavaScript animation library with powerful timeline and stagger capabilities for web animations.

## ⚠ ОБЯЗАТЕЛЬНЫЙ ФОРМАТ для Reels-анимаций Ули

Любая HTML-анимация для Reels должна соответствовать формату ниже. Это обеспечивает совместимость с автоматической QA-проверкой (если она установлена) и записью в mp4 через `record.py`.

### Что обязано быть

1. **Stage 1080×1920** (вертикальный, под Reels)
   - `<div class="stage" id="stage">` с `width:1080px;height:1920px`
   - `transform-origin:top center` + JS-функция `fit()` для авто-подгонки под окно

2. **Глобальные функции для harness:**
   - `window.startAnimation()` — запускает/перезапускает анимацию
   - `window.master` — ссылка на anime.timeline
   - Поддержка `?qa=1` в URL: при наличии `autoplay:false`, ждёт ручного вызова `startAnimation()`

3. **Инкрементный счётчик сцен:**
   - `mark()` без аргумента — вызывается в `begin:` каждой сцены
   - Внутри: `sceneIdx++; setProgress(sceneIdx); if(window.qaMark) window.qaMark(sceneIdx);`

4. **Служебные элементы скрываются в записи** (CSS-классы `.progress` и `.controls` — record.py их прячет автоматически)

### Как использовать шаблон

1. Скопируйте `~/.claude/skills/animejs/template_index.html` в папку проекта как `index.html`
2. Заполните сцены (HTML внутри `.scene` блоков)
3. Заполните таймлайн в `buildTimeline()` (каждая сцена начинается с `master.add({targets:'#sN', opacity:[0,1], duration:300, begin:()=>mark()})`)
4. Обновите `const SCENES` на актуальное число сцен
5. Прогоните QA: `python3 ~/.claude/skills/animation-qa/qa_check.py index.html`
6. Запишите видео: `python3 ~/.claude/skills/animejs/record.py --duration N`

### Скрипт записи (record.py)

Лежит в `~/.claude/skills/animejs/record.py`. Можно вызывать из любой папки:

```bash
cd /путь/к/проекту/анимации
python3 ~/.claude/skills/animejs/record.py --duration 55
# → _out/index.mp4
```

Или скопировать в папку анимации как `record.py` и запускать локально `python3 record.py`.

Параметры:
- `--duration N` — длительность записи в секундах (по умолчанию 60)
- `--html path` — путь к HTML (по умолчанию `./index.html`)
- `--out path` — путь к выходному mp4 (по умолчанию `_out/{html_name}.mp4`)

Выход: mp4 1080×1920, h264, без звука, без рамок и панелей браузера.

### Правила контента (важно для Ули)

- **Никакого шрифта меньше 40px** — на мобильном плохо читается
- **Числа ВСЕГДА цифрами, никогда словами** — «92%», не «девяносто два процента». «1000 человек», не «тысяча человек». QA-скил `animation-qa` это автоматически проверяет (`numbers_as_words`).
- **Подписи в кадре — максимум 3-4 строки.** Никогда не на весь экран. Если фраза не помещается крупно в 4 строки — разбить на 2 сцены. QA проверяет (`oversized_text`).
- **Никаких дублирований** — если число уже показано, не повторять его словами
- **Один кадр — одна мысль** — не нагружать кадр иконками/декорацией
- **Цветовой код**: жёлтый = деньги, красный = опасность/налог, зелёный = рост/правильно, белый = факт, серый = вспомогательный

### Текст поверх графики — обязательная плашка-градиент

Если подпись лежит над сеткой/графиком/массой элементов (zoom, stagger-сетка из 100+ объектов и т.п.), под текстом ОБЯЗАТЕЛЕН тёмный градиент-плашка. Шаблон в `template_index.html` содержит готовые классы `.top-text` и `.bottom-text` — используйте их.

```css
.top-text{
  position:absolute;left:0;right:0;top:0;z-index:10;
  padding:90px 80px 70px; text-align:center;
  background:linear-gradient(to bottom,
    rgba(10,10,18,0.92) 0%,
    rgba(10,10,18,0.88) 65%,
    rgba(10,10,18,0) 100%);
}
```

Без плашки текст пропадает на сильном zoom — приходится переделывать. Не экономьте 5 строк CSS.

### Метафоры — что НЕ делать

- ❌ Мультяшные иконки: домики-банки, человечки-кружки, короны, звёзды
- ❌ Глаза-овалы как "журналисты"
- ❌ SVG-мешки $ как "деньги"
- ❌ Дома с колоннами как "банк/налоговая"
- ❌ Российский флаг сам по себе как "Россия"

**Исключение:** силуэт-человечек как массовая инфографика (сетка 100/1000 одинаковых силуэтов для статистики «92% не доходят») — допустим. Готовый класс `.person` в шаблоне. НЕЛЬЗЯ использовать одиночного человечка как иконку.

### Метафоры — что работает

- ✅ **Газетная вырезка** с заголовком и штампом «УТЕЧКА/LEAKED»
- ✅ **Гигантская цифра** во весь кадр (счёт, налог, разница)
- ✅ **Перечёркнутая плашка** с текстом ("ЗАРПЛАТА: $0" + красная линия)
- ✅ **Цветная карточка** с тикером и графиком (TSLA + ▲ + линия)
- ✅ **Конверт с печатью** (для уведомлений ФНС, повесток)
- ✅ **Развилка с цифрами** (×100 разница: 15 000 vs 1 500 000)
- ✅ **Текстовая схема со стрелками** (A → B → C словами, не иконками)

## Overview

Anime.js (pronounced "Anime JS") is a versatile animation engine that works with DOM elements, CSS properties, SVG attributes, and JavaScript objects. Unlike React-specific libraries, Anime.js works with vanilla JavaScript and any framework.

**When to use this skill:**
- Timeline-based animation sequences with precise choreography
- Staggered animations across multiple elements
- SVG path morphing and drawing animations
- Keyframe animations with percentage-based timing
- Framework-agnostic animation (works with React, Vue, vanilla JS)
- Complex easing functions (spring, steps, cubic-bezier)

**Core features:**
- Timeline sequencing with relative positioning
- Powerful stagger utilities (grid, from center, easing)
- SVG morphing and path animations
- Built-in spring physics easing
- Keyframe support with flexible timing
- Small bundle size (~9KB gzipped)

## Loading via CDN (no build step)

For Ulia's projects (plain HTML, no npm), load via CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"></script>
<script>
  anime({
    targets: '.element',
    translateX: 250,
    duration: 800,
    easing: 'easeInOutQuad'
  })
</script>
```

## Core Concepts

### Basic Animation

```javascript
anime({
  targets: '.element',
  translateX: 250,
  rotate: '1turn',
  duration: 800,
  easing: 'easeInOutQuad'
})
```

### Targets

```javascript
anime({ targets: '.box' })                              // CSS selector
anime({ targets: document.querySelectorAll('.box') })   // DOM elements
anime({ targets: [el1, el2, el3] })                     // Array of elements
const obj = { x: 0 }; anime({ targets: obj, x: 100 })   // JS object
```

### Animatable Properties

CSS properties:
```javascript
anime({
  targets: '.element',
  translateX: 250,
  scale: 2,
  opacity: 0.5,
  backgroundColor: '#FFF'
})
```

CSS transforms (use individual props, not the `transform` string):
```javascript
anime({
  targets: '.element',
  translateX: 250,
  rotate: '1turn',
  scale: 2
})
```

SVG attributes:
```javascript
anime({
  targets: 'path',
  d: 'M10 80 Q 77.5 10, 145 80',
  fill: '#FF0000',
  strokeDashoffset: [anime.setDashoffset, 0]
})
```

### Timeline

```javascript
const tl = anime.timeline({ duration: 750, easing: 'easeOutExpo' })

tl.add({ targets: '.box1', translateX: 250 })
  .add({ targets: '.box2', translateX: 250 }, '-=500')   // 500ms before previous ends
  .add({ targets: '.box3', translateX: 250 }, '+=200')   // 200ms after previous ends
```

## Common Patterns

### 1. Stagger reveal

```javascript
anime({
  targets: '.stagger-element',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(100),
  easing: 'easeOutQuad',
  duration: 600
})
```

### 2. Stagger from center / grid

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [14, 5],
    from: 'center',
    axis: 'x'
  }),
  easing: 'easeOutQuad'
})
```

### 3. SVG line drawing

```javascript
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutQuad',
  duration: 2000,
  delay: (el, i) => i * 250
})
```

### 4. SVG morphing

```javascript
anime({
  targets: '#morphing-path',
  d: [
    { value: 'M10 80 Q 77.5 10, 145 80' },
    { value: 'M10 80 Q 77.5 150, 145 80' }
  ],
  duration: 2000,
  easing: 'easeInOutQuad',
  loop: true,
  direction: 'alternate'
})
```

### 5. Hero entrance timeline

```javascript
const tl = anime.timeline({ easing: 'easeOutExpo', duration: 750 })

tl.add({ targets: '.title',    translateY: [-50, 0], opacity: [0, 1] })
  .add({ targets: '.subtitle', translateY: [-30, 0], opacity: [0, 1] }, '-=500')
  .add({ targets: '.button',   scale: [0, 1],        opacity: [0, 1] }, '-=300')
```

### 6. Keyframe sequence

```javascript
anime({
  targets: '.element',
  keyframes: [
    { translateX: 100 },
    { translateY: 100 },
    { translateX: 0 },
    { translateY: 0 }
  ],
  duration: 4000,
  easing: 'easeInOutQuad',
  loop: true
})
```

### 7. Scroll-driven scrubbing

```javascript
const animation = anime({
  targets: '.scroll-element',
  translateY: [100, 0],
  opacity: [0, 1],
  easing: 'easeOutQuad',
  autoplay: false
})

window.addEventListener('scroll', () => {
  const p = window.scrollY / (document.body.scrollHeight - window.innerHeight)
  animation.seek(animation.duration * p)
})
```

## Easing

Spring:    `easing: 'spring(1, 80, 10, 0)'` (mass, stiffness, damping, velocity)
Steps:     `easing: 'steps(5)'`
Bezier:    `easing: 'cubicBezier(.5, .05, .1, .3)'`
Built-ins: `easeInOutQuad`, `easeOutExpo`, `easeOutBack`, `easeInOutCirc`, ...

## Direction & Loop

```javascript
anime({
  targets: '.element',
  translateX: 250,
  direction: 'alternate',  // 'normal' | 'reverse' | 'alternate'
  loop: true,              // true | number
  easing: 'easeInOutQuad'
})
```

## Playback Control

```javascript
const a = anime({ targets: '.el', translateX: 250, autoplay: false })
a.play(); a.pause(); a.restart(); a.reverse(); a.seek(500)
```

## Path Following

```javascript
const path = anime.path('#motion-path')

anime({
  targets: '.element',
  translateX: path('x'),
  translateY: path('y'),
  rotate: path('angle'),
  easing: 'linear',
  duration: 2000,
  loop: true
})
```

## Performance

- Animate `translateX/Y`, `scale`, `opacity` (GPU-accelerated). Avoid `left`, `width`, `height`.
- Batch animations on a single `targets` selector instead of looping per element.
- Set `will-change: transform, opacity` on heavily animated nodes.
- For infinite background loops prefer pure CSS `@keyframes` over JS loops.

## Common Pitfalls

1. **Forgetting units** for non-transform props: `width: '200px'`, not `width: 200`.
2. **Using the `transform` string**: animate `translateX`, `rotate`, `scale` individually.
3. **No cleanup in React**: keep the animation handle and call `pause()` in the effect cleanup.
4. **Animating 1000+ nodes**: switch to pure CSS or virtualize the list.
5. **Timeline offsets without operator**: `'+=200'` / `'-=500'`, never bare `'500'`.
6. **`loop: true` everywhere**: drains battery; use CSS for endless ambient motion.

## Anime.js vs alternatives

- **vs GSAP** — Anime.js is lighter and great for SVG; GSAP wins for complex scroll-driven scenes and pro timelines.
- **vs Framer Motion** — Anime.js is framework-agnostic; Motion is React-only with gesture/layout magic.
