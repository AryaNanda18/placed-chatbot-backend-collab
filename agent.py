from dotenv import load_dotenv, find_dotenv
import os
import requests

from tools import *

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set")

@dataclass
class Agent:
    system_prompt: str = "You are an AI chatbot assistant called EduBuddy for an EdTech company called PLACED, you are an assistant/helper to the users that may use the website to ask about Placement Assistance, services provided by PLACED. keep the responses short and concise."
    model: str = "llama-3.1-8b-instant"
    base_url: str = "https://api.groq.com/openai/v1"
    api_key: str = API_KEY
    tools: Tools = field(default_factory=Tools)
    contexts: dict[str, Callable[[], str]] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self) -> None:
         self.base_url = self.base_url.rstrip("/")
         
    def context(self, func: Callable[[], str]) -> Callable[[], str]:
        self.contexts[func.__name__] = func
        return func
         
    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        
        context_content = "\n\n".join(
            f"<context>\n<{n}>{fn()}</{n}>\n</context>"
            for n, fn in self.contexts.items()
        )
        
        prefix: list[dict[str, Any]] = [
            {"role": "system", "content" : self.system_prompt},
            {"role": "system", "content" : context_content},
        ]
        
        while True:
            api_kwargs ={
                "model": self.model,
                "messages": prefix + self.messages,
            }
            
            tool_schemas = self.tools.get_schemas()
            if tool_schemas:
                api_kwargs["tools"] = tool_schemas
                
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            r = requests.post(
                url,
                headers=headers,
                json=api_kwargs,
                timeout=300,
            )
            r.raise_for_status()
            data = r.json()
            choices = data.get("choices")
            
            if not choices:
                raise RuntimeError("Model response missing choices")
            
            message = choices[0].get("message")
            if message is None:
                raise RuntimeError("Model response missing message")
            
            tool_calls = message.get("tool_calls") or []
            self.messages.append({
                "role": "assistant",
                "content": message.get("content"),
                "tool_calls": [
                    {
                        "id": tc.get("id"),
                        "type": tc.get("type"),
                        "function": {
                            "name": (tc.get("function") or {}).get("name"),
                            "arguments": (tc.get("function") or {}).get("arguments"),
                        },
                    }
                    for tc in tool_calls
                ],
            })
            
            if not tool_calls:
                return message.get("content") or ""
            
            for tool_call in tool_calls:
                result = self.tools.execute(tool_call)
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "content": json.dumps(result),
                    }
                )
                
            