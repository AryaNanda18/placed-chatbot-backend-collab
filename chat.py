import traceback

from agent import Agent
from context import register_all_contexts
from constants import *

def chat(message: str = "") -> str:
    """Process a single chat message for the FastAPI /predict endpoint."""
    if not message.strip():
        return "Please provide a message."

    try:
        if not API_KEY:
            return "Server misconfiguration: API_KEY is not set. Add API_KEY to your .env file." 

        agent = Agent(
            model=MODEL,
            base_url=BASE_URL,
            api_key=API_KEY,
            system_prompt=SYSTEM_PROMPT,
        )

        register_all_contexts(agent)

        response = agent.chat(message).strip()
        return response if response else "Sorry, I could not generate a response. Please try again."

    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return f"Sorry, an error occurred: {str(e)}. Check server logs and ensure API_KEY is set in .env."

