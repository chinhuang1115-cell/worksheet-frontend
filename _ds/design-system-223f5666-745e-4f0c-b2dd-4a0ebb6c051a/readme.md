# 易數教室 Design System

> **易數教室** (YiShu Classroom) — a Traditional Chinese mathematics education platform serving students and teachers across three digital products.

## Sources

This design system was built **from scratch** — no external codebase, Figma file, or brand assets were provided. The system is derived entirely from the brand name and product description supplied by the team. If you have existing source materials (Figma links, a codebase repo, logo SVGs, brand guidelines), please share them to refine the token values, component behaviors, and visual identity.

---

## Products

### 1. Teacher Dashboard
**Surface:** Desktop web (1280px+, responsive)
**Audience:** Math teachers managing one or more classes
**Core flows:** Class overview → student progress → assignment review → grade analysis
**UI kit:** `ui_kits/teacher_dashboard/index.html`

### 2. Student App
**Surface:** Mobile-first web (390px), progressive
**Audience:** Junior high students (grades 7–9)
**Core flows:** Home → today's tasks → exercise practice → achievements
**UI kit:** `ui_kits/student_app/index.html`

### 3. Video Platform
**Surface:** Desktop/tablet web (1280px)
**Audience:** Students watching recorded course lessons
**Core flows:** Course browse → video player → chapter navigation → progress tracking
**UI kit:** `ui_kits/video_platform/index.html`

---

## Content Fundamentals

### Language
- Primary: **Traditional Chinese (繁體中文)**. All UI copy, labels, and help text in zh-TW.
- Numbers: Always **Arabic numerals** (1, 2, 3) for data and statistics. Chinese numerals (一, 二, 三) only in ordinal prose ("第一課").
- Mixed: Subject names and chapter titles stay in Chinese; math expressions use Latin notation (`x`, `f(x)`, `ax + b = 0`).

### Tone
| Surface | Tone | Pronoun | Example |
|---|---|---|---|
| Student-facing | Warm, encouraging, celebratory | 你 (informal) | 「做得很棒！繼續加油！」 |
| Teacher-facing | Professional, efficient, data-forward | 您 (formal in onboarding) / 你 in everyday labels | 「本週待批改作業：15 份」 |
| Error messages | Clear, non-blaming | — | 「學號格式不正確，請輸入 6 位數字」 |

### Casing
- **Navigation / headings:** Title case in Chinese (natural, no special treatment needed)
- **ALL CAPS:** Never use for Chinese text. Acceptable only for English abbreviations (CTA labels, metadata codes)
- **Sentence case:** All body text, hint copy, tooltips

### Terminology (use consistently)
| Term | Chinese |
|---|---|
| Class | 班級 |
| Course / Curriculum | 課程 |
| Unit / Chapter | 單元 |
| Exercise | 練習題 |
| Homework / Assignment | 作業 |
| Progress | 進度 |
| Grade / Score | 成績 / 分數 |
| Teacher | 老師 |
| Student | 學生 / 同學 |

### Emoji
Not used in UI chrome or body copy. Reserved for celebratory micro-moments in student-facing contexts only (achievement unlocks, perfect scores).

---

## Visual Foundations

### Colors

**數藍 (Shù Lán) — Brand Blue** — `oklch(0.515 0.240 258)`
The primary brand color. Conveys trust, focus, and academic seriousness. Used for interactive elements (buttons, links, active states), brand moments, and the teacher sidebar. Full scale: `--color-brand-50` → `--color-brand-950`.

**琥珀 (Hǔ Pò) — Accent Amber** — `oklch(0.730 0.165 58)`
Warm, energetic counterpoint to the cool brand blue. Used for gamification elements (points, streaks, achievements), student-facing CTAs, and highlights. Full scale: `--color-accent-50` → `--color-accent-950`.

**暖灰 (Nuǎn Huī) — Neutral Warm Gray**
All backgrounds, borders, and body text. Subtly warm (slight hue toward brand blue) so it harmonizes rather than clashes. `neutral-0` = white; `neutral-950` = near-black.

**Semantic:** success (green 145°), warning (amber 75°), error (red 25°), info (sky 220°).

### Typography

| Role | Family | Weights |
|---|---|---|
| Display / headings / brand | Noto Serif TC | 600, 700 |
| Body / UI / labels | Noto Sans TC | 400, 500, 700 |
| Math / numbers / scores | JetBrains Mono | 400, 500 |

- **Line height for TC body copy:** `1.8` — Chinese characters need more vertical air than Latin text
- **Letter spacing for display headings:** `0.06–0.12em` — adds elegance to large Chinese type
- **Minimum body size:** 14px (`--text-sm`) for any reading-weight copy

> **Font substitution note:** These are Google Fonts. For production, consider licensed equivalents such as Hiragino Sans GB (macOS) or the full Noto CJK family for broader weight coverage. See `tokens/fonts.css`.

### Spacing
4px base unit. Standard container padding: `24px` (`--space-6`). Card-to-card gap: `12–16px`. Section headers to content: `12px`. Page section gap: `24px`.

### Backgrounds
- **Primary surfaces:** white (`--bg-base`)
- **Secondary / sidebar:** `--bg-subtle` (neutral-50)
- **Active/selected tint:** `--color-brand-50`
- Never use full-bleed gradients in data-dense layouts. The teacher sidebar is the only dark surface (brand-800).

### Cards
- **Variant `raised`:** white bg + `1px neutral-200` border + `--shadow-sm`
- **Variant `bordered`:** white bg + `1.5px neutral-300` border, no shadow
- **Variant `flat`:** neutral-50 bg, no border or shadow (inner sub-sections)
- **Corner radius:** `--radius-xl` (16px) for main content cards; `--radius-md` (8px) for compact cards and chips

### Hover & Press States
- **Primary button:** one shade darker on brand scale + brand glow shadow on hover; two shades darker + `scale(0.975)` on press
- **Card (interactive):** `translateY(-1px)` + shadow step up on hover; transition `150ms ease-out`
- **Nav items:** opacity shift from 55% → 100% white on active
- **Inputs:** brand-500 border + 3px brand-100 ring on focus

### Borders
- `1px` for cards and dividers; `1.5px` for interactive inputs and outlined buttons
- Default color: `--border-subtle` (neutral-200) for cards, `--border-default` (neutral-300) for inputs

### Shadows
All shadows are tinted with brand hue 258° at low chroma — they feel cohesive rather than generic black shadows. `--shadow-brand` and `--shadow-accent` are glow shadows reserved for primary hover states and achievement moments only.

### Animations
- **Default:** `150ms ease-out` — all hover/focus transitions
- **Micro-interactions (button press, checkmark):** `250ms ease-spring` — slight overshoot for tactile feel
- **Content reveal / panels:** `400ms ease-smooth`
- **Always respect:** `@media (prefers-reduced-motion)` — collapse all animations to instant

### Corner Radii
`xs` 2px → `sm` 4px → `md` 8px → `lg` 12px → `xl` 16px → `2xl` 20px → `full` 9999px (pill)
Use `full` for badges, tags, and progress bars only.

### Imagery
Diagrams, coordinate planes, and mathematical figures as clean SVG. No stock photography. Geometric math illustrations in brand colors are preferred for empty states and onboarding. Avoid grain, texture, and photographic backgrounds.

---

## Iconography

**System:** [Lucide Icons](https://lucide.dev) — `stroke-width: 1.5`, size `20px` default, `16px` compact, `24px` navigation

**Load from CDN:**
```html
<!-- Vanilla (non-React pages) -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

For React UI kits, icons are inlined as SVG path components (see each `index.html` for the pattern).

**Key icon usage:**
| Context | Icon |
|---|---|
| Classes / dashboard | `Grid` |
| Students | `Users` |
| Courses | `BookOpen` |
| Assignments | `ClipboardCheck` |
| Analytics | `BarChart3` |
| Settings | `Settings` |
| Search | `Search` |
| Add / New | `Plus` |
| Progress / Trend | `TrendingUp` |
| Streak | `Flame` |
| Points | `Star` |
| Achievement | `Trophy` |

**Never use:**
- Emoji as icons
- Hand-drawn or custom SVGs for UI chrome
- Filled icon variants (always `fill="none"` stroke icons)

---

## File Index

```
易數教室 Design System
│
├── styles.css                 ← ENTRY POINT — @import this in any consumer
│
├── tokens/
│   ├── fonts.css              — @font-face + --font-* family tokens
│   ├── colors.css             — Full palette + semantic aliases
│   ├── typography.css         — --text-*, --weight-*, --leading-*, --tracking-*
│   ├── spacing.css            — --space-* scale (4px base)
│   ├── borders.css            — --radius-*, --border-* width
│   ├── shadows.css            — --shadow-* scale (brand-tinted)
│   └── motion.css             — --duration-*, --ease-*, --transition-*
│
├── components/core/
│   ├── Button.(jsx|d.ts|prompt.md)
│   ├── Card.(jsx|d.ts|prompt.md)
│   ├── Badge.(jsx|d.ts|prompt.md)
│   ├── Input.(jsx|d.ts|prompt.md)
│   ├── Avatar.(jsx|d.ts|prompt.md)
│   ├── Tag.(jsx|d.ts|prompt.md)
│   ├── ProgressBar.(jsx|d.ts|prompt.md)
│   └── core.card.html         — @dsCard: all 7 components at a glance
│
├── guidelines/
│   ├── brand-identity.card.html
│   ├── colors-brand.card.html
│   ├── colors-accent.card.html
│   ├── colors-neutral.card.html
│   ├── colors-semantic.card.html
│   ├── type-display.card.html
│   ├── type-body.card.html
│   ├── type-scale.card.html
│   ├── spacing.card.html
│   ├── borders-radius.card.html
│   ├── shadows.card.html
│   └── motion.card.html
│
├── ui_kits/
│   ├── teacher_dashboard/index.html   — 1280px interactive desktop dashboard
│   ├── student_app/index.html         — 390px mobile student home screen
│   └── video_platform/index.html     — 1280px video course player
│
├── readme.md                  ← You are here
└── SKILL.md                   — Agent skill definition
```

---

## Component Summary

| Component | Variants | Key Props |
|---|---|---|
| `Button` | primary, secondary, ghost, accent, danger | size, disabled, loading, icon, fullWidth |
| `Card` | raised, flat, bordered, brand, success, warning, error | padding, radius, interactive, selected |
| `Badge` | brand, accent, success, warning, error, info, neutral, dark | size, dot |
| `Input` | — | label, hint, error, size, prefix, suffix, required |
| `Avatar` | circle, rounded | size (xs–2xl), online, src |
| `Tag` | neutral, brand, accent, success, error | size, onRemove, icon, onClick |
| `ProgressBar` | brand, accent, success, warning, error | size (xs–xl), label, showValue, animated |
