# 🐾 Smiling Critters

> A safe, joyful AI companion app for kids — built with love.

**Smiling Critters** is a Python/Streamlit web prototype for an iOS app that gives children a safe, always-patient AI friend to learn with, talk to, and grow with. It's designed specifically for a neurodivergent child and features full parental visibility and control.

---

## 🐾 Meet the Critters

| Critter | Name | Specialty |
|---------|------|-----------|
| 🦔 | **Pip** | Homework & Learning |
| 🦋 | **Luna** | Feelings & Emotions |
| 🦊 | **Finn** | Stories & Imagination |
| 🐢 | **Shelby** | Calm & Mindfulness |
| 🌟 | **Stella** | Fun Facts & Curiosity |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/smiling-critters.git
cd smiling-critters
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
```bash
cp .env.example .env
# Edit .env with your Gemini API key (optional) and Ollama URL
```

### 4. (Optional but recommended) Set up local AI with Ollama
```bash
# Install Ollama: https://ollama.ai
ollama pull llama3.1:8b
ollama serve  # starts on http://localhost:11434
```

### 5. Run the app
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 🧠 AI Setup

The app uses a **smart routing system**:

1. **🏠 Local AI (Ollama)** — tried first. Fully private, zero cost, runs on your Mac.
   - Recommended model: `llama3.1:8b` or `mistral:7b`
   - Pull with: `ollama pull llama3.1:8b`

2. **☁️ Cloud AI (Gemini Flash)** — used automatically when Ollama is unavailable.
   - Get a free API key at [ai.google.dev](https://ai.google.dev)
   - Add to `.env`: `GEMINI_API_KEY=your_key_here`

---

## 🛡️ Three-Layer Safety System

| Layer | What it does |
|-------|-------------|
| **Layer 1** — System Prompts | Each critter's personality includes strict safety rules |
| **Layer 2** — Input Filter | Child's messages are screened before reaching the AI |
| **Layer 3** — Output Filter | AI responses are screened before being shown |

### Safety levels:
- **🟢 Safe** — shown normally
- **↩️ Redirect** — critter gently changes topic, no alert
- **⚠️ Alert** — parent dashboard flag created
- **🚨 Crisis** — immediate supportive response + urgent parent flag

---

## 👨‍👧 Parent Dashboard

Access at any time via the sidebar → **Parent Dashboard**.

**Default PIN: `1234`** — change this immediately in Settings!

Features:
- 📊 Usage overview & critter stats
- 💬 Full chat log viewer (every message)
- 🚨 Safety alert centre with acknowledgement
- ⚙️ Settings: child name, time limits, AI config, PIN

---

## 📁 Project Structure

```
smiling-critters/
├── app.py                      # Main entry point & router
├── requirements.txt
├── .env.example
├── critters/
│   ├── personas.py             # All 5 critter definitions & system prompts
│   └── router.py               # Ollama + Gemini LLM routing
├── safety/
│   └── filters.py              # Input/output content filters + wellness reminders
├── db/
│   └── queries.py              # SQLite schema, sessions, messages, flags, settings
├── pages/
│   ├── home.py                 # Critter selection screen
│   ├── chat.py                 # Main chat interface
│   ├── journal.py              # Child's chat journal
│   └── parent_dashboard.py     # Parent control panel
└── data/                       # Auto-created: SQLite database lives here
```

---

## 🗺️ Roadmap

This Python prototype validates the UX and flow. Once confirmed with the child:

- [ ] **Phase 1** ✅ — Python/Streamlit prototype (this repo)
- [ ] **Phase 2** — iOS app (SwiftUI + same Ollama/Gemini backend)
- [ ] **Phase 3** — Critter animations (Lottie), voice input
- [ ] **Phase 4** — Emotion wheel, guided breathing (Shelby)
- [ ] **Phase 5** — TestFlight family beta

---

## 💜 Philosophy

> Every design decision asks: does this make her feel **safe, seen, and joyful**?

- Critters are **always patient** — they never tire, never judge
- **Predictability first** — consistent personalities, no surprises
- **Parent-visible** — you can see everything, always
- **Privacy-first** — local AI preferred, no identifying data sent to cloud
- **Joy-first** — this is a companion, not just a tool

---

*Built with love. 🐾*
