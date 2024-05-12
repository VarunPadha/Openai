import streamlit as st
import openai
import firebase_admin
from firebase_admin import credentials, firestore

try:
    cred = credentials.Certificate('path/to/your_firebase_service_account.json')
    firebase_admin.initialize_app(cred)
except ValueError:
    # Ignore if the app is already initialized
    pass

db = firestore.client()

# OpenAI API Key from Streamlit Secrets (securely)
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_conversation_history(user_id):
    doc_ref = db.collection('conversations').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('discussions', [{"role": "system", "content": "You are a helpful assistant."}])
    else:
        return [{"role": "system", "content": "You are a helpful assistant."}]

def add_message_to_conversation(user_id, role, content):
    db.collection('conversations').document(user_id).set({
        'discussions': firestore.ArrayUnion([{'role': role, 'content': content}])
    }, merge=True)

def fetch_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        max_tokens=150
    )
    return response.choices[0].message['content']

def main():
    st.title('Chat with GPT-4')
    user_id = st.text_input("Enter your User ID:")
    
    if user_id:
        conversations = get_conversation_history(user_id)
        user_input = st.text_input("Type your message:", key="input")

        if st.button("Send"):
            conversations.append({"role": "user", "content": user_input})
            ai_response = fetch_response(conversations)
            conversations.append({"role": "assistant", "content": ai_response})
            add_message_to_conversation(user_id, "user", user_input)
            add_message_to_conversation(user_id, "assistant", ai_response)
            st.experimental_rerun()

        st.write("## Conversation History")
        for message in conversations:
            if message['role'] == "user":
                st.text_area("You", value=message['content'], height=75, disabled=True)
            else:
                st.text_area("AI", value=message['content'], height=75, disabled=True)

if __name__ == "__main__":
    main()