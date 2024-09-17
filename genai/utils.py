# Common utilities.

from dotenv import load_dotenv

import os
from openai import OpenAI


def setup():
    load_dotenv()

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
    return client
