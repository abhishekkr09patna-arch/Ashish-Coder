import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("AI chatbot creater by Ashish coder")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input box
user_input = st.chat_input("Type your message...")

if user_input:

    # Show user message
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Send to AI model
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Show bot response
    st.chat_message("assistant").write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })