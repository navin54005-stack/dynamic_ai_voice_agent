# 🎙️ Dynamic Voice Agent (Flask)

A **Flask-based AI Voice/Chat Agent backend** that dynamically responds to customer inputs using **company data uploaded via CSV**. Designed for call-center–style conversational agents, lead handling, and company-aware AI responses.

---

## 🚀 Features

* 📂 **Smart CSV Upload** – Automatically detects company & contact-related columns
* 🧠 **Dynamic AI Agent** – Generates short, contextual responses (5–10 sec speech)
* 🗣️ **Conversation Learning** – Tracks patterns & learning insights
* 🔐 **Session-Based State** – Company data stored securely per session
* 🧪 **Health Monitoring API**
* ⚡ Lightweight & fast Flask server

---

## 🗂️ Project Structure

```
project-root/
│
├── app.py                  # Main Flask application
├── config.py               # Central configuration
├── dynamic_ai_model.py     # Core AI logic (DynamicVoiceAgent)
├── utils/
│   └── csv_processor.py    # Smart CSV parsing & column detection
│
├── templates/
│   └── index.html          # Web UI
│
├── uploads/                # Uploaded CSV files
├── data/
│   ├── clusters/           # Conversation clusters
│   ├── patterns/           # Learned response patterns
│   └── sessions/           # Session data
│
├── .env                    # Environment variables
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/dynamic-voice-agent.git
cd dynamic-voice-agent
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-super-secret-key
```

---

## ▶️ Running the Application

```bash
python app.py
```

Server will start at:

* 🌐 **App**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* 🧪 **Health Check**: [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)

---

## 📡 API Endpoints

### 🔹 Upload Company Data

`POST /upload-company-data`

* **Input**: CSV file
* **Output**: Company info, detected columns, record count

---

### 🔹 Get AI Response

`POST /get-ai-response`

```json
{
  "customer_response": "Tell me about your services",
  "customer_data": {"name": "John"}
}
```

---

### 🔹 Learning Insights

`GET /get-learning-insights`

Returns AI learning patterns & conversation insights.

---

### 🔹 Health Check

`GET /health`

```json
{
  "status": "healthy",
  "company_data_loaded": true
}
```

---

### 🔹 Clear Session

`POST /clear-session`

Clears uploaded company data & session memory.

---

## 📄 CSV Format (Flexible)

The system **auto-detects columns**, but common headers include:

* Company Name
* Services / Products
* Phone / Email
* Address
* Contact Person

> No strict format required 🎯

---

## 🔐 Configuration (`config.py`)

| Setting              | Description                    |
| -------------------- | ------------------------------ |
| `MAX_RESPONSE_WORDS` | Keeps responses short          |
| `CLUSTER_COUNT`      | Conversation learning clusters |
| `SESSION_TIMEOUT`    | Session expiry time            |

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Flask**
* **Session-based state**
* **CSV intelligence processing**
* **Modular AI logic**

---

## 🧠 Future Enhancements

* 📞 Twilio / GSM call integration
* 🔊 Text-to-Speech (TTS)
* 🤖 Ollama / LLM backend integration
* 📊 Admin analytics dashboard

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 👨‍💻 Author

**Naveen Rao
Mayank Panwar**
AI & Automation Developer

---

⭐ If you find this project useful, don’t forget to star the repo!
