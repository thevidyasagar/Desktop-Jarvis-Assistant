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

