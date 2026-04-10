# 🤖 Local AI Chatbot (Streamlit + Ollama)

A simple **ChatGPT-like chatbot** built using **Streamlit** and **local LLMs** powered by Ollama.
This project runs completely **offline** using open-source models like LLaMA3, Mistral, or Phi-3.

---

## 🚀 Features

* 💬 ChatGPT-style conversational UI
* 🧠 Context-aware chat (remembers conversation)
* 🏠 Runs locally (no API key required)
* ⚡ Supports multiple LLMs (LLaMA3, Mistral, Phi3)
* 🐍 Compatible with Python 3.14

---

## 🛠️ Tech Stack

* Python 3.14
* Streamlit (UI framework)
* Ollama (Local LLM runtime)
* Requests (API communication)

---

## 📦 Required Packages

Install dependencies using:

```bash
pip install streamlit requests
```

### 📚 Package Details

| Package   | Purpose                     |
| --------- | --------------------------- |
| streamlit | Build interactive web UI    |
| requests  | Communicate with Ollama API |

---

## 🤖 Model Setup (Ollama)

Install Ollama from official site.

### Pull a model:

```bash
ollama pull llama3
```

Or faster alternatives:

```bash
ollama pull phi3
ollama pull mistral
```

---

## ▶️ How to Run

### 1. Start Ollama

```bash
ollama run llama3
```

---

### 2. Run the App

```bash
streamlit run app.py
```

---

### 3. Open in Browser

```
http://localhost:8501
```

---

## 💻 Project Structure

```
chatbot-local/
│── app.py
│── README.md
```

---

## 🧠 How It Works

* User inputs a message in the UI
* Chat history is stored in session state
* Messages are sent to Ollama API (`/api/chat`)
* Local LLM generates response
* Response is displayed in chat format

---

## ⚡ Performance Tips

* Use smaller models for faster response:

  * `phi3` → fastest ⚡
  * `mistral` → balanced ⚖️
  * `llama3` → best quality 🧠

* Limit chat history for speed:

```python
messages[-5:]
```

---

## 🧹 Clear Chat (Optional Feature)

```python
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
```

---

## ❗ Troubleshooting

### 1. Slow Responses

* Use `phi3` instead of `llama3`
* Ensure Ollama is running

---

### 2. Connection Error

Make sure Ollama is running:

```bash
ollama run llama3
```

---

### 3. No Response

Check API:

```
http://localhost:11434
```

---

## 📌 Future Enhancements

* 📄 File upload (PDF, CSV, Excel)
* 🔍 RAG (Retrieval-Augmented Generation)
* 🎨 Improved UI styling
* ⚡ Streaming responses
* 🧠 Vector database integration

---

## 📄 License

This project is open-source and free to use.

---

## 🙌 Acknowledgements

* Ollama for local LLM support
* Streamlit for easy UI development

---

## ⭐ Support

If you like this project, give it a ⭐ and share!

---
