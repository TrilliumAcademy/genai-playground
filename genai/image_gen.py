#!/usr/bin/env python3

# This script demonstrates how to generate an image using the OctoAI API.

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import base64
from io import BytesIO

from PIL import Image
from octoai.text_gen import ChatMessage
from octoai.client import OctoAI

client = OctoAI()

image_resp = client.image_gen.generate_flux_schnell(
    prompt="A 1950s Cold War era Soviet propaganda poster depicting a rubber chicken and a train engineer."
)
images = image_resp.images

if not images[0].removed_for_safety:
    # Get the Base64 image data out of the response.
    im_bytes = base64.b64decode(images[0].image_b64)
    # Now we can display the image using PIL.
    im_file = BytesIO(im_bytes)
    img = Image.open(im_file)
    img.show()
