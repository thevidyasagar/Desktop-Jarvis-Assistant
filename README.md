# Assistant Jarvis – AI Desktop Voice Assistant

Assistant Jarvis is a personal AI desktop assistant that listens to your voice, understands natural language, and performs tasks for you in real time.  
It combines wake-word detection, RAG-based memory, LLMs, and a sci-fi style HUD interface to give a Jarvis-like experience.

---

## 🚀 Features

- 🎙 **Wake Word Detection**  
  - Always-on listening using Porcupine  
  - <300 ms wake-word response time for smooth interaction

- 🧠 **RAG-based Long-Term Memory**  
  - Stores context and user data using vector embeddings  
  - Retrieves relevant information for more personalized answers

- 🗣 **Natural Voice Conversation**  
  - Uses OpenAI APIs for LLM responses  
  - Text-to-Speech pipeline for natural voice output  
  - Noise filtering & preprocessing to improve speech accuracy

- 💻 **HUD Interface**  
  - Desktop UI with real-time visual feedback  
  - Shows current status, transcription, and responses  
  - Sci-fi inspired layout (Jarvis-style)

- ⚙ **Command Execution Engine**  
  - Open apps, search the web, perform system tasks  
  - Easy to extend with custom commands

- 🌐 **API Backend**  
  - FastAPI backend for routing, AI requests, and RAG pipeline  
  - Clean separation between UI, logic, and models

---

## 🧰 Tech Stack

**Programming Language**
- Python

**Core AI & ML**
- OpenAI API (LLM)
- LangChain
- RAG (Retrieval-Augmented Generation)
- Vector Embeddings & Vector Store

**Voice & Audio**
- Porcupine (wake-word detection)
- Speech Recognition
- Text-to-Speech (TTS)

**Backend & API**
- FastAPI
- Python async support

**Others**
- Git & GitHub
- Virtual environments (venv)
- Config via `.env` file

---

## 🏗 Architecture Overview

High-level flow:

1. **Wake Word Listener**  
   - Listens continuously using Porcupine  
   - On wake word, starts recording audio

2. **Speech to Text**  
   - Captures user command and converts it to text

3. **RAG Pipeline**  
   - Converts query into embeddings  
   - Searches vector store for relevant context  
   - Combines user query + context and sends to LLM

4. **LLM Response & Actions**  
   - Generates response text  
   - Optionally triggers system commands or custom actions

5. **HUD & Voice Output**  
   - Displays response in the HUD  
   - Speaks back using TTS

---

## ⚙️ Getting Started

### 1. Clone the Repository

git clone https://github.com/thevidyasagar/Desktop-Jarvis-Assistant.git


## 2. Create & Activate Virtual Environment ##
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
# source .venv/bin/activate

## 3. Install Dependencies ##
pip install -r requirements.txt

(Make sure requirements.txt contains all required packages like fastapi, langchain, openai, porcupine, uvicorn, etc.)

## 🔐 Environment Variables ##

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
VECTOR_DB_PATH=./data/vector_store
PORCUPINE_ACCESS_KEY=your_porcupine_access_key_here

Add any other keys/config you use (TTS provider, additional APIs, etc.).

## ▶️ Running the Project ##
## 1. Start the Backend (FastAPI) ##
uvicorn app.main:app --reload


or if your entry file is different, update the path accordingly.

## 2. Start the Desktop Assistant / HUD ##

If you have a separate script for the UI:

-python main.py

This typically:

Starts the HUD interface

Connects to the FastAPI backend

Starts the wake-word listener

## 🗣 Example Voice Commands ##

You can say things like:

“Jarvis, what’s the weather today?”

“Jarvis, open YouTube.”

“Jarvis, summarize this text.”

“Jarvis, remind me to study at 9 PM.”

“Jarvis, what did we discuss yesterday?” (uses RAG memory)

You can extend the command engine to add your own custom actions.

