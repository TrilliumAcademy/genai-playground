# This is a simple web app that provides a ChatGPT-like user interface.
#
# To run:
#  poetry run python -m streamlit run genai/chat_demo.py

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import os
from openai import OpenAI
import streamlit as st

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

st.title("AI Chat Demo")


def do_query():
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="gpt-4o",
    )
    response_message = response.choices[0].message.dict()
    st.session_state.messages.append(response_message)
    st.write(response_message["content"])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] not in ["user", "assistant"]:
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything"):
    msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        do_query()
