"""
Streamlit Frontend for Banking AI Agent
Professional chat interface with session management
"""
import streamlit as st
import requests
import json
from datetime import datetime
import time
from typing import Dict, List

# Page configuration
st.set_page_config(
    page_title="Banking AI Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .tool-call {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    .response-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://localhost:8001"
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = f"conv_{int(time.time())}"


def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{st.session_state.api_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_agent_response(user_message: str) -> Dict:
    """Send message to backend and get response"""
    try:
        response = requests.post(
            f"{st.session_state.api_url}/chat",
            json={
                "message": user_message,
                "conversation_id": st.session_state.conversation_id
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "❌ Backend not connected. Please start the backend server with: python -m uvicorn backend.main:app --reload"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "⏱️ Request timed out. The system is currently experiencing high traffic (rate limits). Please try again in a minute."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}"
        }


def format_tool_call(tool_call: Dict) -> str:
    """Format tool call for display"""
    name = tool_call.get("name", "Unknown")
    args = tool_call.get("args", {})
    result = tool_call.get("result", {})
    
    output = f"🔧 **Tool: {name}**\n"
    if args:
        output += f"   Arguments: {json.dumps(args, indent=2)}\n"
    if result.get("success"):
        output += f"   ✅ Success\n"
    else:
        output += f"   ❌ Error: {result.get('error', 'Unknown error')}\n"
    return output


def display_tool_calls(tool_calls: List[Dict]):
    """Display tool calls made by the agent"""
    if tool_calls:
        with st.expander(f"🔧 Tool Calls ({len(tool_calls)})", expanded=False):
            for i, call in enumerate(tool_calls, 1):
                st.markdown(f"**Call {i}:**")
                st.code(f"Function: {call['name']}\nArgs: {json.dumps(call['args'], indent=2)}", language="json")
                
                if call.get("result"):
                    with st.expander("Result", expanded=False):
                        st.json(call["result"])


def main():
    """Main Streamlit app"""
    init_session_state()
    
    # Header
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title("🏦 Banking AI Assistant")
        st.markdown("*Powered by OpenAI Function Calling & RAG*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Backend configuration
        st.session_state.api_url = st.text_input(
            "Backend URL",
            value=st.session_state.api_url,
            help="URL of the backend API server"
        )
        
        # Health check
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.markdown("**Backend Status:**")
        with col2:
            if check_backend_health():
                st.success("🟢 Connected", icon="✅")
            else:
                st.error("🔴 Disconnected", icon="❌")
        
        st.markdown("---")
        
        # Agent info
        st.markdown("### 📋 Agent Info")
        st.markdown("""
        **Capabilities:**
        - 🔍 Account information lookup
        - 📊 Transaction history
        - 🏢 Branch location finder
        - 💰 Loan eligibility check
        - 📞 Escalation to human agents
        
        **Example Queries:**
        - "What's my account balance?"
        - "Show me my recent transactions"
        - "Find branches in Mumbai"
        - "Am I eligible for a personal loan?"
        """)
        
        st.markdown("---")
        
        # Actions
        st.markdown("### 🎯 Actions")
        if st.button("🔄 Reset Conversation"):
            try:
                requests.post(f"{st.session_state.api_url}/reset")
                st.session_state.messages = []
                st.success("Conversation reset!")
            except:
                st.error("Failed to reset conversation")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared!")
    
    # Main chat area
    st.markdown("### 💬 Chat")
    
    # Display message history
    for message in st.session_state.messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])
        iterations = message.get("iterations", 0)
        
        if role == "user":
            st.markdown("**👤 You:** " + content)
        else:
            st.markdown("**🤖 Assistant:** " + content)
            
            # Display metadata
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"⚙️ Iterations: {iterations}")
            with col2:
                st.caption(f"🔧 Tools used: {len(tool_calls)}")
            
            # Display tool calls if any
            display_tool_calls(tool_calls)
    
    # Input area
    st.markdown("---")
    
    # Chat input
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input(
            "Enter your query:",
            placeholder="e.g., Check my account balance..."
        )
    with col2:
        send_button = st.button("Send")
    
    # Process user input
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        st.markdown("**👤 You:** " + user_input)
        
        # Get agent response
        with st.spinner("🤔 Thinking..."):
            response = get_agent_response(user_input)
        
        if response.get("success"):
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.get("response", "No response"),
                "tool_calls": response.get("tool_calls", []),
                "iterations": response.get("iterations", 0)
            })
            
            # Display response
            st.markdown("**🤖 Assistant:** " + response.get("response", "No response"))
            
            # Display metadata
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"⚙️ Iterations: {response.get('iterations', 0)}")
            with col2:
                st.caption(f"🔧 Tools used: {len(response.get('tool_calls', []))}")
            
            # Display tool calls
                display_tool_calls(response.get("tool_calls", []))
        else:
            error_msg = response.get("error", "Unknown error occurred")
            st.error(error_msg)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
        <p>Banking AI Assistant v1.0 | Powered by OpenAI GPT-4 Turbo</p>
        <p>For complex issues, a human agent will be assigned to assist you.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
