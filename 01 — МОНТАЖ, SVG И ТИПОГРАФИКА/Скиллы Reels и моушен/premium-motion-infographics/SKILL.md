---
name: premium-motion-infographics
description: Create premium, varied SVG/HTML motion infographics for Reels, explainers, launch videos, presentations, and product stories. Use when the request calls for cinematic data art, unusual spheres, particle/ASCII objects, editorial charts, mascots, interface motion, or high-end explanatory animation rather than generic UI cards or repeated diagram templates.
---

# Premium Motion Infographics

Create a visual explanation, not decorative motion. For Elianora, read [eli-visual-system.md](references/eli-visual-system.md) before designing or coding.

## Non-negotiable workflow

1. Extract the beats and write a visual treatment before coding. For every beat, specify: spoken idea, visual metaphor, information shown, motion action, and why the next beat is different. Do not start implementation until every beat has a named object family and kinetic verb.
2. Build an inventory. Do not reuse the same object family in adjacent beats; in a 30-second sequence, no family may appear more than twice unless the script explicitly requires recurrence. Treat a browser window, progress bar, checkmark, node graph, and orbit as separate families.
3. Establish a constrained system: canvas, safe area, font sizes, palette, stroke weights, timing, and a single active accent colour. Respect user-provided tokens over defaults.
4. Make a single 5–10 second proof of the most difficult scene. Render or screen-capture it, inspect it at delivery size, then continue only after approval when requested. Never expand a weak proof into the full video.
5. Implement scene-specific SVG/HTML/CSS animation. Use `animejs` for timelines and `svg-animations` / `svg-creator` for SVG construction when available.
6. Run visual QA: no overlap, clipping, accidental repeated structures, unreadable text, or static holds longer than 0.6 seconds unless intentionally required. Use a 1× playback check and screenshots at entrance, action peak, and exit for every unique scene.

## Storyboard standard

Before implementation, make a compact table:

| Time | Meaning | Object family | On-screen action | Transition |
|---|---|---|---|---|

Keep one main thought per micro-scene. Do not make a new scene by merely changing a caption on a previous visual.

## Hard rejection gate

Stop and redesign a beat before showing it if any statement is true:

- Its graphic could be swapped with another beat without changing the meaning.
- It is a browser-window shell, progress bar, checkmark, rounded card, node graph, orbit, or long line used as decoration rather than explanation.
- It repeats the silhouette, layout, easing, or object family of either of the two preceding beats.
- It has a static central icon while only text changes.
- More than one element overlaps unintentionally, text exceeds its safe area, or a diagram cannot be understood without the caption.
- The accent colour is doing the work of visual hierarchy instead of signalling one active datum or action.

When a beat fails, replace the metaphor—not merely its colour, scale, or caption.

## Visual families

Choose the family from the meaning, then vary its geometry and behaviour. Consult [visual-vocabulary.md](references/visual-vocabulary.md) for the selection guide. For Elianora's locked mappings and palette, use [eli-visual-system.md](references/eli-visual-system.md).

- **Language / transcription:** numeric/glyph sphere, word sphere, timestamp stream, typographic particles resolving into phrases.
- **Time / compression:** clock hand arc, collapsing time blocks, radial comparison, stepped data density, elastic counter.
- **Automation / AI:** modular mascot, process conveyor, transforming files, self-assembling system, terminal-to-object translation.
- **Video / editing:** waveform, edit decision list, layered timeline, caption snapping, crop map, protected safe-area field.
- **Review / quality:** comparison lens, annotation pins, diff layers, playback scrubber, before/after peel.
- **Outcome:** assembled reel, generative export, controlled particle release, compact results board.

Avoid assigning a generic browser window to every idea. A panel may appear only when it communicates a real interaction.

## Composition rules

- Use a visible grid and safe margins. Align objects deliberately; never solve layout by overlapping elements.
- Keep the title/subtitle anchor consistent when the format calls for it. Let the moving graphic occupy its own stage.
- Use 2–3 text sizes plus one tiny technical label size. Keep technical labels subdued.
- Use an accent colour only for the current action, selected datum, or branded mascot. Never use it as a default outline, repeated bar, or long decorative line.
- A line must terminate in, connect, cut, measure, sort, trace, or construct an object. If it does none of these, remove it.
- Use depth through density, scale, masking, parallax and temporal sequencing—not gratuitous gradients or heavy shadows.
- Reuse brand motifs sparingly. A mascot can recur as an actor, but must do a different job each time.

## Motion rules

- Animate cause and effect: input becomes process, process becomes output.
- Prefer staggered assembly, flow, morphing, gathering, sorting, snapping, lifting, and compression over generic fade-ins.
- Keep primary entrances 250–500 ms. During a hold, leave a subtle live signal: cursor blink, data drift, looping particle field, or progressing marker.
- Never use a large checkmark, concentric circles, rounded card, generic browser window, or node web as a fallback. Use them only if the script literally needs confirmation, orbiting, a container, interaction, or a network.
- Make adjacent scenes distinct in silhouette, spatial rhythm, and kinetic principle.

## Mascots and reference assets

- Recreate a user-provided mascot faithfully before embedding it in scenes. Do not substitute an invented character.
- First deliver the mascot alone on a neutral background for visual approval when it is a focal brand element.
- Preserve its defining silhouette, proportions, colours and face; animate its action, not its identity.

## Validation checklist

- Is every beat visually distinct from the previous two?
- Can a viewer understand the action with sound off?
- Does every object have a semantic purpose?
- Are titles, labels and shapes unclipped at the target resolution?
- Is the accent colour used only for an active state?
- Are text, object density and stroke widths readable at actual playback size?
- Has a frame-by-frame screenshot pass been made at scene starts, peaks and transitions?
- Has the beat passed the hard rejection gate?
