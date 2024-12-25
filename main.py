import os
import google.generativeai as genai
import dotenv
import streamlit as st

# Load environment variables
dotenv.load_dotenv()

# Configure the Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Initialize the chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize messages list in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit App Layout
st.title("🧘‍♀️ Mental Health Wellness Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("Share your thoughts...")

if prompt:
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response from Google AI
    with st.chat_message("assistant"):
        st.spinner("Thinking...")
        response = st.session_state.chat_session.send_message(
            prompt + 
            " and I want you to act as a therapist and give responses accordingly, If the user says things like I want to end my life or kill myself, advice them to talk to a professional therapist or a friend and seek help"
            "Be a good listener, kind, and show empathy, "
            "Just be a good listener and don't mention that you are a chatbot."
        )
        assistant_response = response.text.splitlines()[0]
        st.markdown(assistant_response)

    # Append assistant response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})