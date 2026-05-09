from openai import OpenAI

client = OpenAI()


def call_llm(system_instructions: str, user_prompt: str, model: str = "gpt-4.1-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
