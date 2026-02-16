# ⚡ QUICK REFERENCE - Banking AI Agent

## 🚀 Start in 30 Seconds

### Terminal 1 (Backend)
```powershell
cd C:\Users\user\Downloads\BankAssistAI
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload
```

### Terminal 2 (Frontend)
```powershell
cd C:\Users\user\Downloads\BankAssistAI
.\venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

### Browser
```
http://localhost:8501
```

---

## 📋 Checklist Before Running

- [ ] Virtual environment activated
- [ ] `requirements.txt` installed
- [ ] `.env` file created with OPENAI_API_KEY
- [ ] Both terminals ready

---

## 🧪 Quick Test Queries

Copy and paste these into the chat:

### Test 1: Account Lookup
```
What's my account balance for ACC001?
```
**Tool Used**: get_account_details

### Test 2: Transactions
```
Show me recent transactions for ACC002
```
**Tool Used**: get_transaction_history

### Test 3: Branches
```
Find branches in Mumbai
```
**Tool Used**: find_nearest_branch

### Test 4: Loan Check
```
Am I eligible for a home loan? Account: ACC001
```
**Tool Used**: check_loan_eligibility

### Test 5: Escalation
```
I need to open a business account
```
**Tool Used**: escalate_to_human (when needed)

---

## 🔑 Account IDs for Testing

```
ACC001 - Rajesh Kumar (Savings, Rs. 250,000)
ACC002 - Priya Sharma (Current, Rs. 500,000)
ACC003 - Amit Patel (Salary, Rs. 125,000)
```

---

## 🏙️ Cities for Branch Search

```
Mumbai
Bangalore
Delhi
```

---

## 💰 Loan Types

```
personal
home
business
auto
```

---

## 📊 System Check

### Is Backend Running?
```
curl http://localhost:8000/health
```

Should return:
```json
{"status": "healthy", "rag_ready": true, "agent_ready": true}
```

### Is Frontend Running?
```
Open browser to http://localhost:8501
```

---

## 🐛 Common Issues

| Issue | Fix |
|-------|-----|
| Backend won't start | Check you're in project root directory |
| "ModuleNotFoundError" | Activate venv: `.\venv\Scripts\Activate.ps1` |
| FAISS installation fails | `pip install faiss-cpu --no-binary :all:` |
| OpenAI API key error | Edit .env with your actual key |
| Connection refused | Start backend first (port 8000) |
| Streamlit blank page | Refresh browser, check backend logs |

---

## 📁 Important Files

- `backend/main.py` - FastAPI app
- `backend/agent/agent.py` - Function calling agent
- `frontend/app.py` - Streamlit UI
- `.env` - Your OpenAI API key (SECRET)
- `SETUP_GUIDE.md` - Detailed setup
- `README.md` - Full documentation

---

## 🎯 What the Agent Can Do

✅ Check account balance and status
✅ View transaction history
✅ Find nearby branches
✅ Check loan eligibility
✅ Answer banking FAQs
✅ Escalate to human agents

---

## ⚙️ How It Works

```
You: "What's my balance?"
     ↓
RAG: Retrieves relevant banking docs
     ↓
Agent: Decides to call get_account_details tool
     ↓
Tool: Returns account data
     ↓
Agent: Analyzes result, forms response
     ↓
You: Gets detailed answer with account info
```

---

## 📊 Response Time

- **First query**: 3-5 seconds (creates embeddings)
- **Subsequent queries**: 2-3 seconds
- **Escalation**: <1 second

---

## 🔄 Reset Conversation

```
Click "Reset Conversation" button in sidebar
```

---

## 🛑 Stop Applications

### Stop Backend
```
Press Ctrl+C in backend terminal
```

### Stop Frontend
```
Press Ctrl+C in frontend terminal
```

---

## 📈 Monitor Logs

### Backend Logs
Watch the first terminal:
```
- Agent iteration messages
- Tool calls
- API requests
```

### Frontend Logs
Watch Streamlit terminal:
```
- Page loads
- User interactions
- API calls
```

---

## 🔐 Security Notes

- ✅ API key in .env (never commit)
- ✅ No hardcoded secrets
- ✅ CORS configured
- ✅ Input validated
- ✅ Errors sanitized

---

## 💡 Pro Tips

1. **Tool Calls**: Check sidebar to see what tools were called
2. **Iterations**: Shows how many times the agent thought
3. **Clear History**: Use button to clear chat
4. **Test Incrementally**: Start with simple queries
5. **Watch Logs**: Terminal logs show what's happening

---

## 🎓 Learning Points

- OpenAI function calling
- RAG with vector databases
- ReAct pattern
- FastAPI async
- Streamlit state management

---

## 📞 Need Help?

1. Check **SETUP_GUIDE.md** for detailed help
2. Run `python verify_setup.py` to check config
3. Check **AI_TOOLS_TRANSPARENCY.md** for dev notes
4. Review logs in both terminals

---

## ✅ You're All Set!

Everything is ready to run. Just follow the 30-second setup above and you're good to go! 🚀

---

**Questions for SME?** Be ready to explain:
- How function calling works
- RAG architecture
- ReAct loop
- Why it's production-ready
- Future enhancements

**Good luck!** 🎉
