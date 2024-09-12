#!/usr/bin/env python

# This script demonstrates how to generate a text using the OctoAI API.

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import os
from openai import OpenAI

# Check that our environment variables are set.
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

if "HELICONE_API_KEY" not in os.environ:
    raise ValueError("Please set the HELICONE_API_KEY environment variable.")

# Create an OpenAI client. We proxy the request through Helicone so we can keep track of usage.
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {os.environ['HELICONE_API_KEY']}",
    },
)

# Send a chat message to the API and receive a response.
stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Tell me a joke about an anteater, a train engineer, and a rubber chicken.",
        },
    ],
    model="gpt-4o",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
