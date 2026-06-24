---
name: DocuMind
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#464555'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#712ae2'
  on-secondary: '#ffffff'
  secondary-container: '#8a4cfc'
  on-secondary-container: '#fffbff'
  tertiary: '#7e3000'
  on-tertiary: '#ffffff'
  tertiary-container: '#a44100'
  on-tertiary-container: '#ffd2be'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#eaddff'
  secondary-fixed-dim: '#d2bbff'
  on-secondary-fixed: '#25005a'
  on-secondary-fixed-variant: '#5a00c6'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb695'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7b2f00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  code-sm:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style
The design system is engineered for an intelligent AI SaaS platform that bridges the gap between academic rigor and cutting-edge technology. The brand personality is poised, helpful, and sophisticated, aiming to evoke a sense of clarity and mental space for the user.

The visual style follows a **Refined Minimalist** approach. It leverages generous white space and high-quality typography to ensure focus on content, while integrating **Glassmorphism** and subtle gradients to signal its modern, AI-driven core. The aesthetic is inspired by the functional clarity of Notion and the conversational simplicity of ChatGPT, but elevated with a distinct editorial polish.

## Colors
This design system utilizes a sophisticated palette centered on deep Indigo and Purple to represent intelligence and innovation.

- **Primary & Secondary:** A vibrant Indigo (#4F46E5) serves as the main action color, often transitioning into a Deep Purple (#7C3AED) via linear gradients (135°) for high-impact moments or AI-specific features.
- **Neutrals:** The system uses Slate-900 (#0F172A) for primary text to ensure maximum readability against White (#FFFFFF) or Light Gray (#F8FAFC) backgrounds.
- **Accents:** Success, Warning, and Error states should use desaturated versions of green, amber, and red to maintain the professional, academic tone.

## Typography
The typography system prioritizes legibility and structure. **Inter** is the primary typeface, chosen for its neutral yet modern appearance and excellent performance in academic and technical contexts.

- **Scale:** Use tight letter-spacing for large headlines to maintain a "compact" and professional look. 
- **Hierarchy:** Use font weight (SemiBold/Bold) rather than size alone to distinguish hierarchy in dense information environments.
- **Technical Accents:** **Geist** is used for labels, metadata, and code snippets to provide a subtle "developer-tool" or "technical" aesthetic without disrupting the overall clean feel.

## Layout & Spacing
The design system employs a **Fluid Grid** model based on an 8px base unit. 

- **Desktop:** A 12-column grid with 24px gutters. Sidebars should be fixed at 280px for a "workspace" feel.
- **Mobile:** A 4-column grid with 16px margins.
- **Vertical Rhythm:** Use consistent padding (e.g., 16px, 24px, 48px) to separate content blocks. 
- **Alignment:** Content should be primarily left-aligned to mirror document and chat patterns, utilizing wide right-side margins for "AI assistant" overlays or annotations.

## Elevation & Depth
Depth is created through a combination of **Tonal Layers** and **Glassmorphism**.

- **Surfaces:** The base layer is #F8FAFC. Primary containers use #FFFFFF with a subtle 1px border (#E2E8F0).
- **Glassmorphism:** Headers, sidebars, and floating palettes utilize a `backdrop-filter: blur(12px)` with a semi-transparent white background (`rgba(255, 255, 255, 0.8)`).
- **Shadows:** Use "Soft XL" shadows for floating elements—highly diffused, low opacity (4-8%), with a slight indigo tint to prevent the UI from looking flat.

## Shapes
The shape language is friendly yet structured, utilizing large corner radii to soften the academic nature of the content.

- **Standard Elements:** Buttons and input fields use a 0.5rem (8px) radius.
- **Containers:** Main cards and modal overlays use `rounded-2xl` (1rem / 16px) to create a modern, app-like appearance.
- **AI Elements:** Special AI-driven components or "magic" buttons may use pill-shaped (full) rounding to distinguish them from standard functional UI.

## Components
- **Buttons:** 
  - *Primary:* Indigo/Purple gradient background, white text, subtle inner-glow.
  - *Secondary/Ghost:* Transparent background, slate-600 text, 1px border that becomes Indigo on hover.
- **Cards:** Clean white backgrounds, 1px slate-200 border, and `shadow-xl` on hover to indicate interactivity.
- **Input Fields:** Minimalist style with a subtle gray background. Upon focus, the border transitions to Indigo with a soft outer glow (ring).
- **Chips/Tags:** Small, light indigo background with dark indigo text for categorization and document metadata.
- **AI Sidebar:** A glassmorphic panel on the right side of the viewport with a blurred background to keep the main document visible but secondary.
- **Icons:** 2px stroke-width line icons. Use Indigo for active states and Slate-400 for inactive states.