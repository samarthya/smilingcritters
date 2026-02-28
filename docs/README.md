# 🐾 Smiling Critters — Design Documentation

This directory contains the full design documentation for the **Smiling Critters** project — a safe, joyful AI companion app for children.

---

## Contents

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | System architecture, module map, data flow |
| [critter-personas.md](critter-personas.md) | Design rationale for all 5 critter characters |
| [safety-system.md](safety-system.md) | Three-layer content safety architecture |
| [data-model.md](data-model.md) | SQLite schema, entities, and data lifecycle |
| [llm-routing.md](llm-routing.md) | LLM routing logic — Ollama + Gemini fallback |
| [ui-ux.md](ui-ux.md) | UI design system, theme, pages, component patterns |

---

## Design Philosophy

> **Every decision asks: does this make her feel safe, seen, and joyful?**

Smiling Critters is designed first and foremost for a specific child — a neurodivergent 7–8 year old — and only then generalised. This specificity is a feature, not a constraint.

### Core principles

1. **Safety above all** — a three-layer filter stops harmful content from ever reaching the child, at input *and* output
2. **Predictability** — each critter has a fixed, unwavering personality; no surprises
3. **Parent visibility** — every message, session, and safety flag is accessible to the parent
4. **Privacy-first** — local AI (Ollama) is preferred; cloud (Gemini) is opt-in fallback
5. **Joy-first** — this is a companion, not a tutoring tool; warmth always wins

---

## Project Phases

| Phase | Scope | Status |
|-------|-------|--------|
| **Phase 1** | Python / Streamlit prototype | ✅ Active |
| **Phase 2** | iOS app (SwiftUI + same backend) | 🗺️ Planned |
| **Phase 3** | Critter animations (Lottie), voice input | 🗺️ Planned |
| **Phase 4** | Guided breathing, emotion wheel (full) | 🗺️ Planned |
| **Phase 5** | TestFlight family beta | 🗺️ Planned |
