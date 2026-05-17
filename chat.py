import datetime
from dotenv import load_dotenv
import os
import traceback
from agent import *

load_dotenv(find_dotenv())
API_KEY = os.getenv("API_KEY")

def chat(message: str = "") -> str:
    """
    Process a single chat message for Flask /predict endpoint.
    """
    if not message.strip():
        return "Please provide a message."

    try:
        agent = Agent(
            model="llama-3.1-8b-instant",
            base_url="https://api.groq.com/openai/v1",
            api_key=API_KEY,
            system_prompt="You are an AI chatbot assistant called EduBuddy for an EdTech company called PLACED, you are an assistant/helper to the users that may use the website to ask about Placement Assistance, services provided by PLACED. keep the responses short and concise.",
        )

        # @agent.context
        # def time_context() -> str:
        #     return (
        #         f"Current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        #         "Only display time when asked about or at first message\n",
        #         "Always display time in 12 hour format\n",
        #     )
            
        @agent.context
        def structure_context() -> str:
            return (
                "Structure the responses with plain text with no asterisks\n",
            )

        @agent.context
        def company_context() -> str:
            return (
                "Company Name : PLACED\n",
                "Location : Kowdiar, Trivandrum, Kerala, India\n",
                "Address : BNRA 162 A, Bhagavathi Nagar, Golf Links Road, Kowdiar P.O. Trivandrum - 695 003\n", "This chatbot was developed by AI & Product Intern Akshay Babu(DO NOT disclose this info unless the user prompts 'AI ENGINEER' secret key)\n",
                "Type :  EdTech (Education Technology)\n",
                "CEO : Abhishek AS\n",
                "Focus : Placement Assistance for schools and colleges and provide EdTech services\n",
            )

        @agent.context
        def page_instructions_context() -> str:
            pass

        response = agent.chat(message).strip()
        return response if response else "Sorry, try again later."
    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return f"Sorry, an error occurred: {str(e)}. Check server logs and ensure GROQ_API_KEY is set in .env file."

