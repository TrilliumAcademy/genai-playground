import os

from octoai.text_gen import ChatMessage
from octoai.client import OctoAI

client = OctoAI()
stream = client.text_gen.create_chat_completion_stream(
    max_tokens=512,
    messages=[
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(
            role="user",
            content="Tell me a joke about an anteater, a train engineer, and a rubber chicken.",
        ),
    ],
    model="meta-llama-3.1-8b-instruct",
    presence_penalty=0,
    temperature=0,
    top_p=1,
)

for token in stream:
    if token.choices[0].delta.content:
        print(token.choices[0].delta.content, end="", flush=True)
