# 🧠 Multi-Agent Research Action System
## 1. Architecture 
-   Model: Task Delegation Architecture (One Coordinator agent + multiple Worker agents)
-   Language: Python
-   Frameworks: Autogen, Semantic Kernal, Microsoft 365 Agents SDK, Azure Agents SDK
## 2. Detailed Architechture
```bash
User Request --> Coordinator Agent (Autogen)
            |--> Research Agent (Autogen AssistantAgent + ToolAgent for Web Search)
            |--> Analysis Agent (Semantic Kernel Planner / Skills)
            |--> Communication Agent (Microsoft 365 SDK: send mail, Teams messages)
```

## 3. Agent Roles
| Agent               | Role                                                                 |
|---------------------|----------------------------------------------------------------------|
| Coordinator         | Breaks user tasks into subtasks, assigns them to workers, collects and delivers results. |
| Research Agent      | Performs web searches, optional AI evaluation, summarizes findings.  |
| Analysis Agent      | Plans, organizes, and prioritizes information using Semantic Kernel Skills. |
| Communication Agent | Sends final outputs to users via Outlook or Microsoft Teams.         |


## 4. Key Components and Tools

|Component           | Framework/Service                       |
|--------------------|-----------------------------------------|
|Research Worker | Autogen + Web Search ToolAgent              |
|Analysis Worker | Semantic Kernel (Skills and Planner)        |
|Communication Worker | Microsoft 365 Agents SDK               |
|Optional Memory | Semantic Kernel persistent memory           |
|Front-End | Flask (for document upload + simple UI)           |
|Deployment | Azure Free Tier (App Service, Functions, etc.)   |




## 5. Front-End Plan
-   Framework: Flask
-   Features:
 -   Upload documents (for RAG - Retrieval-Augmented Generation).
 -   Input custom queries.
 -   Show agent progress/status dynamically (could use simple polling or WebSockets).
-   Design Goal: Clean, minimal UI for fast interactions.

## 6. Backend Intelligence
-   Integrate RAG (document-based retrieval) optionally:
 -   Upload document → Embed using Azure Cognitive Search / FAISS.
 -   Query system searches document first, then runs agents.
-   Use lightweight NLP for basic sentence understanding if needed.


## 7. Deployment Plan
-   Use Azure App Service (Free Tier) for Flask app.
-   Use Azure Functions if heavy background processing needed.
-   Use Azure Blob Storage for uploaded documents.
-   Keep everything inside Microsoft ecosystem to maximize hackathon scoring.

## 8. Protocols
-   Agents should communicate using basic API calls internally (REST).
-   Implement MCP-like message structure if time allows (optional).
-   API: OpenRouter's APIs


## OPENROUTER API Documentation overview in python.
```bash
- Using OpenAI SDK
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  model="openai/gpt-4o",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)

print(completion.choices[0].message.content)
```

```bash
- using OpenRouter API Directly

import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer <OPENROUTER_API_KEY>",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "openai/gpt-4o", # Optional
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

```


## Updates (April 2025):
- Duplicate entry point main.py removed; backend/app.py is now the main backend.
- Improved web search reliability (timeout increased, better error handling).
- Added stubs for AnalysisAgent and CommunicationAgent for future expansion.


## Current Issues:
- Web Search reliability improved, but further enhancements possible.
- In live page, After all the timeouts, it is saying "The model 'api/v1chat' is not available" which should be api/v1/chat. (API endpoint usage is being double-checked)
- Worker Agent stubs (AnalysisAgent, CommunicationAgent) added; full implementation pending.