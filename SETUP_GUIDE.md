# Banking AI Agent - Complete Setup Guide

## 🎯 Project Overview
This is a **professional-grade Banking Customer Service AI Agent** using:
- **OpenAI GPT-4 Turbo** for LLM
- **Function Calling** (ReAct pattern) for tool use
- **RAG (Retrieval Augmented Generation)** for banking documents
- **FastAPI** for backend
- **Streamlit** for frontend

## 📋 Prerequisites
- Python 3.8+ (recommend 3.10+)
- OpenAI API Key (GPT-4 Turbo access)
- Windows/Mac/Linux with pip

## 🚀 Quick Setup (5 minutes)

### Step 1: Get OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Copy it (you won't see it again)

### Step 2: Create Virtual Environment
```powershell
# Navigate to project directory
cd C:\Users\user\Downloads\BankAssistAI

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or activate (Windows CMD)
.\venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```powershell
# Ensure you're in the project directory with venv activated
pip install -r requirements.txt
```

**Note**: If you get FAISS installation errors on Windows, try:
```powershell
pip install faiss-cpu --no-binary :all:
```

### Step 4: Configure Environment
```powershell
# Create .env file from template
Copy-Item .env.example .env

# Edit .env and add your OpenAI API Key
notepad .env
```

In the `.env` file, replace:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Run Backend
```powershell
# From project root with venv activated
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     ✅ Banking AI Agent ready!
```

### Step 6: Run Frontend (In New Terminal)
```powershell
# Open new PowerShell window

# Navigate to project
cd C:\Users\user\Downloads\BankAssistAI

# Activate venv
.\venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run frontend/app.py
```

Streamlit will open at: `http://localhost:8501`

## 🏗️ Project Structure

```
BankAssistAI/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── data_init.py            # Sample data generation
│   ├── agent/
│   │   ├── agent.py            # Function calling agent (ReAct)
│   │   ├── rag.py              # RAG system with FAISS
│   │   └── tools.py            # Banking tools for function calling
│   └── data/
│       ├── banking_docs.txt    # FAQs and policies
│       ├── branch_data.json    # Branch information
│       └── transactions.json   # Sample transactions
├── frontend/
│   └── app.py                  # Streamlit UI
├── vectorstore/                # FAISS vector database (auto-created)
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Example environment file
└── requirements.txt            # Python dependencies
```

## 🔑 Key Features

### 1. Function Calling Agent
The agent uses OpenAI's function calling with ReAct pattern:
```
1. Understand user query
2. Decide which tools to call
3. Execute tools (get_account_details, etc.)
4. Analyze results
5. Return response to user
```

### 2. Available Banking Tools
- **get_account_details**: Check balance, account status
- **get_transaction_history**: View recent transactions
- **find_nearest_branch**: Locate branches by city
- **check_loan_eligibility**: Assess loan eligibility
- **escalate_to_human**: Hand off to human agent

### 3. RAG System
- Loads banking FAQs and policies
- Creates vector embeddings with OpenAI
- Stores in FAISS for fast retrieval
- Provides context to the agent for accurate responses

### 4. Professional UI
- Clean chat interface
- Shows tool calls and iterations
- Session management
- Backend health check
- Example queries

## 🧪 Testing the Agent

### Test Query 1: Account Information
```
"What's my account balance? My account ID is ACC001"
```
Expected: Agent calls get_account_details tool

### Test Query 2: Transactions
```
"Show me my recent transactions for ACC002"
```
Expected: Agent calls get_transaction_history tool

### Test Query 3: Branch Location
```
"Find branches in Mumbai"
```
Expected: Agent calls find_nearest_branch tool

### Test Query 4: Loan Check
```
"Am I eligible for a home loan? Account ID: ACC001"
```
Expected: Agent calls check_loan_eligibility tool

### Test Query 5: Escalation
```
"I need to speak to someone about opening a business account"
```
Expected: Agent offers to escalate to human agent

## 🔧 Troubleshooting

### Backend won't start
**Error**: `ModuleNotFoundError: No module named 'backend'`
**Solution**: Run from project root directory:
```powershell
cd C:\Users\user\Downloads\BankAssistAI
python -m uvicorn backend.main:app --reload
```

### FAISS installation fails
**Solution**: Install CPU version with:
```powershell
pip install faiss-cpu --no-binary :all:
```

### OpenAI API key not working
**Check**:
1. API key is in `.env` file correctly
2. Key has proper access (not expired)
3. You have credits in OpenAI account
4. Model is available in your region

### Streamlit can't connect to backend
**Check**:
1. Backend is running (check terminal)
2. URL in sidebar is correct
3. No firewall blocking port 8000

### Vector store takes long time to create
**Normal**: First run creates embeddings for all documents (~30 seconds)
**Next runs**: Uses cached vector store (instant)

## 📊 How It Works

### Message Flow
```
User Message (Streamlit)
    ↓
[Sent to Backend via HTTP]
    ↓
Backend receives message
    ↓
RAG system retrieves relevant documents
    ↓
Agent processes with RAG context + user message
    ↓
[ReAct Loop]:
  1. LLM decides which tools to call
  2. Execute tools (get_account_details, etc.)
  3. Analyze results
  4. Return final response
    ↓
Response sent back to Frontend
    ↓
Streamlit displays response + tool calls
```

### Function Calling Process
1. **Understand**: LLM reads user query + RAG context
2. **Decide**: LLM decides which tool(s) to call
3. **Execute**: Backend executes selected tools
4. **Analyze**: LLM analyzes tool results
5. **Respond**: LLM formulates final response

## 🎓 Learning Points for SME

### What to Highlight:
1. **Function Calling**: Shows how modern LLMs can use tools
2. **RAG Pattern**: Documents provide context for accuracy
3. **ReAct Loop**: Shows reasoning and action patterns
4. **Error Handling**: Graceful escalation to humans
5. **Production Ready**: Logging, health checks, error handling

### Code Quality Features:
- Type hints throughout
- Comprehensive docstrings
- Error handling with logging
- Configuration management
- Session state management

## 🚀 Enhancements (Future)

- [ ] Database integration (SQL)
- [ ] Authentication (JWT)
- [ ] Rate limiting
- [ ] Usage analytics
- [ ] Conversation memory in DB
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Advanced monitoring

## 📚 References

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Streamlit Docs](https://docs.streamlit.io)
- [LangChain RAG](https://python.langchain.com)
- [FastAPI](https://fastapi.tiangolo.com)

## 💡 Pro Tips

1. **Test Incrementally**: Start with backend, then test frontend
2. **Monitor Logs**: Check both terminal windows for issues
3. **API Costs**: Monitor OpenAI API usage (embeddings + chat)
4. **Tool Results**: Look at tool calls in sidebar to debug agent behavior
5. **Conversation History**: Agent maintains context across messages

## 📞 Support

If you encounter issues:
1. Check logs in both backend and frontend terminals
2. Verify .env configuration
3. Ensure all dependencies are installed
4. Try resetting conversation
5. Restart both backend and frontend

---

**Ready to impress your SME? You now have a production-ready Banking AI Agent!** 🎉
