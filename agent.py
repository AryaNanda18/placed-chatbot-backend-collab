import requests
 
from tools import *
from constants import *

@dataclass
class Agent:
    system_prompt: str = SYSTEM_PROMPT
    model: str = MODEL
    base_url: str = BASE_URL
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
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": context_content},
        ]
 
        while True:
            api_kwargs: dict[str, Any] = {
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
 
            assistant_msg: dict[str, Any] = {
                "role": "assistant",
                "content": message.get("content") or "",
            }
            if tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.get("id"),
                        "type": tc.get("type"),
                        "function": {
                            "name": (tc.get("function") or {}).get("name"),
                            "arguments": (tc.get("function") or {}).get("arguments"),
                        },
                    }
                    for tc in tool_calls
                ]
 
            self.messages.append(assistant_msg)
 
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