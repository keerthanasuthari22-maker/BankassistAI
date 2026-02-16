"""
Function Calling Agent for Banking Customer Service
Uses Google Gemini (google-genai SDK) with RAG context + Tool execution
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import time
import random

from google import genai

from .tools import BankingToolkit
from ..config import settings

logger = logging.getLogger(__name__)


class FunctionCallingAgent:
    """Banking AI Agent using Gemini with tool calling + RAG"""

    def __init__(self, rag_system, config=settings):
        self.rag = rag_system
        self.config = config

        # New Gemini SDK client
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

        self.toolkit = BankingToolkit(config.DATA_DIR)
        self.conversation_history = []

        # Use correct model names for google-genai SDK
        # Models must include 'models/' prefix based on ListModels API response
        self.primary_model = f"models/{config.GEMINI_MODEL}"
        self.final_model = f"models/{config.GEMINI_MODEL}"
        
        # Log the model being used
        logger.info(f"🤖 Initialized with model: models/{config.GEMINI_MODEL}")
        
        # Simple rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.5  # Minimum seconds between requests

    def _get_rag_context(self, query: str) -> str:
        """Fetch context from FAISS RAG"""
        return self.rag.get_context(query)

    def _build_system_prompt(self) -> str:
        """System prompt for banking assistant"""
        return f"""
You are an expert Banking Customer Service AI Agent.

## Responsibilities:
- Answer customer banking queries professionally
- Use context from knowledge base
- Use tools when required:
    - get_account_details
    - get_transaction_history
    - find_nearest_branch
    - check_loan_eligibility
    - escalate_to_human

## Rules:
- Be concise, accurate, professional.
- Never hallucinate account balances or transaction info.
- If user asks account-related queries, use tools.
- If fraud/unauthorized transaction is mentioned, escalate immediately.
- If you cannot answer, ask a clarifying question.

Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    def _handle_tool_call(self, tool_name: str, tool_args: Dict) -> str:
        """Execute tool and return JSON string result"""
        try:
            if tool_name == "get_account_details":
                result = self.toolkit.get_account_details(tool_args.get("account_id"))

            elif tool_name == "get_transaction_history":
                result = self.toolkit.get_transaction_history(
                    tool_args.get("account_id"),
                    int(tool_args.get("days", 30))
                )

            elif tool_name == "find_nearest_branch":
                result = self.toolkit.find_nearest_branch(tool_args.get("city"))

            elif tool_name == "check_loan_eligibility":
                result = self.toolkit.check_loan_eligibility(
                    tool_args.get("account_id"),
                    tool_args.get("loan_type")
                )

            elif tool_name == "escalate_to_human":
                result = self.toolkit.escalate_to_human(
                    tool_args.get("account_id"),
                    tool_args.get("reason")
                )

            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            return json.dumps(result)

        except Exception as e:
            logger.error(f"❌ Tool execution error {tool_name}: {e}")
            return json.dumps({"error": str(e)})

    def _generate_with_retry(self, model, contents, retries=3, delay=2, max_wait=8):
        """Generate content with retry logic for rate limits (capped wait time)"""
        logger.info(f"🔍 Attempting API call with model: {model}")
        for attempt in range(retries):
            try:
                return self.client.models.generate_content(
                    model=model,
                    contents=contents
                )
            except Exception as e:
                # Check for 429 Resource Exhausted
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < retries - 1:
                        import re
                        # Try to find retry delay in error message
                        # Pattern looks for: 'retryDelay': '40.35s' or similar
                        delay_match = re.search(r"'retryDelay':\s*'([\d\.]+)s'", error_str)
                        
                        if delay_match:
                            retry_after = float(delay_match.group(1))
                            # Cap the sleep time to max_wait seconds (don't wait the full API request)
                            sleep_time = min(retry_after * 0.3, max_wait) + random.uniform(0.5, 1.5)
                            logger.warning(f"⏳ Rate limit hit. API requested {retry_after}s, but waiting only {sleep_time:.2f}s (attempt {attempt + 1}/{retries})...")
                        else:
                            # Exponential backoff with jitter, capped at max_wait
                            sleep_time = min((delay * (2 ** attempt)), max_wait) + random.uniform(0, 1)
                            logger.warning(f"⏳ Rate limit hit for {model}. Retrying in {sleep_time:.2f}s (attempt {attempt + 1}/{retries})...")
                        
                        time.sleep(sleep_time)
                        continue
                    else:
                        logger.error(f"❌ Max retries ({retries}) exceeded for rate limit")
                raise e

    def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user query with Gemini.
        If Gemini returns tool_call JSON, execute tool and ask Gemini to format response.
        """
        # Simple rate limiting to prevent hitting API limits
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"⏱️  Throttling request, waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

        rag_context = self._get_rag_context(user_message)

        prompt = f"""
{self._build_system_prompt()}

[Banking Knowledge Base Context]
{rag_context}

[Customer Query]
{user_message}

Instructions:
- If tool is required, respond ONLY in JSON:
{{
  "tool_call": {{
    "name": "tool_name_here",
    "args": {{
      "param1": "value1"
    }}
  }}
}}

- If tool is not required, respond normally with final answer.
"""

        try:
            response = self._generate_with_retry(
                model=self.primary_model,
                contents=prompt
            )

            text = (response.text or "").strip()

            # Clean markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()

            tool_calls = []
            final_answer = text

            # Detect tool call JSON
            if text.startswith("{") and "tool_call" in text:
                parsed = json.loads(text)
                tool_call = parsed.get("tool_call")

                if tool_call:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})

                    tool_calls.append({"name": tool_name, "args": tool_args})

                    tool_result = self._handle_tool_call(tool_name, tool_args)

                    final_prompt = f"""
Customer Query:
{user_message}

Tool Executed:
{tool_name}

Tool Result (JSON):
{tool_result}

Now generate a final professional banking response to the customer.
- Explain the tool output clearly.
- Provide next steps if required.
"""

                    final_response = self._generate_with_retry(
                        model=self.final_model,
                        contents=final_prompt
                    )

                    final_answer = (final_response.text or "").strip()

            # Store conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": final_answer})
            self.conversation_history = self.conversation_history[-6:]

            return {
                "response": final_answer,
                "iterations": 1,
                "tool_calls": tool_calls,
                "success": True
            }

        except Exception as e:
            error_str = str(e)
            import traceback
            logger.error(f"❌ Gemini API error: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Provide specific error messages based on error type
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                error_msg = "I'm experiencing high demand right now. Please wait a few seconds and try your question again. I apologize for the inconvenience."
            elif "INVALID_ARGUMENT" in error_str:
                error_msg = "I encountered an issue processing your request. Could you please rephrase your question?"
            else:
                error_msg = f"I'm temporarily unable to process your request. Error: {error_str[:100]}"
            
            return {
                "response": error_msg,
                "iterations": 1,
                "tool_calls": [],
                "success": False,
                "error": error_str[:200]  # Include truncated error for debugging
            }

    def reset_conversation(self):
        """Reset history"""
        self.conversation_history = []

    def get_conversation_history(self) -> List[Dict]:
        """Return last history"""
        return self.conversation_history