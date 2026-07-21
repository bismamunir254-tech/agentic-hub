<div align="center">

<img src="https://img.icons8.com/?size=100&id=dJ46wPls9v2K&format=png" width="100" alt="AgentIQ Logo"/>

# 🤖 AgentIQ Hub
### Multi-Persona AI Chatbot powered by Groq + Streamlit

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq_AI-Powered-00F2FE?style=for-the-badge)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Deployed on Streamlit Cloud](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io)

**An advanced, production-ready AI chatbot web app** with 5 specialized personalities, real-time streaming, side-by-side agent comparison, live analytics, and session memory — all powered by the blazing-fast Groq inference API.

[🚀 Live Demo](#-live-demo) • [✨ Features](#-features) • [🎬 Demo Video](#-demo-video) • [📦 Installation](#-installation) • [☁️ Deploy](#️-deploy-to-streamlit-cloud) • [📁 Project Structure](#-project-structure)

</div>

---

## 🎬 Demo Video

> 📺 **Watch the full walkthrough on YouTube / Loom** *(Upload your screen recording and paste the URL below)*

[![AgentIQ Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://youtu.be/YOUR_VIDEO_ID)

> 🎯 **Click the thumbnail above** to watch the demo. The video covers:
> - Live chat with different AI personalities
> - Personality boundary enforcement (asking the wrong question!)
> - Side-by-side Agent Comparison Mode
> - Real-time analytics & chat export features

---

## 🚀 Live Demo

> 🌐 **Try it live** → [**https://your-app-name.streamlit.app**](https://your-app-name.streamlit.app)

*(Deploy to Streamlit Cloud and update this link)*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎭 **5 AI Personalities** | Math Teacher, Doctor, Travel Guide, Chef, Tech Support |
| 🔒 **Strict Domain Boundaries** | Each agent politely refuses out-of-scope questions |
| ⚡ **Real-time Streaming** | Token-by-token response streaming with live cursor |
| 🧠 **Session Memory** | Full conversation context maintained across the chat session |
| ⚔️ **Agent Comparison Mode** | Prompt two different personalities simultaneously, side-by-side |
| 📊 **Live Analytics** | Real-time response latency (ms), word count, and query counter |
| 💡 **Suggested Prompts** | 3 quick-start prompt buttons per personality |
| 📥 **Chat Export** | Download full conversation as Markdown or JSON |
| 🤖 **Multiple Groq Models** | Choose from Llama 3.3 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma 2 9B |
| 🎨 **Premium Dark UI** | Glassmorphism cards, gradient headings, Google Fonts, custom CSS |
| 🧪 **Prompt Sandbox** | Inspect and understand the exact system prompt rules for each agent |

---

## 🎭 AI Personalities

| Personality | Icon | Allowed Domain | Refused Topics | Response Style |
|---|---|---|---|---|
| **Math Teacher** | 📐 | Algebra, Calculus, Geometry, Logic | Anything non-math | LaTeX equations, step-by-step solutions |
| **Doctor** | 🩺 | Symptoms, Medicine, Anatomy, Wellness | Non-health queries | Structured medical disclaimers, bullet points |
| **Travel Guide** | ✈️ | Destinations, Itineraries, Packing Tips | Non-travel queries | Markdown tables with Day/Activity/Cost/Tips |
| **Chef** | 👨‍🍳 | Recipes, Cooking Techniques, Ingredients | Non-cooking queries | Prep time, ingredients list, numbered steps, Chef's Tip |
| **Tech Support** | 💻 | Hardware, Software, Networking, Debugging | Non-tech queries | Code blocks, step-by-step troubleshooting |

---

## 🧠 How Session Memory Works

AgentIQ Hub maintains a **full multi-turn conversation context** within each session. Here is the architecture:

```
User Message
      │
      ▼
 st.session_state.messages  ◄──── Stores every user + assistant turn
      │
      ▼
 api_messages = [system_prompt] + [all previous messages] + [new message]
      │
      ▼
 Groq API (streaming)
      │
      ▼
 Streamed Response ──► Appended to session_state.messages
```

- Each personality's **system prompt is prepended on every API call**, enforcing domain restrictions throughout the conversation.
- Switching personalities **clears the conversation context** to avoid cross-personality confusion.
- Clicking **"Clear Chat History"** resets the memory entirely.

---

## 🏗️ Project Structure

```
agentiq-hub/
│
├── app.py                    # Main Streamlit application
├── personalities.py          # AI personality definitions, system prompts & suggestions
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes secrets, cache, logs from Git
│
└── .streamlit/
    ├── config.toml           # Streamlit theme configuration (dark mode)
    └── secrets.toml.example  # Template for setting up your API key
```

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/agentiq-hub.git
cd agentiq-hub
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your Groq API Key
Get a **free** API key at [console.groq.com](https://console.groq.com/), then create the secrets file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Then edit .streamlit/secrets.toml and paste your key
```

### 5. Run Locally
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud

1. **Push your code to GitHub** (make sure `secrets.toml` is in `.gitignore`)
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** → **New App**
3. Select your repository, branch (`main`), and entry file (`app.py`)
4. In **App Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
5. Click **Deploy** — your app is live!

---

## 🤖 Available Groq Models

| Model | ID | Best For |
|---|---|---|
| Llama 3.3 70B Versatile | `llama-3.3-70b-versatile` | Complex reasoning, best quality |
| Llama 3.1 8B Instant | `llama-3.1-8b-instant` | Ultra-fast responses |
| Mixtral 8x7B | `mixtral-8x7b-32768` | Balanced reasoning & speed |
| Gemma 2 9B | `gemma2-9b-it` | Lightweight, efficient |

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Your Groq Cloud API key | Yes |

---

## 🛠️ Tech Stack

- **Python 3.9+** — Core language
- **Streamlit** — Web app framework with chat components
- **Groq Python SDK** — LLM inference API client
- **Groq Cloud** — Ultra-fast LPU-based AI inference
- **Custom CSS** — Glassmorphism, Google Fonts (Outfit), gradient effects

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙋 Author

**Bisma Munir**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/bisma-m-a9055b30a/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/bismamunir254-tech)

---

<div align="center">

**Star this repo if you found it useful! It helps others discover the project.**

*Built with love using Streamlit and Groq AI*

</div>
