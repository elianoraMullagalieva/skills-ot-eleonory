(async () => {
  await figma.loadFontAsync({ family: "Inter", style: "Regular" });
  await figma.loadFontAsync({ family: "Inter", style: "Bold" });
  await figma.loadFontAsync({ family: "Inter", style: "Medium" });
  const page = figma.currentPage;
  let fixed = 0;

  const updates = [
    { id: "10:295", text: `сделай мне 6 таких разноформенных фигур на точно таком же фон` },
    { id: "10:304", text: `REFERENCE SYSTEM:
Image 1 = primary color palette and atmosphere
Image 2,3 = premium layout rhythm and luxury minimalism reference
Image 4 = brand system, typography and composition reference
TASK:
Transform the current visual identity into a more refined, minimalistic and ultra-premium futuristic brand system.
Create a COMPLETE cohesive luxury visual identity in the exact emotional atmosphere and color palette from Image 1, while inheriting the elegance, spacing, composition and art direction quality from Image 1, 2 and 4.
The result should feel:
more expensive
more minimal
more intelligent
more architectural
more emotionally premium
more fashion-editorial
more timeless
more art directed
IMPORTANT:
Reduce visual noise.
Reduce random abstraction.
Reduce overdesigned gradients.
Everything should become:
cleaner,
calmer,
more intentional,
more spatial,
more luxurious.
CREATE A FULL BRAND SYSTEM:
logo atmosphere
typography system
visual identity language
premium website compositions
modular UI system
editorial poster layouts
luxury social templates
futuristic stickers
abstract graphic elements
sound-inspired visual forms
minimal iconography
premium presentation slides
typography compositions
atmospheric background systems
sculptural CGI figures
interface elements
navigation systems
premium buttons and cards
conceptual campaign visuals
VISUAL STYLE:
Ultra-minimal luxury futurism, cinematic editorial design, atmospheric CGI abstraction, architectural composition, premium sensory minimalism, conceptual technology aesthetic, Apple x Gentle Monster x Acne Studios x TeamLab visual language.
The brand should feel like:
a private intellectual club
a luxury cognitive platform
a fashion-tech exhibition
a futuristic editorial universe
a conceptual gallery installation
COLOR SYSTEM:
Use ONLY the emotional palette from Image 1.
Main colors:
pearl aqua
translucent cyan
soft resonance blue
atmospheric turquoise
luminous lemon accents
smoked graphite
pearl white
Gradients must feel:
soft
cinematic
atmospheric
premium
layered
calm
translucent
intelligent
Avoid:
aggressive neon
cyberpunk
rainbow holographics
hard transitions
noisy abstraction
generic AI gradients
TYPOGRAPHY:
Minimal editorial typography.
Large elegant spacing.
Architectural hierarchy.
Tiny captions + oversized headlines.
Gallery-style composition.
Only premium minimal layouts.
Typography should feel:
quiet,
confident,
fashion-level,
expensive,
intellectual.
MATERIALS:
frosted glass
smoked crystal
liquid acrylic
soft chrome
pearl translucency
atmospheric haze
silk reflections
COMPOSITION RULES:
huge negative space
asymmetrical layouts
clean modular systems
floating balance
minimal luxury framing
premium visual hierarchy
calm interface rhythm
cinematic spacing
LIGHTING:
museum-grade studio lighting
soft atmospheric glow
elegant reflections
volumetric diffusion
subtle cinematic contrast
IMPORTANT:
The final result should NOT look like:
startup branding
SaaS UI
dribbble trend graphics
gaming visuals
generic AI art
Instead it should feel like:
a fully art-directed luxury futuristic identity system for an elite intellectual audiovisual platform.` },
    { id: "10:313", text: `Image 1 = exact figure and geometry reference
Image 2,3 = exact HEX color palette reference only
Recreate the exact abstract figure from Image 1 with the original silhouette, proportions and geometry preserved precisely. Apply ONLY the colors from Image 2 as HEX palette references, without copying its lighting, reflections or texture behavior.
Premium translucent liquid-glass CGI sculpture, soft cinematic translucency, realistic natural studio reflections, physically accurate glass highlights, subtle refraction, smooth volumetric gradients, clean premium material rendering.
IMPORTANT:
preserve the original figure exactly
no new geometry
no random blobs
realistic natural reflections only
soft balanced highlights
no fake holographic shine
no oversaturated neon
no harsh gradients
Composition:
single isolated centered object, fully visible, not cropped, large empty space around the figure for clean cutout.
Background:
solid flat matte Figma-style background strictly HEX #181818, completely uniform, no gradients, no shadows, no texture, no additional objects or elements.
Ultra sharp high-resolution museum-grade CGI product render.` },
    { id: "10:322", text: `сделай мне эту фигуру без лишних квадртатов, на однотонном фоне цвета Hex #181818 и в высоком качестве` },
    { id: "10:331", text: `сделай фигуры с фото 1 в оттенках с фото 2 в формате HEX` },
    { id: "10:340", text: `REFERENCE SYSTEM:
Image 1 = main color atmosphere reference
Image 2 = secondary gradient/material reference
Image 3, 4, 5, 6  = editorial composition, modular layout system, poster rhythm and spatial graphic styling reference
IMPORTANT:
The previous generation created ONLY:
posters
a few sculptures
several compositions
BUT this task requires a FULL MODULAR DESIGN ECOSYSTEM.
The AI MUST think like:
a world-class art director
a futuristic product designer
a luxury interface studio
a premium branding system creator
The result should NOT look like:
“4 nice posters”.
The result MUST look like:
a COMPLETE DESIGN PACK for a futuristic luxury application, premium website and conceptual digital ecosystem.
MAIN TASK:
Create a MASSIVE cohesive luxury FUTURISTIC DESIGN SYSTEM PACK for “Performance Club” — an intellectual audiovisual platform where speech, thought, sound and cognition become a visual language.
Generate MANY DIFFERENT assets, components, modules and interface systems within ONE unified visual universe.
The output must feel like:
a luxury operating system
a futuristic sensory interface
an audiovisual AI ecosystem
a cognitive technology platform
a premium editorial campaign
a digital philosophy environment
a conceptual luxury product system
VERY IMPORTANT:
DO NOT generate:
only posters
only centered sculptures
isolated abstract renders
empty minimalist scenes
gallery mockups only
Instead:
Generate a REAL PRODUCT DESIGN SYSTEM with MANY ELEMENTS.
The final output should feel like:
an entire Figma system
a complete visual identity
a luxury app ecosystem
a futuristic UI kit
a modular web system
a conceptual product language
GENERATE ALL OF THESE ELEMENTS:
FULL WEBSITE SECTIONS:
hero screens
onboarding sections
immersive typography layouts
storytelling blocks
audio-reactive sections
interactive-looking interface compositions
luxury feature cards
premium call-to-action sections
futuristic statistics blocks
resonance visualization sections
speech analysis sections
editorial landing page modules
futuristic navigation systems
premium footer concepts
modular layout systems
FULL APPLICATION UI:
mobile app screens
desktop dashboard screens
onboarding flows
AI assistant interface
voice analytics screens
resonance calibration UI
speech structure interface
semantic optimization screens
futuristic player UI
profile systems
sound visualization UI
breathing synchronization interface
AI feedback overlays
immersive fullscreen experiences
luxury settings screens
UI COMPONENTS:
floating glass buttons
futuristic navigation bars
luxury toggles
premium sliders
resonance indicators
audio wave meters
liquid progress bars
translucent cards
floating windows
modular UI blocks
futuristic search bars
AI interaction modules
premium chips and tags
holographic labels
sensory interface widgets
glass dropdowns
luxury tabs
spatial notifications
abstract loaders
conceptual cursors
GRAPHIC SYSTEMS:
luxury futuristic stickers
modular poster systems
typography compositions
conceptual typography layouts
spatial graphic dividers
atmospheric separators
abstract icon systems
resonance-inspired symbols
frequency graphics
soundwave patterns
futuristic branding marks
premium abstract pictograms
editorial grid systems
layered graphic overlays
motion-inspired layout elements
3D OBJECTS & FORMS:
floating sound sculptures
speech waveforms
liquid intelligence forms
glass resonance ribbons
pearl frequency particles
volumetric abstract structures
translucent signal objects
sculptural interface geometry
atmospheric floating forms
liquid crystal abstractions
futuristic architectural shapes
sensory CGI objects
harmonic wave structures
abstract cognition sculptures
BACKGROUND SYSTEMS:
atmospheric gradients
volumetric fog backgrounds
soft luminous textures
cinematic depth environments
translucent light systems
pearl diffusion surfaces
futuristic spatial atmospheres
sensory visual environments
immersive luxury backdrops
audio-reactive-looking textures
SOCIAL MEDIA & BRAND SYSTEM:
launch campaign visuals
Instagram story layouts
quote cards
editorial social templates
futuristic announcement graphics
immersive typography posts
luxury presentation slides
product reveal posters
AI feature campaigns
conceptual branded compositions
VISUAL STYLE:
Ultra-premium CGI editorial futurism, luxury audiovisual minimalism, cinematic interface design, atmospheric abstraction, sculptural UI systems, sensory technology aesthetics, liquid translucency, emotional minimalism, conceptual digital brutalism, futuristic editorial composition, visualized cognition, sound-reactive design language.
The style should merge:
Apple × Gentle Monster × TeamLab × Acne Studios × luxury operating system × conceptual exhibition design × futuristic cognitive technology.
TYPOGRAPHY SYSTEM:
ONLY Russian typography.
Typography must feel:
cinematic
architectural
spatial
emotionally intelligent
premium
editorial
futuristic
minimal but powerful
Mix:
oversized brutalist headlines
tiny captions
floating typography
vertical text
isolated words
gallery-style spacing
modular editorial grids
conceptual hierarchy
USE PHRASES:
«Культура речи становится культурой мышления»
«Речь становится стратегией»
«Смыслы — формой капитала»
«Мы формируем среду, а не поток»
«Интеллект имеет свет»
«Звук имеет форму»
«Частота мышления»
«Система восприятия»
«Глубина. Смысл. Речь.»
«Речь как архитектура»
«Свет как мысль»
«Точность звучания»
«Среда определяет уровень»
«Резонанс интеллекта»
«Влиять. Формировать. Усиливать.»
IMPORTANT:
Typography should NOT dominate everything.
It should feel naturally embedded into the visual system.
COLOR SYSTEM:
Use Image 1 and Image 2 colors as inspiration.
PRIMARY COLORS:
pearl aqua
translucent cyan
smoked turquoise
liquid teal
atmospheric lime glow
crystal blue
soft silver
warm fog white
SECONDARY ACCENTS:
muted holographic violet
champagne reflections
soft ultraviolet shadows
deep oceanic gradients
COLOR BEHAVIOR:
Colors must blend through:
liquid translucency
pearl diffusion
atmospheric fog
soft reflections
volumetric layering
cinematic haze
smooth frequency transitions
Gradients should feel:
soft
fluid
breathable
premium
emotional
tactile
layered
intelligent
AVOID:
hard rainbow gradients
sharp neon
toxic colors
gaming holographics
cyberpunk aesthetics
dribbble-style blobs
MATERIALS:
frosted glass
liquid acrylic
translucent pearl
smoked crystal
soft chrome
atmospheric haze
liquid reflections
silk-like highlights
volumetric translucency
cinematic diffusion
INTERFACE PHILOSOPHY:
The interface should feel:
calm
intelligent
sensory
luxurious
futuristic
emotionally deep
spacious
beautifully minimal
innovative but believable
NOT:
startup SaaS
fintech dashboard
gaming UI
generic glassmorphism
neon cyberpunk
AI-generated trend graphics
Instead:
cognitive luxury technology
sensory operating system
audiovisual intelligence platform
conceptual premium interface
future luxury digital ecosystem
COMPOSITION RULES:
asymmetrical layouts
strong visual hierarchy
huge negative space
floating modular systems
layered interface depth
editorial rhythm
cinematic framing
modular design thinking
premium product composition
realistic usability
immersive visual architecture
LIGHTING:
cinematic studio lighting
soft atmospheric glow
volumetric diffusion
elegant reflections
premium shadows
internal illumination
deep spatial light
museum-grade lighting
emotional ambient atmosphere
FINAL RESULT:
The final output must look like:
a COMPLETE luxury digital ecosystem
a fully art-directed interface universe
a futuristic audiovisual operating system
a modular premium design language
a conceptual luxury technology platform
an immersive cognitive visual identity
The result must contain MANY assets and MANY interface elements within one cohesive system.
Not just pretty renders.
A FULL FUTURISTIC DESIGN PACK.` },
    { id: "10:349", text: `Сделай в большом качестве только фигуры из этого дизайна в точности как на исходном фото, но крупно, четко и точно` },
    { id: "10:358", text: `REFERENCE ANALYSIS
Current visual language from the reference:
MAIN COLORS:
electric turquoise
liquid cyan
soft aqua blue
translucent ice blue
acid lime yellow
liquid green glow
deep ocean teal
transparent crystal white
SECONDARY ACCENTS:
holographic magenta
warm golden reflections
soft ultraviolet shadows
BACKGROUND:
warm light gray
soft matte white
minimal editorial neutral tones
CURRENT MATERIAL STYLE:
liquid glass
translucent acrylic
reflective crystal
soft volumetric glow
premium CGI transparency
VERY IMPORTANT:
The current gradients work because:
they are volumetric
colors blend through transparency
transitions feel fluid
reflections create depth
materials behave like liquid light
BUT for the new version:
make gradients softer,
more atmospheric,
less aggressive,
more premium and calm.
Avoid:
toxic neon
hard rainbow transitions
sharp holographic edges
gaming aesthetic
The new system should feel:
softer
more cinematic
more intelligent
more sensory
more luxurious
more futuristic minimalism
MASTER TASK
Create a futuristic luxury mobile/web application interface system for an AI-powered speech and voice platform.
The app helps users:
improve speech structure
optimize delivery
train voice resonance
reduce verbal noise
improve speaking confidence
synchronize cognition and voice
transform speech into influence
The interface must feel like:
a sensory operating system from the future
a luxury cognitive technology
an audiovisual intelligence interface
a calm futuristic environment
premium AI for high-level thinkers and speakers
The visual language should merge:
sound visualization
liquid light
speech frequencies
resonance geometry
cognitive flow
atmospheric gradients
abstract intelligence
NO literal images.
NO humans.
NO microphones.
NO real-world objects.
Everything must be expressed through:
abstract forms
flowing textures
sound-inspired motion
light resonance
volumetric geometry
futuristic UI architecture
MAIN VISUAL STYLE
Luxury futuristic interface design, ultra-premium CGI abstraction, cinematic UI, liquid soundwave textures, translucent materials, atmospheric depth, soft volumetric lighting, minimal editorial composition, Apple-level refinement, futuristic cognition aesthetic, visualized speech technology, luxury AI interface, emotionally intelligent gradients, sculptural UI system.
The interface should feel:
intelligent
breathable
calm
futuristic
elegant
sensory
innovative
minimal
deeply art directed
GLOBAL UI SYSTEM
STYLE:
floating cards
glassmorphism reimagined in luxury way
soft depth layering
asymmetrical composition
premium typography
cinematic spacing
huge negative space
ultra clean UI hierarchy
MATERIALS:
liquid glass
translucent acrylic
pearl chrome
soft crystal
volumetric fog
reflective gradients
soundwave translucency
LIGHTING:
soft glow
internal illumination
cinematic reflections
atmospheric shadows
premium volumetric light
MOTION FEELING:
slow
floating
breathing-like
resonance-inspired
calm frequency movement
SCREEN STRUCTURE SYSTEM
ALL SCREENS MUST FEEL CONNECTED THROUGH:
same lighting logic
same soundwave texture system
same floating geometry language
same spacing system
same typography rhythm
same cinematic atmosphere
SCREEN 1 — ANALYTICS / NLP STRUCTURE
FUNCTION:
AI analyzes speech logic, detects weak transitions and improves structure.
VISUAL METAPHOR:
fragmented waves becoming ordered
cognitive restructuring
sound organizing itself
chaotic frequencies aligning into elegant geometry
ABSTRACTION:
floating translucent wave structures transforming into clean resonance lines
MAIN COLORS:
aqua blue
transparent cyan
soft silver
pearl white
PROMPT:
Create a futuristic luxury interface screen for AI speech structure analytics. Abstract soundwave geometry reorganizing itself into elegant cognitive patterns, floating translucent resonance lines, liquid glass textures, volumetric light gradients, cinematic futuristic UI, premium typography, ultra-clean layout, visualized speech logic, elegant restructuring frequencies, minimal luxury interface, soft atmospheric lighting, Apple x TeamLab aesthetic, luxury AI cognition platform.
SCREEN 2 — AUDIO DSP / BIO FEEDBACK
FUNCTION:
Real-time voice synchronization and biofeedback training.
VISUAL METAPHOR:
breathing frequencies
resonance synchronization
nervous system pulses
liquid sound harmonics
ABSTRACTION:
organic flowing volumetric forms reacting like living sound energy
MAIN COLORS:
lime glow
turquoise
soft emerald
translucent yellow-green
liquid cyan
PROMPT:
Create a premium futuristic voice training interface with audiovisual biofeedback abstraction. Organic sound resonance forms floating in cinematic space, liquid harmonic gradients, soft pulsating energy waves, translucent volumetric structures, sensory AI atmosphere, futuristic cognitive technology, elegant sound synchronization visuals, luxury CGI interface, breathing-like motion feeling, minimal but emotionally powerful UI.
SCREEN 3 — CONTENT OPTIMIZATION
FUNCTION:
AI reduces noise, strengthens meaning and transforms text into impactful speech.
VISUAL METAPHOR:
compression into clarity
noise dissolving
words becoming pure signal
semantic sharpening
ABSTRACTION:
dense colorful fog transforming into clean luminous directional flow
MAIN COLORS:
crystal blue
deep teal
silver glow
soft pearl cyan
PROMPT:
Create a luxury AI content optimization interface visualizing semantic clarity and speech enhancement. Abstract luminous flow structures emerging from atmospheric noise, elegant directional sound textures, liquid crystal gradients, futuristic minimal UI, cinematic typography composition, premium speech technology aesthetic, volumetric depth, sophisticated CGI abstraction, visualized meaning optimization.
GLOBAL TYPOGRAPHY SYSTEM
Typography must feel:
editorial
architectural
premium
futuristic
calm
intelligent
Use:
condensed bold headlines
thin minimal captions
oversized spacing
floating typography blocks
asymmetric alignment
Russian typography only.
IMPORTANT ART DIRECTION RULES
DO:
make sound feel physical
make speech feel visible
make cognition feel spatial
make gradients feel alive
make light feel intelligent
DO NOT:
create startup UI
create generic SaaS dashboards
create gaming interfaces
create cyberpunk screens
use hard neon
overload screens with widgets
make noisy holographic gradients
The result should look like:
a luxury cognitive operating system
a futuristic audiovisual intelligence platform
a sensory AI interface from the future
conceptual luxury technology
digital art installation + interface design hybrid` },
    { id: "10:367", text: `REFERENCE SYSTEM:
Image 1 = main color atmosphere reference
Image 2 = secondary gradient/material reference
Image 3, 4, 5, 7, 8 = poster/editorial composition and graphic styling reference
TASK:
Create a complete luxury visual design pack for the brand “Performance Club” — a futuristic intellectual club where speech, thought, sound and aesthetics become a visual language.
The result should include:
premium 3D abstract figures
sculptural floating objects
atmospheric backgrounds
luxury graphic elements
editorial posters
futuristic stickers
typography compositions
sound-inspired visual abstractions
experimental layout objects
translucent interface sculptures
visualized speech forms
modern artistic compositions for website sections and social media
The visual system must feel like:
a luxury intellectual movement
a sensory gallery installation
a fashion-tech editorial campaign
a digital philosophy exhibition
a futuristic private members club
VERY IMPORTANT:
Use ONLY Russian typography.
Integrate short Russian phrases naturally into the visuals as part of the composition.
The text should feel:
cinematic
conceptual
emotionally intelligent
spatial
premium
minimal
deeply art directed
Use phrases inspired by the Performance Club texts:
«Культура речи становится культурой мышления»
«Речь становится стратегией»
«Смыслы — формой капитала»
«Мы формируем среду, а не поток»
«Речь — это маркер уровня мышления»
«Не все становятся участниками клуба»
«Здесь речь становится стратегией»
«Влиять. Формировать. Усиливать.»
«Слово как инструмент статуса»
«Интеллект имеет свет»
«Звук имеет форму»
«Точность звучания»
«Среда определяет уровень»
«Мы работаем с глубиной мышления»
«Эстетический интеллект»
«Частота мышления»
«Система восприятия»
«Глубина. Смысл. Речь.»
DO NOT overload compositions with text.
Typography should feel curated and gallery-like.
VISUAL STYLE:
Ultra-premium CGI editorial aesthetic, futuristic luxury abstraction, sculptural minimalism, contemporary art direction, atmospheric typography, soft volumetric lighting, experimental graphic design, cinematic layout composition, tactile gradients, translucent materials, soft architectural depth, gallery installation atmosphere, luxury digital brutalism, visualized intelligence, emotional minimalism.
COLOR SYSTEM:
Use the color atmosphere from Image 1 and Image 2, but reinterpret it into:
softer transitions
smoother gradients
volumetric blending
atmospheric diffusion
pearl-like depth
cinematic texture transitions
The gradients must feel:
fluid
layered
expensive
soft
breathable
luminous
emotionally deep
Avoid:
sharp rainbow transitions
harsh color switching
oversaturated neon
cheap holographic gradients
generic AI blobs
The colors should melt naturally through:
translucent fog
liquid reflections
pearl diffusion
soft chromatic shadows
atmospheric light behavior
MATERIALS:
frosted glass
liquid acrylic
translucent pearl
soft chrome
smoked crystal
matte ceramic
silk reflections
volumetric haze
DESIGN ELEMENTS TO GENERATE:
Floating sound sculptures
Abstract speech waveforms
Luxury futuristic stickers
Editorial typography posters
Atmospheric gradient backgrounds
Minimal brutalist compositions
Sculptural interface objects
Liquid light forms
Spatial text compositions
Resonance-inspired geometry
Glass typography objects
Conceptual fashion-tech posters
Soft frequency abstractions
Gallery-style digital compositions
Experimental luxury graphic systems
TYPOGRAPHY STYLE:
Russian typography only.
Elegant spacing.
Minimal typography.
Editorial hierarchy.
Modern brutalist fashion layout.
Mix of:
tiny typography
oversized phrases
isolated words
vertical text blocks
floating captions
architectural composition
LIGHTING:
cinematic studio lighting
soft atmospheric glow
volumetric diffusion
premium shadows
elegant reflections
deep spatial light
museum-grade illumination
COMPOSITION:
strong negative space
asymmetrical layouts
floating balance
editorial rhythm
premium minimalism
highly photogenic framing
luxury visual hierarchy
THE RESULT SHOULD LOOK LIKE:
a futuristic luxury exhibition
a visual philosophy system
a premium fashion-tech campaign
Apple x Gentle Monster x TeamLab x high-end editorial design
conceptual branding for an intellectual private club from the future
NOT:
startup graphics
cyberpunk
generic AI art
dribbble blobs
gaming visuals
random gradients
cheap holographic textures
social media template aesthetics
The final result must feel:
calm, intelligent, sensory, minimal, luxurious, conceptual, emotional and unforgettable.` },
    { id: "10:376", text: `клиент прислала такие референсы для дизайн элементов. Сделай мне дизайн пак из 3д фигур, фонов, абстракций и дизайн элементов, чтобы я смогла добавить это на сайт` },
    { id: "10:389", text: `Use the final approved house image as the EXACT architectural and realism reference.
Use photo 2 as the EXACT CLOSE-UP TECHNICAL REFERENCE for the facade lighting design and lighting details.
IMPORTANT:
the lighting in the final image must match photo 2 with near 100% technical accuracy.
Create an ultra photorealistic cinematic close-up of the triangular roof edge and facade lighting during winter night.
Composition:
close detailed view of the roof corner
illuminated facade occupies about 40–50% of frame
remaining frame is blurred dark forest and sky
large cinematic negative space
asymmetrical composition
VERY IMPORTANT:
strictly preserve the EXACT technical structure of the lighting from photo 2:
identical fringe density
identical hanging pattern
identical bulb spacing
identical bulb scale
identical cable thickness
identical neon strip placement
identical proportions
identical installation logic
identical lighting geometry
The lighting must feel:
physically real
professionally mounted
architecturally accurate
engineered, not decorative
IMPORTANT:
visible individual bulbs are CRITICAL.
Each bulb must remain:
sharp
separated
realistically exposed
physically believable
NO:
glowing blobs
oversized bulbs
fantasy glow
simplified garlands
blurry lighting
random hanging patterns
Focus on:
ultra detailed roof materials
realistic snow texture
subtle warm reflections
physically accurate light falloff
realistic winter moisture
authentic low-light detail retention
Background:
dark forest
heavily blurred
low contrast
cinematic
text-safe negative space
Lens behavior:
telephoto cinema lens
shallow depth of field
realistic optical compression
cinematic focus falloff
subtle anamorphic lens behavior
The image must feel like a REAL luxury architectural photograph shot on ARRI Alexa LF during winter night.
Ultra photorealistic 4K realism.
Avoid:
AI artifacts, CGI appearance, render aesthetic, fake HDR, melted snow, blurry bulbs, distorted fringe, glowing haze, oversharpening, synthetic lighting, fantasy atmosphere.` },
    { id: "10:398", text: `Use the approved final house image as the EXACT realism and architectural reference.
Create a distant atmospheric winter shot of the illuminated house deep within the forest.
Composition:
house appears smaller in frame
most of image occupied by dark snowy forest
cinematic negative space
realistic environmental depth
Environment:
realistic pine forest
layered snowy trees
subtle atmospheric haze
authentic winter darkness
untouched snow texture
Lighting:
warm glowing facade lighting visible through forest
subtle illuminated pine trees
realistic window glow
restrained cinematic brightness
Lens behavior:
telephoto compression
atmospheric depth separation
realistic focus plane
cinematic low-light photography
The image must feel like a real photographed countryside house hidden in a winter forest.
Avoid CGI look, glowing haze, fake snow, AI artifacts, render aesthetic.` },
    { id: "10:407", text: `Use the approved final house image as the EXACT realism and architectural reference.
Create a cinematic ultra photorealistic wide establishing shot of the house during winter evening.
Composition:
house positioned on the RIGHT side of frame
LEFT side remains mostly empty dark forest and sky
large cinematic negative space for typography
asymmetrical composition
realistic snowy foreground
IMPORTANT:
preserve the exact architecture, roofline, facade lighting, illuminated trees and landscape lighting from the original image.
Environment:
realistic snowy Moscow-region forest
subtle snow imperfections
realistic footprints
atmospheric winter darkness
natural forest depth
Lighting:
realistic warm facade lighting
visible individual bulbs
subtle reflections on snow
realistic illuminated pine trees
soft warm window glow
Lens behavior:
cinematic telephoto compression
shallow depth of field
realistic focus falloff
atmospheric bokeh
The image must feel like a real luxury architectural film still photographed on ARRI Alexa LF.
Avoid CGI look, AI artifacts, glowing haze, fake HDR, oversharpening.` },
    { id: "10:416", text: `Use the final approved house image as the EXACT architectural and realism reference.
Create an ultra photorealistic cinematic wide shot of the house during winter evening.
Composition:
house slightly to the right
realistic dark forest surrounding the house
large snowy foreground
subtle atmospheric depth
elegant cinematic negative space
IMPORTANT:
preserve the exact architecture, roofline, lighting design, forest structure and realism from the original image.
Lighting:
realistic warm facade lighting
visible individual bulbs
subtle reflections on snow
realistic warm window glow
restrained cinematic brightness
Environment:
realistic snowy Moscow-region countryside
authentic pine trees
natural winter darkness
subtle snow imperfections
realistic footprints and compressed snow
The image must feel like a real photographed luxury countryside villa captured on ARRI Alexa LF.
Ultra realistic cinematic realism, natural low-light exposure, realistic grain, no CGI look, no AI artifacts.` },
    { id: "10:425", text: `Use the final approved house image as the EXACT architectural and realism reference.
Use photo 2,3 as the EXACT CLOSE-UP TECHNICAL REFERENCE for the facade lighting design and lighting details.
IMPORTANT:
the lighting in the final image must match photo 2 with near 100% technical accuracy.
Create an ultra photorealistic cinematic close-up of the triangular roof edge and facade lighting during winter night.
Composition:
close detailed view of the roof corner
illuminated facade occupies about 40–50% of frame
remaining frame is blurred dark forest and sky
large cinematic negative space
asymmetrical composition
VERY IMPORTANT:
strictly preserve the EXACT technical structure of the lighting from photo 2:
identical fringe density
identical hanging pattern
identical bulb spacing
identical bulb scale
identical cable thickness
identical neon strip placement
identical proportions
identical installation logic
identical lighting geometry
The lighting must feel:
physically real
professionally mounted
architecturally accurate
engineered, not decorative
IMPORTANT:
visible individual bulbs are CRITICAL.
Each bulb must remain:
sharp
separated
realistically exposed
physically believable
NO:
glowing blobs
oversized bulbs
fantasy glow
simplified garlands
blurry lighting
random hanging patterns
Focus on:
ultra detailed roof materials
realistic snow texture
subtle warm reflections
physically accurate light falloff
realistic winter moisture
authentic low-light detail retention
Background:
dark forest
heavily blurred
low contrast
cinematic
text-safe negative space
Lens behavior:
telephoto cinema lens
shallow depth of field
realistic optical compression
cinematic focus falloff
subtle anamorphic lens behavior
The image must feel like a REAL luxury architectural photograph shot on ARRI Alexa LF during winter night.
Ultra photorealistic 4K realism.
Avoid:
AI artifacts, CGI appearance, render aesthetic, fake HDR, melted snow, blurry bulbs, distorted fringe, glowing haze, oversharpening, synthetic lighting, fantasy atmosphere.` },
    { id: "10:434", text: `Use photo 1 as the exact base image and realism reference.
Carefully enhance the existing scene without redesigning the composition or architecture.
IMPORTANT:
preserve the exact house, forest, roofline, facade lighting and overall atmosphere from the original image.
Add subtle realistic warm fringe lighting onto the pine tree near the house using the SAME lighting style as the roof:
identical bulb size
identical spacing
identical warm tone
identical lighting texture
visible individual bulbs
realistic mounting and proportions
Add a very soft cool blue interior glow from the lower windows:
subtle cyan-blue tone
elegant and natural
not saturated
soft realistic window emission
The blue window light should softly reflect onto the nearby snow around the house.
The warm tree lighting should also create subtle warm reflections on the snow:
gentle
realistic
physically believable
very restrained
Add light realistic footsteps in the snow near the house:
subtle
natural
slightly imperfect
physically believable
Increase overall realism and detail:
sharper pine tree textures
detailed snowy branches
realistic snow surface texture
sharper facade materials
realistic wood, brick and glass textures
authentic low-light detail retention
VERY IMPORTANT:
preserve the exact technical lighting quality from the references:
exact fringe proportions
realistic bulb visibility
sharp individual bulbs
no glowing blobs
no distorted lighting geometry
The image must remain:
ultra photorealistic
cinematic
physically realistic
like a real photographed luxury countryside house in winter
Avoid:
AI artifacts, melted trees, fake HDR, glowing haze, oversharpening, orange lighting, CGI look, distorted fringe, blurry bulbs, synthetic snow, render aesthetic, overprocessed contrast.` },
    { id: "10:443", text: `сделай фигуры с фото 1 в оттенках с фото 2 в формате HEX` },
    { id: "10:456", text: `Create a Sims 4 promotional render scene.

CHARACTER REFERENCE — Photo 1:
Use the girls from photo 1 as character references.
Preserve their appearance, hair, outfits and overall
Sims 4 aesthetic from photo 1.
There are exactly 3 girls in the scene.

COMPOSITION REFERENCE — Photo 2:
Use photo 2 as the strict composition and camera reference.
Same aerial top-down camera angle — shot from far above,
looking straight down or at a steep downward angle.
Same scale: characters appear small relative to the scene.
Same sense of vast open space around them.

SCENE:
Three girls sitting on a large blanket on the edge 
of a dramatic rocky cliff plateau, working together —
laptops open, notebooks and cozy items around the blanket.
The cliff drops sharply into a sea of clouds below.

ENVIRONMENT:
Rocky cliff edge with patches of green grass and dirt.
Left side drops into dramatic volumetric clouds below.
Small rustic wooden structure visible in far background.
Right side: grassy slope continuing upward.

LIGHTING — strictly match photo 2:
Late golden hour transitioning into dusk.
Sky is dark, moody, dramatic — deep amber,
burnt orange an` },
    { id: "10:465", text: `Turn the girl from photo 1 into a Sims 4 character.
Keep the SAME face, SAME facial features, SAME expression, 
SAME hairstyle, SAME background and SAME overall 
composition from photo 1.

Do NOT redesign the person or change the scene.
Do NOT make it photorealistic.

Transform the image into:
official Sims 4 / EA Games style render, 
semi-realistic game character aesthetic.

Use photo 2 ONLY as inspiration for the outfit idea 
and styling direction.
Recreate the outfit in a more creative Sims-style version 
that fits the Sims universe.

Important:
— preserve facial identity,
— preserve original background and atmosphere,
— preserve pose and framing,
— preserve hair color and length,
— hair tucked behind the RIGHT ear only,
  the left side falls naturally and loosely,
  a single strand or two may fall across the face,
  the tuck sits close to the head, clean and intentional,
  not a full updo — just one side pinned back,
  Sims 4 hair strand detail preserved,
— realistic Sims-style skin texture,
— detailed Sims hair strands,
— Sims-style rendering and shading.

Style:
The Sims 4 promotional render, EA Games aesthetic, 
semi-realistic character render, stylized game textures, 
soft cinematic lighting.

Avoid:
photorealism, generic AI face, cartoon style, Pixar style, 
anime style, plastic CGI skin, beauty filter, 
mobile game aesthetic, changing the person or background,
do NOT leave hair fully down o` },
    { id: "10:474", text: `turn the girl from photo 1 into a Sims 4 character.
Keep the SAME face, SAME facial features, SAME expression, SAME hairstyle, SAME background and SAME overall composition from photo 1.

Do NOT redesign the person or change the scene.
Do NOT make it photorealistic.

Transform the image into:
official Sims 4 / EA Games style render, semi-realistic game character aesthetic.

Use photo 2 ONLY as inspiration for the outfit idea and styling direction.
Recreate the outfit in a more creative Sims-style version that fits the Sims universe.

Important:
— preserve facial identity,
— preserve original background and atmosphere,
— preserve pose and framing,
— preserve hair color and length,
— soft one-side tucked hair,
— realistic Sims-style skin texture,
— detailed Sims hair strands,
— Sims-style rendering and shading.

Style:
The Sims 4 promotional render, EA Games aesthetic, semi-realistic character render, stylized game textures, soft cinematic lighting.

Avoid:
photorealism, generic AI face, cartoon style, Pixar style, anime style, plastic CGI skin, beauty filter, mobile game aesthetic, changing the person or background.` },
    { id: "10:483", text: `Добавь к двум девушкам из Симс третью, чтобы она сидела рядом с ноутбуком и тоже внимательно работала. Соедини этих девушек в эстетичный кадр Sims  игры` },
    { id: "10:492", text: `сделай ее персонажем из Sims 4 ` },
    { id: "10:501", text: `Соедини девушку 1 и девушку 2 из Игры симс в каждре, где они вместе сидят на траве в игре Симс и работают в ноутбуках на проектами. Эстетика игры Симс на фото 3 ` },
    { id: "10:510", text: `Photo 1 is the reference image.
Keep EVERYTHING from photo 1 exactly as is:
same background, same scene, same composition, 
same lighting, same atmosphere, same number of people,
same poses, same positions of all characters.

Change ONLY one thing:
the girl in the brown dress — redress her in the outfit 
from photo 2. This is her new style.

Keep her face, hair, body proportions, 
and position in the scene completely unchanged.
Only swap the clothing.

Do NOT remove any people from the scene.
Do NOT change the background.
Do NOT change the composition.
Do NOT move any characters.
Do NOT change hairstyles.
Do NOT make it more or less realistic than photo 1.

Style: match the exact visual style and rendering 
quality of photo 1.` },
    { id: "10:519", text: `сделай ее персонажем из Sims 4 стоящей в лесу на фоне голубого неба. Кадр по пояс ` },
    { id: "10:528", text: `Сделай темно коричневый  на корнях  волос чуть темнее блонд по всей длине волос
` },
    { id: "10:537", text: `делай cinematic storyboard для персонажа из Sims 4 — Элианоры.
Она веб-дизайнер, businesswoman, creative director и travel-girl с эстетикой творческой свободы.

Главный вайб:
ностальгия по лету, путешествиям, свободе, красивым пейзажам и жизни креативного человека.

Стиль:
semi-realistic Sims 4 aesthetic, cinematic game render, soft dreamy lighting, realistic textures, cozy luxury atmosphere.

Покажи 8–10 cinematic сцен из её жизни:

— работает за ноутбуком на фоне гор,
— сидит летом в поле с ноутбуком и мудбордом,
— идёт по лесной тропе в aesthetic outfit,
— встречает закат у моря,
— работает в уютном доме среди природы,
— делает дизайн ночью при мягком свете,
— собирает референсы в красивом travel-cafe,
— едет в машине через лес или горы,
— отдыхает у озера с ноутбуком и идеями,
— проводит creative brainstorm на природе.

Очень важно:
во всех сценах сохранить одного и того же персонажа, её внешность и стиль.

Пейзажи должны быть красивыми, атмосферными и кинематографичными:
летние поля, леса, горы, море, туман, golden hour, природа, travel aesthetic.

Персонаж должен органично выглядеть внутри мира и локаций, а не быть “вставленным” поверх фона.

Атмосфера:
Sims 4 × A24 × Pinterest travel girl × creative entrepreneur × nostalgic summer indie movie.

Избегай:
corporate vibe, plastic CGI skin, mobile game aesthetic, empty generic backgrounds, over-saturated colors.` },
    { id: "10:546", text: `сделай ее персонажем из Sims 4 стоящей в лесу на фоне голубого неба. Кадр по пояс ` },
    { id: "10:555", text: `сделай корни и пряди волос чуть  темнее ` },
    { id: "10:568", text: `Create a Sims 4 promotional render scene.

CHARACTER REFERENCE — Photo 1:
Use the girls from photo 1 as character references.
Preserve their appearance, hair, outfits and overall
Sims 4 aesthetic from photo 1.
There are exactly 3 girls in the scene.

COMPOSITION REFERENCE — Photo 2:
Use photo 2 as the strict composition and camera reference.
Same aerial top-down camera angle — shot from far above,
looking straight down or at a steep downward angle.
Same scale: characters appear small relative to the scene.
Same sense of vast open space around them.

SCENE:
Three girls sitting on a large blanket on the edge 
of a dramatic rocky cliff plateau, working together —
laptops open, notebooks and cozy items around the blanket.
The cliff drops sharply into a sea of clouds below.

ENVIRONMENT:
Rocky cliff edge with patches of green grass and dirt.
Left side drops into dramatic volumetric clouds below.
Small rustic wooden structure visible in far background.
Right side: grassy slope continuing upward.

LIGHTING — strictly match photo 2:
Late golden hour transitioning into dusk.
Sky is dark, moody, dramatic — deep amber,
burnt orange an` },
    { id: "10:577", text: `Turn the girl from photo 1 into a Sims 4 character.
Keep the SAME face, SAME facial features, SAME expression, 
SAME hairstyle, SAME background and SAME overall 
composition from photo 1.

Do NOT redesign the person or change the scene.
Do NOT make it photorealistic.

Transform the image into:
official Sims 4 / EA Games style render, 
semi-realistic game character aesthetic.

Use photo 2 ONLY as inspiration for the outfit idea 
and styling direction.
Recreate the outfit in a more creative Sims-style version 
that fits the Sims universe.

Important:
— preserve facial identity,
— preserve original background and atmosphere,
— preserve pose and framing,
— preserve hair color and length,
— hair tucked behind the RIGHT ear only,
  the left side falls naturally and loosely,
  a single strand or two may fall across the face,
  the tuck sits close to the head, clean and intentional,
  not a full updo — just one side pinned back,
  Sims 4 hair strand detail preserved,
— realistic Sims-style skin texture,
— detailed Sims hair strands,
— Sims-style rendering and shading.

Style:
The Sims 4 promotional render, EA Games aesthetic, 
semi-realistic character render, stylized game textures, 
soft cinematic lighting.

Avoid:
photorealism, generic AI face, cartoon style, Pixar style, 
anime style, plastic CGI skin, beauty filter, 
mobile game aesthetic, changing the person or background,
do NOT leave hair fully down o` },
    { id: "10:586", text: `turn the girl from photo 1 into a Sims 4 character.
Keep the SAME face, SAME facial features, SAME expression, SAME hairstyle, SAME background and SAME overall composition from photo 1.

Do NOT redesign the person or change the scene.
Do NOT make it photorealistic.

Transform the image into:
official Sims 4 / EA Games style render, semi-realistic game character aesthetic.

Use photo 2 ONLY as inspiration for the outfit idea and styling direction.
Recreate the outfit in a more creative Sims-style version that fits the Sims universe.

Important:
— preserve facial identity,
— preserve original background and atmosphere,
— preserve pose and framing,
— preserve hair color and length,
— soft one-side tucked hair,
— realistic Sims-style skin texture,
— detailed Sims hair strands,
— Sims-style rendering and shading.

Style:
The Sims 4 promotional render, EA Games aesthetic, semi-realistic character render, stylized game textures, soft cinematic lighting.

Avoid:
photorealism, generic AI face, cartoon style, Pixar style, anime style, plastic CGI skin, beauty filter, mobile game aesthetic, changing the person or background.` },
    { id: "10:595", text: `Добавь к двум девушкам из Симс третью, чтобы она сидела рядом с ноутбуком и тоже внимательно работала. Соедини этих девушек в эстетичный кадр Sims  игры` },
    { id: "10:604", text: `сделай ее персонажем из Sims 4 ` },
    { id: "10:613", text: `Соедини девушку 1 и девушку 2 из Игры симс в каждре, где они вместе сидят на траве в игре Симс и работают в ноутбуках на проектами. Эстетика игры Симс на фото 3 ` },
    { id: "10:622", text: `Photo 1 is the reference image.
Keep EVERYTHING from photo 1 exactly as is:
same background, same scene, same composition, 
same lighting, same atmosphere, same number of people,
same poses, same positions of all characters.

Change ONLY one thing:
the girl in the brown dress — redress her in the outfit 
from photo 2. This is her new style.

Keep her face, hair, body proportions, 
and position in the scene completely unchanged.
Only swap the clothing.

Do NOT remove any people from the scene.
Do NOT change the background.
Do NOT change the composition.
Do NOT move any characters.
Do NOT change hairstyles.
Do NOT make it more or less realistic than photo 1.

Style: match the exact visual style and rendering 
quality of photo 1.` },
    { id: "10:631", text: `сделай ее персонажем из Sims 4 стоящей в лесу на фоне голубого неба. Кадр по пояс ` },
    { id: "10:640", text: `Сделай темно коричневый  на корнях  волос чуть темнее блонд по всей длине волос
` },
    { id: "10:649", text: `делай cinematic storyboard для персонажа из Sims 4 — Элианоры.
Она веб-дизайнер, businesswoman, creative director и travel-girl с эстетикой творческой свободы.

Главный вайб:
ностальгия по лету, путешествиям, свободе, красивым пейзажам и жизни креативного человека.

Стиль:
semi-realistic Sims 4 aesthetic, cinematic game render, soft dreamy lighting, realistic textures, cozy luxury atmosphere.

Покажи 8–10 cinematic сцен из её жизни:

— работает за ноутбуком на фоне гор,
— сидит летом в поле с ноутбуком и мудбордом,
— идёт по лесной тропе в aesthetic outfit,
— встречает закат у моря,
— работает в уютном доме среди природы,
— делает дизайн ночью при мягком свете,
— собирает референсы в красивом travel-cafe,
— едет в машине через лес или горы,
— отдыхает у озера с ноутбуком и идеями,
— проводит creative brainstorm на природе.

Очень важно:
во всех сценах сохранить одного и того же персонажа, её внешность и стиль.

Пейзажи должны быть красивыми, атмосферными и кинематографичными:
летние поля, леса, горы, море, туман, golden hour, природа, travel aesthetic.

Персонаж должен органично выглядеть внутри мира и локаций, а не быть “вставленным” поверх фона.

Атмосфера:
Sims 4 × A24 × Pinterest travel girl × creative entrepreneur × nostalgic summer indie movie.

Избегай:
corporate vibe, plastic CGI skin, mobile game aesthetic, empty generic backgrounds, over-saturated colors.` },
    { id: "10:658", text: `сделай ее персонажем из Sims 4 стоящей в лесу на фоне голубого неба. Кадр по пояс ` },
    { id: "10:667", text: `сделай корни и пряди волос чуть  темнее ` },
  ];

  for (const u of updates) {
    const node = figma.getNodeById(u.id);
    if (!node || node.type !== "TEXT") continue;
    node.characters = u.text;
    node.textAutoResize = "HEIGHT";
    // Подгоняем высоту родительской карточки
    const card = node.parent;
    if (card && card.type === "FRAME") {
      const newH = node.y + node.height + 40;
      if (newH > card.height) card.resize(card.width, newH);
    }
    fixed++;
  }

  figma.viewport.scrollAndZoomIntoView(page.children.filter(n => n.x >= 4400));
  return `Обновлено ${fixed} промптов из ${updates.length}`;
})();