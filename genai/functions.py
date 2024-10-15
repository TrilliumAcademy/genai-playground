# This code demonstrates how to use OpenAI's "function calling" API.

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import argparse
import json
import os
import random

from openai import OpenAI

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


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "generate_random_number",
            "description": "Generate a random number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from": {
                        "type": "integer",
                        "description": "The minimum value of the random number.",
                    },
                    "to": {
                        "type": "integer",
                        "description": "The maximum value of the random number.",
                    },
                },
            },
        },
    },
]


def handle_tool_calls(tool_calls):
    response_messages = []

    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        tool_function_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        console.print(f"Tool call: [blue]{tool_function_name}: {tool_args}")

        if tool_function_name == "generate_random_number":
            from_value = tool_args["from"]
            to_value = tool_args["to"]
            random_number = random.randint(from_value, to_value)
            tool_response = str(random_number)
        else:
            console.print(f"[red]Bad tool function name: {tool_function_name}")
            tool_response = "I don't know how to handle this tool call."

        console.print(f"Tool response: [green]{tool_response}")
        tool_response_message = {
            "role": "tool",
            "content": tool_response,
            "tool_call_id": tool_call_id,
            "name": tool_function_name,
        }
        response_messages.append(tool_response_message)
    return response_messages


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "prompt", default="Roll 4d20 and tell me the final sum.", nargs="?", help="The prompt to use."
    )
    args = argparser.parse_args()
    prompt = args.prompt

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that rolls virtual dice on behalf of the user.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,  # type: ignore
            tools=TOOLS,  # type: ignore
            tool_choice="auto",
        )
        response_dict = response.choices[0].message.to_dict()
        messages.append(response_dict)  # type: ignore
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            tool_response_messages = handle_tool_calls(tool_calls)
            messages.extend(tool_response_messages)
        else:
            print(response_dict["content"])
            break


if __name__ == "__main__":
    main()
