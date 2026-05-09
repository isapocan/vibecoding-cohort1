from openai import OpenAI
from dotenv import load_dotenv
from typing import Iterator

load_dotenv()

client = OpenAI()


def stream_llm(
    system_instructions: str,
    user_prompt: str,
    model: str = "gpt-4.1-mini",
) -> Iterator[str]:
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
