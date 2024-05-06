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

# List of allowed emails
allowed_emails = ["email1@example.com", "email2@example.com"]

# Initialize Streamlit app
st.title('Restricted Image Generator')

# Get user login (email)
user_email = st.text_input("Enter your email to access", type="default")

if user_email in allowed_emails:
    # Image prompt
    prompt = st.text_area("Enter a prompt for the image you want to generate", height=150, value="Describe the image here...")

    # Number of images
    num_images = st.slider("Number of images", 1, 5, 1)

    # Choose model
    model_choice = st.radio("Choose a model", ["DALL-E 3", "GPT-4 Turbo"])

    # Generate button
    if st.button("Generate Image"):
        if prompt.strip() == "":
            st.error("Please enter a prompt.")
        else:
            # Use environment variable for API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                st.error("OpenAI API key not found in environment variables.")
                st.stop()
            # Generate and display images
            try:
                if model_choice == "DALL-E 3":
                    images = generate_image(prompt, api_key, model="dall-e-3", n=num_images)
                else:
                    images = generate_image(prompt, api_key, model="text-davinci-003", n=num_images)  # GPT-4 Turbo
                for image in images:
                    st.image(image, use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.error("Access denied. Your email is not on the allowed list.")
