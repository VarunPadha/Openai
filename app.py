import os
import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Function to generate image
def generate_image(prompt, api_key, model="dall-e-3", n=1):
    openai.api_key = api_key
    response = openai.Image.create(
        model=model,
        prompt=prompt,
        n=n,
        response_format="url"
    )

    images = []
    for data in response['data']:
        image_url = data['url']
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        images.append(image)

    return images

# Function for text generation
def generate_text(prompt, api_key):
    openai.api_key = api_key
    discussions = [{"role": "system", "content": "You are a helpful assistant."}]
    discussions.append({"role": "user", "content": prompt})
    
    completion = openai.ChatCompletion.create(
        model="text-davinci-003",  # GPT-4 Turbo
        messages=discussions
    )

    response = completion.choices[0].message.content
    return response

# List of allowed emails
allowed_emails = ["email1@example.com", "email2@example.com"]

# Initialize Streamlit app
st.title('Restricted AI Assistant')

# Get user login (email)
user_email = st.text_input("Enter your email to access", type="default")

if user_email in allowed_emails:
    # Input prompt
    prompt_type = st.radio("Select prompt type", ["Text", "Image"])

    if prompt_type == "Text":
        prompt = st.text_input("Enter your prompt", value="Hi, how are you?")
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
                    response = generate_text(prompt, api_key)
                    st.text("AI Response:")
                    st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
    elif prompt_type == "Image":
        # Image prompt
        image_prompt = st.text_area("Enter a prompt for the image you want to generate", height=150, value="Describe the image here...")
        if st.button("Generate Image"):
            if image_prompt.strip() == "":
                st.error("Please enter a prompt.")
            else:
                # Use environment variable for API key
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    st.error("OpenAI API key not found in environment variables.")
                    st.stop()
                # Generate and display images
                try:
                    images = generate_image(image_prompt, api_key)
                    for image in images:
                        st.image(image, use_column_width=True)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.error("Access denied. Your email is not on the allowed list.")
