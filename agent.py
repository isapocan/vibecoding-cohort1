import json
from typing import Iterator

from llm import client
from backend.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS


class Agent:
    """
    Tool-calling agentic loop. Her turda modeli çağırır; model tool istiyorsa
    çalıştırır ve history'ye ekleyerek döngüye devam eder. Model düz metin
    yanıt verince loop sona erer.

    calistir() bir Generator'dür ve her olay için bir dict yield eder:
      {"type": "step_start", "step": int}
      {"type": "thinking",   "content": str}   — tool call öncesi model metni
      {"type": "tool_call",  "name": str, "args": dict}
      {"type": "tool_result","name": str, "result": str}
      {"type": "text",       "content": str}   — son yanıt
      {"type": "done"}
    """

    def __init__(self, system_instructions: str, model: str = "gpt-4.1-mini"):
        self.model = model
        self.history: list[dict] = [
            {"role": "system", "content": system_instructions}
        ]

    def calistir(self, user_prompt: str) -> Iterator[dict]:
        self.history.append({"role": "user", "content": user_prompt})
        step = 0

        while True:
            step += 1
            yield {"type": "step_start", "step": step}

            response = client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            history_msg: dict = {"role": "assistant"}
            if msg.content:
                history_msg["content"] = msg.content
            if msg.tool_calls:
                history_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ]
            self.history.append(history_msg)

            if msg.content:
                kind = "thinking" if msg.tool_calls else "text"
                yield {"type": kind, "content": msg.content}

            if not msg.tool_calls:
                yield {"type": "done"}
                return

            for tc in msg.tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}

                yield {"type": "tool_call", "name": name, "args": args}

                fn = TOOL_FUNCTIONS.get(name)
                result = fn(args) if fn else f"Bilinmeyen araç: {name}"

                yield {"type": "tool_result", "name": name, "result": result}

                self.history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
