import os
import streamlit as st
import openai
import json
import time

# Function for text generation
# Function for text generation
def generate_text(prompt, api_key, discussions):
    openai.api_key = api_key
    
    discussions.append({"role": "user", "content": prompt})
    
    completion = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # GPT-4 Turbo
        messages=discussions
    )

    response = completion.choices[0].message.content
    discussions.append({"role": "assistant", "content": response})
    return response, discussions


# List of allowed emails
allowed_emails = ["email1@example.com", "email2@example.com"]

# Initialize Streamlit app
st.title('Restricted AI Assistant')

# Get user login (email)
user_email = st.text_input("Enter your email to access", type="default")

if user_email in allowed_emails:
    # Initialize discussion history
    discussions = [{"role": "system", "content": "You are a helpful assistant."}]
    
    while True:
        # User input
        prompt = st.text_input("Enter your prompt (type 'quit' to exit)", value="Hi, how are you?")
        
        # Check if user wants to quit
        if prompt.lower().strip() == "quit":
            break
        
        # Generate response
        if st.button("Generate Response"):
            if prompt.strip() == "":
                st.error("Please enter a prompt.")
            else:
                # Use environment variable for API key
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    st.error("OpenAI API key not found in environment variables.")
                    st.stop()
                # Generate and display response
                try:
                    response, discussions = generate_text(prompt, api_key, discussions)
                    st.text("AI Response:")
                    st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.error("Access denied. Your email is not on the allowed list.")
