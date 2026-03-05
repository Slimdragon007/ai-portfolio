# Case Study 04: Production HTML Artifacts
## The Prezi-Style Portfolio Site

---

## Problem

Most AI-generated code is demo-quality: it works in a sandbox but breaks in production. Can AI collaboration produce a polished, production-ready web application that rivals hand-coded work?

---

## Architecture

```
Design brief
    -> Claude architecture session
    -> iterative HTML/CSS/JS build
    -> responsive testing
    -> production artifact
    -> Build Vault logging with Resume Card
```

### Application Spec

- 5-slide Prezi-style camera-pan navigation
- Lateral panning on desktop, vertical on mobile
- Auto dark/light mode detection
- Swipe, keyboard, and dot navigation
- Custom typography (Poppins + Lora)
- Brand accent color system (#d97757 orange)

---

## Build Details

**Stack**: HTML5, CSS3, vanilla JavaScript, built entirely through Claude collaboration

### Slide Architecture

| Slide | Content | Position | Style |
|-------|---------|----------|-------|
| S1 | Mission statement | Center | Light |
| S2 | Who I Am | Right pan | Light |
| S3 | The Work | Below | Dark bg, 4-column grid |
| S4 | Skills | Left pan | Light |
| S5 | Contact | Center | Dark bg, zoom transition |

### What Makes It Different

- **Zero hand-coding**: the entire application was built through conversational AI collaboration. No IDE, no manual CSS debugging, no Stack Overflow.
- **Production-grade responsive**: not a demo. Full mobile-first responsive design with touch gestures, keyboard navigation, and viewport-aware layout switching.
- **Iterative refinement**: built across multiple sessions with the Build Vault's Resume Card enabling seamless continuation. Each session picked up exactly where the last left off.
- **Design system thinking**: consistent typography scale, color system, and spacing, not random AI-generated styling.

---

## Result

- Production-ready single-page application
- Multi-input navigation (swipe, keyboard, click)
- Responsive across all viewport sizes
- First artifact tracked in the Build Vault system
- Proof that AI collaboration can produce professional-grade frontend work

---

## Proof

The file (MichaelHaslim_FINAL.html) is archived in the Build Vault with full Resume Context. The build demonstrates that AI-assisted development can match the quality bar of traditional development workflows.

---

[Back to Portfolio](../README.md)
