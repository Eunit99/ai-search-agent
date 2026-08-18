# Real-Time AI Search Agent (Python CLI)

A lightweight, autonomous AI search agent built from scratch using **Python 3**, **OpenAI's tool-calling framework (GPT-4o-mini)**, and **[SearchApi.io](https://www.searchapi.io/?utm_source=Dev&utm_medium=Ambassador&utm_campaign=eunit.me)** as the live web data pipeline.

This CLI tool turns an LLM into a real-time research assistant capable of autonomously deciding when to search Google, retrieving structured SERP data, and synthesizing grounded, fact-checked answers.

---

## How It Works (4-Step Agent Loop)

```txt
┌──────────────┐     1. Prompt     ┌──────────────┐     2. Tool Call Request     ┌──────────────────┐
│              │ ────────────────> │              │ ───────────────────────────> │                  │
│  User Query  │                   │ OpenAI LLM   │                              │ search_helper.py │
│              │ <──────────────── │ (GPT-4o-mini)│ <─────────────────────────── │ (SearchApi.io)   │
└──────────────┘    4. Final Text  └──────────────┘       3. Live Web Data       └──────────────────┘
```

1. **User Query**: Accepts natural language prompts (e.g. current events, live stock market data, or timeless technical concepts).
2. **Intent Check & Tool Call**: OpenAI model evaluates if live search data is needed. If yes, it emits a `search_web` tool call request.
3. **Infrastructure Execution**: `search_helper.py` queries SearchApi.io's Google Search engine, extracts organic results, and injects clean snippets back into conversation history.
4. **AI Synthesis**: The LLM reads the live search snippets and synthesizes a grounded answer.

---

## Repository Structure

```txt
ai-search-agent/
├── search_helper.py    # SearchApi.io Google engine API wrapper
├── agent.py            # OpenAI tool schema definition & ask_agent()
├── run.py              # Orchestration loop (CLI entry point)
├── .env.example        # Template for API keys
├── requirements.txt    # Python package dependencies
└── README.md           # Documentation
```

---

## Getting Started

### 1. Prerequisites

- **Python 3.8+**
- **OpenAI API Key**: Sign up at [OpenAI Platform](https://platform.openai.com)
- **SearchApi API Key**: Get 100 free searches at [SearchApi.io](https://www.searchapi.io/?utm_source=Dev&utm_medium=Ambassador&utm_campaign=eunit.me)

### 2. Setup Instructions

Clone the repository and move into the project directory:

```bash
git clone https://github.com/Eunit99/ai-search-agent.git
cd ai-search-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Open `.env` and add your API keys:

```env
OPENAI_API_KEY="your_actual_openai_api_key_here"
SEARCHAPI_API_KEY="your_actual_searchapi_api_key_here"
```

---

## Running the Agent

Run the main orchestrator script:

```bash
python run.py
```

### Sample Output

**Query 1 (Current Events — Web Search Triggered):**

```txt
User: What were the top 3 tech stock market trends in Q1 of 2026?

Agent decision: 'I need to use SearchApi to look up live information on the web.'
Invoking tool: search_web() with arguments {'query': 'top tech stock market trends Q1 2026'}
Synthesizing live search data into a comprehensive answer...

Final answer:
Based on recent web data, the top three tech stock market trends in Q1 2026 were:
1. AI infrastructure stocks surged as hyperscalers accelerated GPU procurement...
2. Semiconductor supply chain stabilization drove AMD and TSMC to multi-year highs...
3. Enterprise SaaS consolidation continued with major M&A announcements...
```

**Query 2 (Technical Concept — Answered Natively):**

```txt
User: Explain the fundamental difference between a SQL and NoSQL database in two sentences.

Agent decision: 'I can answer this question from my existing knowledge.'

Final answer:
SQL databases organize data into structured tables with predefined schemas...
```

---

## Related Projects & Tutorials

- **Full-Stack Next.js Application**: [github.com/Eunit99/realtime-search](https://github.com/Eunit99/realtime-search)
- **Live Demo**: [realtime-search.vercel.app](https://realtime-search.vercel.app/)
- **Tutorial Guide**: [Building a Real-Time AI Search Agent with SearchApi and OpenAI](http://eunit.me/blog/building-a-real-time-ai-search-agent-with-searchapi-and-openai)
