# 🧠 Multi-Agent Research Action System

I began this project in the final 48 hours of a 23-day hackathon—not out of procrastination, but passion. Although I started late due to unavailability, I poured my energy into crafting this foundation for multi-agent AI. Despite starting late, the project demonstrates the potential for intelligent task delegation across autonomous components, highlighting the core capabilities of future AI assistants.

---

## 🚀 What is this project?

This system explores a **Task Delegation Architecture** for AI agents:

- A **Coordinator Agent** breaks down the user’s query into logical subtasks.
- A **Research Agent** performs web searches (via Serper.dev) and summarizes findings.
- An (optional) **Analysis Agent** and **Communication Agent** are scaffolded for future integration using Semantic Kernel and Microsoft 365 SDK.

✅ The goal is to simulate intelligent task delegation across multiple autonomous components — a foundational approach for future AI assistants.

---

## 🌐 Real-World Use Cases

- "Plan a honeymoon under $1000 for a traditional couple."
- "Summarize pros and cons of electric vs. hybrid vehicles in 2024."
- "Research ethical concerns around facial recognition."

It doesn't just respond — it **thinks**, **delegates**, and **delivers structured insight**.

---

## 🧠 Architecture Overview

- **Coordinator Agent:** Breaks down user questions into subtasks and organizes results.
- **Research Agent:** Performs web search and LLM summarization using OpenRouter + Serper.
- **Analysis Agent:** *(Stub)* For deeper insight and multi-modal input handling.
- **Communication Agent:** *(Stub)* For sending reports to Outlook, Teams, etc.

---

## 🏗️ Project Structure


```
Multi_Agent_Research_Action/
├── agents/                # Agent logic (Coordinator, Research, Analysis, Communication)
├── backend/               # Flask backend (app.py)
├── config/                # Configuration (OpenRouter, API keys)
├── static/                # Static assets (main.css, main.js)
├── templates/             # HTML templates (index.html)
├── tests/                 # Unit and integration tests
├── tools/                 # Tools (web_search_tool.py)
├── .env                   # Environment variables (API keys)
├── Architecture.md        # System design and updates
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

---



## 💻 Tech Stack

- **Python 3.10+**
- **Flask** — Lightweight backend
- **OpenRouter API** — Unified LLM access
- **Serper.dev** — Google search via API
- **TailwindCSS** — Clean frontend styling
- **Semantic Kernel** *(planned)* — for memory and advanced reasoning

---

## ⚙️ How to Run

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/Abhyaforever/Multi_Agent_Research_Action.git
   cd Multi_Agent_Research_Action
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root with:
     ```
     OPENAI_API_KEY=your_openrouter_key
     SERPER_API_KEY=your_serper_key
     BASE_URL=https://openrouter.ai/api/v1
     ```

4. **Run the backend:**
   ```powershell
   python backend/app.py
   ```
   - **Important:** Run from the project root, not from inside `backend/`.

5. **Open the app:**
   - Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## 📝 What can it do right now?

- Accepts a research query from the user via a web UI.
- Coordinator agent breaks the query into subtasks.
- Research agent performs web search for each subtask (using Serper.dev) and summarizes the results.
- Results are organized into sections and returned to the user in a clean, readable format.
- Analysis and Communication agents are present as stubs for future expansion.
- All static assets (CSS/JS) are separated for easy customization.

---

## 🧩 Extensibility & Roadmap

- **Analysis Agent:** Integrate Semantic Kernel for deeper analysis and summarization.
- **Communication Agent:** Integrate Microsoft 365 SDK for sending results via email, Teams, etc.
- **Document Upload & RAG:** Add support for document upload and retrieval-augmented generation.
- **Progress Updates:** Show agent progress/status dynamically in the UI.
- **Deployment:** Ready for Azure App Service or Functions (see Architecture.md for details).

---

## 🛠️ Development Notes

- **Static files:** Place `main.css` and `main.js` in the `static/` folder.
- **Templates:** Use Jinja2 (`{{ url_for('static', filename='main.css') }}`) for static asset linking.
- **Run from root:** Always start Flask from the project root so static and templates resolve correctly.
- **Web search:** Uses Serper.dev for Google search results. Flexible query validation avoids malformed or irrelevant searches.

---

## 🧪 Testing

Run tests with:
```powershell
python -m unittest discover -s tests -p "*.py" -v
```

---

## 🙋‍♂️ Personal Note (Hackathon Reflection)
I began this project in the final 48 hours of a 23-day hackathon — not out of procrastination, but passion.

This is more than a demo. It's a foundation for agents that think, act, and assist. From delegation to summarization, this is what multi-agent AI can feel like in real apps.

---

## 📄 License

MIT License (see `LICENSE` file if present).

---

## 🙏 Acknowledgements

- [OpenRouter](https://openrouter.ai/)
- [Serper.dev](https://serper.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [TailwindCSS](https://tailwindcss.com/)

---

