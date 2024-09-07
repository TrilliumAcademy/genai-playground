# This is a simple web app that provides a ChatGPT-like user interface.
#
# To run:
#  poetry run python -m streamlit run genai/chat_demo.py

# This needs to come before we import other things.
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from octoai.text_gen import ChatMessage
from octoai.client import OctoAI


st.title("AI Chat Demo")


def do_query():
    response = client.text_gen.create_chat_completion(
        max_tokens=512,
        messages=st.session_state.messages,
        model="meta-llama-3.1-8b-instruct",
        presence_penalty=0,
        temperature=0,
        top_p=1,
    )
    response_message = response.choices[0].message
    st.session_state.messages.append(response_message)
    st.write(response_message.content)


# Set OpenAI API key from Streamlit secrets
client = OctoAI()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message.role not in ["user", "assistant"]:
        continue
    with st.chat_message(message.role):
        st.markdown(message.content)

# Accept user input
if prompt := st.chat_input("Ask me anything"):
    msg = ChatMessage(role="user", content=prompt)
    st.session_state.messages.append(msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        do_query()
