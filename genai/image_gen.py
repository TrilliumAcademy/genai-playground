#!/usr/bin/env python3

# This script demonstrates how to generate an image using the OctoAI API.

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import os
import base64
from io import BytesIO
import random

from openai import OpenAI
from PIL import Image
import requests

from rich.console import Console

console = Console()

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

# We're going to ask the AI to generate an image using some of the topics below.
TOPICS = [
    "Rubber chickens",
    "capybaras",
    "train engineers",
    "anteaters",
    "Soviet propaganda posters",
    "Vikings",
    "Turnips",
    "Pokemon",
    "Dungeons and Dragons",
    "The Matrix",
    "The Lord of the Rings",
    "The Hitchhiker's Guide to the Galaxy",
    "The Beatles",
    "The Roman Empire",
    "The Renaissance",
    "The Industrial Revolution",
    "The First World War",
]

# Randomly shuffle the list of topics, and pick the first five.
random.shuffle(TOPICS)
topics = TOPICS[:5]

# Now, we're going to ask the LLM to generate an image generation prompt based on these topics.
prompt = f"""Generate a single prompt for a text-to-image AI model for a very cringe-worthy meme type image about the following topics: {', '.join(topics)}.

    Do not generate more than one caption. This caption will be sent directly to an image generation AI.
    Include stylistic elements that would make the image even more cringe-worthy."""


# Generate the image prompt.
with console.status("Generating image prompt"):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4o",
    )

image_prompt = response.choices[0].message.content
print(image_prompt)

# Generate the image with this prompt.
with console.status("Generating image"):
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        n=1,
        size="1024x1024",
    )

print(image_response.data[0].url)

# Download the image data and display it.
image_data = requests.get(image_response.data[0].url).content
image_bytes = BytesIO(image_data)
img = Image.open(image_bytes)
img.show()
