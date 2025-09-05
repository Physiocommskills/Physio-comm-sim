import streamlit as st
from transformers import pipeline
import datetime

# ---- Set up AI model (free Hugging Face model) ----
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

# ---- Define patient persona ----
PATIENT_PROMPT = """You are a patient speaking with a physiotherapy student. 
Stay in character as: 
- Name: Alex Johnson
- 42 years old
- Recovering from a knee injury
- Worried about not being able to return to sport
- Sometimes skeptical about physiotherapy exercises

Keep responses realistic, short (1–3 sentences), and conversational.
Do not break character.
"""

# ---- Streamlit UI ----
st.title("Physiotherapy Communication Skills Trainer")
st.write("Chat with your patient avatar. Your conversation will be saved at the end.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("You (Physio Student):", key="input")

if user_input:
    # Append student input
    st.session_state.conversation.append(("Student", user_input))

    # Generate AI reply
    context = PATIENT_PROMPT + "\n\n"
    for role, text in st.session_state.conversation:
        context += f"{role}: {text}\n"
    ai_reply = chatbot(context)[0]['generated_text'].split("Student:")[-1].strip()

    # Append AI reply
    st.session_state.conversation.append(("Patient", ai_reply))

# Display chat
for role, text in st.session_state.conversation:
    st.markdown(f"**{role}:** {text}")

# Download transcript
if st.session_state.conversation:
    transcript_text = "\n".join([f"{r}: {t}" for r, t in st.session_state.conversation])
    filename = f"transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.download_button("Download Transcript", transcript_text, file_name=filename)
