# Brand register

When design IS the product: brand sites, landing pages, marketing surfaces, campaign pages, portfolios, long-form content, about pages. The deliverable is the design itself; a visitor's impression is the thing being made.

The register spans every genre. A tech brand (Stripe, Linear, Vercel). A luxury brand (a hotel, a fashion house). A consumer product (a restaurant, a travel site, a CPG packaging page). A creative studio, an agency portfolio, a band's album page. They all share the stance (*communicate, not transact*) and diverge wildly in aesthetic. Don't collapse them into a single look.

## The brand slop test

If someone could look at this and say "AI made that" without hesitation, it's failed. The bar is distinctiveness; a visitor should ask "how was this made?", not "which AI made this?"

Brand isn't a neutral register. AI-generated landing pages have flooded the internet, and average is no longer findable. Restraint without intent now reads as mediocre, not refined. Brand surfaces need a POV, a specific audience, a willingness to risk strangeness. Go big or go home.

**The second slop test: aesthetic lane.** Before committing to moves, name the reference. A Klim-style specimen page is one lane; Stripe-minimal is another; Liquid-Death-acid-maximalism is another. Don't drift into editorial-magazine aesthetics on a brief that isn't editorial. A hiking brand with Cormorant italic drop caps has the wrong register within the register.

Then the inverse test: in one sentence, describe what you're about to build the way a competitor would describe theirs. If that sentence fits the modal landing page in the category, restart.

## Typography

### Font selection procedure

Every project. Never skip.

1. Read the brief. Write three concrete brand-voice words. Not "modern" or "elegant," but "warm and mechanical and opinionated" or "calm and clinical and careful." Physical-object words.
2. List the three fonts you'd reach for by reflex. If any appear in the reflex-reject list below, reject them; they are training-data defaults and they create monoculture.
3. Browse a real catalog (Google Fonts, Pangram Pangram, Future Fonts, Adobe Fonts, ABC Dinamo, Klim, Velvetyne) with the three words in mind. Find the font for the brand as a *physical object*: a museum caption, a 1970s terminal manual, a fabric label, a cheap-newsprint children's book, a concert poster, a receipt from a mid-century diner. Reject the first thing that "looks designy."
4. Cross-check. "Elegant" is not necessarily serif. "Technical" is not necessarily sans. "Warm" is not Fraunces. If the final pick lines up with the original reflex, start over.

### Reflex-reject list

Training-data defaults. Ban list. Look further:

Fraunces · Newsreader · Lora · Crimson · Crimson Pro · Crimson Text · Playfair Display · Cormorant · Cormorant Garamond · Syne · IBM Plex Mono · IBM Plex Sans · IBM Plex Serif · Space Mono · Space Grotesk · Inter · DM Sans · DM Serif Display · DM Serif Text · Outfit · Plus Jakarta Sans · Instrument Sans · Instrument Serif

### Reflex-reject aesthetic lanes

Parallel to the font list. Currently saturated aesthetic families that have flooded brand surfaces. If a brief lands in one of these lanes without a register reason that *requires* it (a literal magazine, a literal terminal, a literal industrial signage system), it's the second-order training reflex: the trap one tier deeper than picking a Fraunces font. Look further.

- **Editorial-typographic.** Display serif (often italic) + small mono labels + ruled separators + monochromatic restraint. Klim-influenced, magazine-cover affectation. By 2026, every Stripe-adjacent and Notion-adjacent brand has landed here. The fingerprint: three rule-separated columns, an italic Fraunces / Recoleta / Newsreader headline, lowercase track-spaced metadata, no imagery.

(More entries land here on the same cadence the font list updates. Brutalist-utility and acid-maximalism may join when they saturate. Removing entries when they fall back below saturation is also fine.)

The reflex-reject lists apply to **new design choices**. When the existing brand has already committed to a font or a lane as part of its identity, identity-preservation wins; variants on an existing surface don't second-guess what's already shipping. The reflex-reject lists are for greenfield decisions and for departure-mode variants in [live.md](live.md).

### Pairing and voice

Distinctive + refined is the goal. The specific shape depends on the brand:

- **Editorial / long-form / luxury**: display serif + sans body (a magazine shape).
- **Tech / dev tools / fintech**: one committed sans, usually; custom-tight tracking, strong weight contrast inside a single family.
- **Consumer / food / travel**: warmer pairings, often a humanist sans plus a script or display serif.
- **Creative studios / agencies**: rule-breaking welcome. Mono-only, or display-only, or custom-drawn type as voice.

Two families minimum is the rule *only* when the voice needs it. A single well-chosen family with committed weight/size contrast is stronger than a timid display+body pair.

Vary across projects. If the last brief was a serif-display landing page, this one isn't.

### Scale

Modular scale, fluid `clamp()` for headings, ≥1.25 ratio between steps. Flat scales (1.1× apart) read as uncommitted.

Light text on dark backgrounds: add 0.05–0.1 to line-height. Light type reads as lighter weight and needs more breathing room.

## Color

Brand surfaces have permission for Committed, Full palette, and Drenched strategies. Use them. A single saturated color spread across a hero is not excess; it's voice. A beige-and-muted-slate landing page ignores the register.

- Name a real reference before picking a strategy. "Klim Type Foundry #ff4500 orange drench", "Stripe purple-on-white restraint", "Liquid Death acid-green full palette", "Mailchimp yellow full palette", "Condé Nast Traveler muted navy restraint", "Vercel pure black monochrome". Unnamed ambition becomes beige.
- Palette IS voice. A calm brand and a restless brand should not share palette mechanics.
- When the strategy is Committed or Drenched, color carries the brand. Don't hedge with neutrals around the edges. Commit.
- Don't converge across projects. If the last brand surface was restrained-on-cream, this one is not.
- When a cultural-symbol palette is the obvious pull, reach past it. Let the cultural reading come from typography, imagery, and copy, not the palette.

## Layout

- Asymmetric compositions are one option. Break the grid intentionally for emphasis.
- Fluid spacing with `clamp()` that breathes on larger viewports. Vary for rhythm: generous separations, tight groupings.
- Alternative: a strict, visible grid as the voice (brutalist / Swiss / tech-spec aesthetics). Either asymmetric or rigorously-gridded can be "designed"; the failure mode is splitting the difference into a generic centered stack.
- Don't default to centering everything. Left-aligned with asymmetric layouts feels more designed; a strict grid reads as confident structure. A centered-stack hero with icon-title-subtitle cards reads as template.
- When cards ARE the right affordance, use `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` for breakpoint-free responsiveness.

## Imagery

Brand surfaces lean on imagery. A restaurant, hotel, magazine, or product landing page without any imagery reads as incomplete, not as restrained. A solid-color rectangle where a hero image should go is worse than a representative stock photo.

**When the brief implies imagery (restaurants, hotels, magazines, photography, hobbyist communities, food, travel, fashion, product), you must ship imagery.** Zero images is a bug, not a design choice. "Restraint" is not an excuse. If the approved comp or brief is image-led, ship real project assets, generated raster assets, or a credible canvas/SVG/WebGL scene. Do not replace photographic, architectural, product, or place imagery with generic CSS panels, decorative diagrams, cards, bullets, or copy.

- **For greenfield work without local assets, use stock imagery.** Unsplash is the default. The URL shape is `https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=1600&q=80`. **Verify the URLs before referencing them.** If you have an image-search MCP, web-fetch tool, or browser access, use it to find real photo IDs and confirm they resolve. Guessed IDs (even ones that look real) often 404 and ship as broken-image placeholders. Without a verification path, pick fewer photos you're confident exist over more that you guessed; never substitute colored `<div>` placeholders.
- **Search for the brand's physical object**, not the generic category: "handmade pasta on a scratched wooden table" beats "Italian food"; "cypress trees above a limestone hotel facade at dusk" beats "luxury hotel".
- **One decisive photo beats five mediocre ones.** Hero imagery should commit to a mood; padding with more stock doesn't rescue an indecisive one.
- **Alt text is part of the voice.** "Coastal fettuccine, hand-cut, served on the terrace" beats "pasta dish".

"Imagery" here is broader than stock photography: product screenshots, custom data visualizations, generated SVG, and canvas/WebGL scenes are all imagery. Text-only pages where typography alone carries the entire visual weight are the failure mode.

## Motion

- One well-orchestrated page-load with staggered reveals beats scattered micro-interactions, when the brand invites it. Tech-minimal brands often skip entrance motion entirely; the restraint is the voice.
- For collapsing/expanding sections, transition `grid-template-rows` rather than `height`.

## Кнопки — обязательная проверка

КАЖДАЯ кнопка на странице должна быть рабочей. Без исключений.

- Кнопки с `href="#"` — только если это якорная ссылка на реальный ID на странице. Иначе — заглушка `href` должна вести на реальный адрес или использовать `onclick`.
- Кнопки "Написать", "Связаться", "Оставить заявку" → всегда `href="mailto:..."` или `href="https://t.me/..."` с реальным контактом.
- Кнопки скролла вниз → `href="#section-id"` с реально существующим ID.
- После любого изменения разметки: проверить, что все `href` ведут куда надо, ни один не оборван и не остался заглушкой.
- Кнопка без действия — это ошибка, позор перед клиентом.

## Brand bans (on top of the shared absolute bans)

- Monospace as lazy shorthand for "technical / developer." If the brand isn't technical, mono reads as costume.
- Large rounded-corner icons above every heading. Screams template.
- Single-family pages that picked the family by reflex, not voice. (A single family chosen deliberately is fine.)
- All-caps body copy. Reserve caps for short labels and headings.
- Timid palettes and average layouts. Safe = invisible.
- Zero imagery on a brief that implies imagery (restaurant, hotel, food, travel, fashion, photography, hobbyist). Colored blocks where a hero photo belongs.
- Defaulting to editorial-magazine aesthetics (display serif + italic + drop caps + broadsheet grid) on briefs that aren't magazine-shaped. Editorial is ONE aesthetic lane, not the default brand aesthetic.
- Repeated tiny uppercase tracked labels above every section heading. A single strong kicker can be voice; repeating it as section grammar is AI scaffolding unless it's a deliberate, named brand system.

## Brand permissions

Brand can afford things product can't. Take them.

- Ambitious first-load motion. Reveals, scroll-triggered transitions, typographic choreography.
- Single-purpose viewports. One dominant idea per fold, long scroll, deliberate pacing.
- Typographic risk. Enormous display type, unexpected italic cuts, mixed cases, hand-drawn headlines, a single oversize word as a hero.
- Unexpected color strategies. Palette IS voice; a calm brand and a restless brand should not share palette mechanics.
- Art direction per section. Different sections can have different visual worlds if the narrative demands it. Consistency of voice beats consistency of treatment.

## Висячие предлоги и союзы

НИКОГДА не оставлять предлоги, союзы и частицы висячими в конце строки — ни в заголовках, ни в параграфах, ни в подписях. Список: за, и, в, на, с, к, по, или, но, от, до, у, о, а, но, же, бы, то, это, не, без, при, для, об.

Это касается ВСЕХ текстовых блоков на странице — h1, h2, h3, p, li, caption, footer. Не только заголовков.

Способы исправления:
- Использовать `&nbsp;` между предлогом/союзом и следующим словом: `в&nbsp;первую`, `к&nbsp;сроку`, `без&nbsp;итераций`
- Перефразировать так, чтобы предлог не попадал в конец строки
- Применять системно ко всем коротким словам (1–3 символа) перед следующим словом в теле текста

Пример ошибки: "Новый облик за↵8 недель", "Финал в↵руках", "Всё по↵ТЗ"

## Ширина текстовых параграфов

Параграфы (`p`, `li`) в многоколоночных блоках НИКОГДА не должны расползаться на всю ширину колонки — текст должен иметь `max-width`.

Правило: для body-текста внутри компонентов (карточки, спринт-строки, планы) — `max-width: 48–56ch`. Без ограничения ширины текст на широком экране растягивается в одну длинную строку, которая плохо читается и не держит вертикальный ритм.

Пример применения: `.week p { max-width: 52ch; }` — текст в спринт-строках не выходит за вертикальную линию раздела.

## Перенос строк в заголовках — обязательные правила

### Ручное управление переносом
Когда пользователь задаёт конкретное место переноса строки — использовать `<br>` в точно указанном месте. НИКОГДА не полагаться на автоматический CSS-перенос там, где важна точная типографика заголовка.

Если пользователь говорит «строчка 1 / строчка 2» — значит нужно поставить `<br>` именно там. Не интерпретировать вольно, не переносить в другом месте.

При использовании `<br>` для конкретного переноса: `max-width` должен быть достаточно широким (`max-width: 100%` или убран совсем), чтобы `<br>` управлял переносом, а не CSS.

### Баланс длин строк — на всех экранах
Если `<br>` не указан явно: строки должны быть примерно одинаковой длины (±20% максимум). Подбирать `max-width` в `ch` так, чтобы добиться баланса.

ЗАПРЕЩЕНО: строка 150 символов и рядом строка 10 символов. Это грубая ошибка на любом экране — мобиле, планшете, ПК.

Обязательно проверять перенос на трёх точках: мобиле (~375px), планшете (~768px), десктопе (~1440px). На каждой ширине заголовок должен переноситься лаконично и сбалансированно.

Инструменты балансировки:
- `max-width` в `ch` — основной инструмент. Для заголовков обычно 16–22ch дают баланс на десктопе
- `<br>` с медиазапросами — если нужен разный перенос на мобиле и ПК: `<span class="br-mobile"><br></span>` со стилем `display: none` на десктопе
- `text-wrap: balance` (CSS) — автоматический баланс, поддерживается в современных браузерах. Добавлять ко всем заголовкам `h1, h2, h3 { text-wrap: balance; }` как базовое правило
- НИКОГДА не использовать `max-width: 100%` для заголовков которые должны переноситься — это снимает контроль над переносом на широких экранах

## Ёлочка — запрещённый перенос строк в заголовках

НИКОГДА не допускать ёлочки в заголовках: это когда строки переноса имеют разную длину и образуют ступенчатый «треугольник» (длинная → короткая → ещё короче). Это грубая типографская ошибка.

Правило: заголовок должен переноситься максимум на 2 строки примерно одинаковой длины. Три и более строк — только если они выровнены по длине.

Способы исправления:
- Подобрать `max-width` в `ch` так, чтобы текст разбивался на 2 сбалансированные строки
- Перефразировать заголовок — укоротить или удлинить фразу, чтобы перенос был органичным
- Использовать `<br>` в нужном месте для ручного управления переносом
- Никогда не оставлять `max-width: 26ch` «по умолчанию» — всегда проверять, как текст переносится

Пример ошибки: "Можем добавить к↵любому тарифу↵по запросу" — три строки ступенькой.

## Интервал между заголовком и подзаголовком

Между заголовком (`h2`, `h3`) и следующим за ним подзаголовком / подписью (`p`, `.subtitle`, `.sub`) ВСЕГДА должно быть 20–40px пространства. Никогда меньше.

- `margin-bottom: 12px` у заголовка — слишком мало, тексты «наезжают» друг на друга
- Минимум: `margin-bottom: 24px`, оптимально: `28–32px`
- Заголовок и подзаголовок должны образовывать плотную, но читаемую группу — они относятся друг к другу, но не сливаются

Пример ошибки: `margin-bottom: 12px` при крупном `font-size` заголовка — подзаголовок визуально наезжает на нижние строки заголовка.
