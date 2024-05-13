import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

# Set up secret management for API key
api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = api_key

st.title('DALL-E 3 Image Generator')

# User input for the image description
prompt = st.text_input("Enter a description for the image you'd like to generate:", "a futuristic city skyline")

# Slider to select the number of images
num_images = st.slider('How many images would you like to generate?', min_value=1, max_value=5, value=1)

# Button to generate images
if st.button('Generate Images'):
    if prompt:
        with st.spinner('Generating images...'):
            try:
                # Call to OpenAI DALL-E API
                response = openai.Image.create(
                    model="dall-e-3",
                    prompt=prompt,
                    n=num_images,
                    size="1024x1024"
                )
                
                # Display and allow download of images
                for idx, image_data in enumerate(response['data']):
                    image_url = image_data['url']
                    image_response = requests.get(image_url)
                    image = Image.open(BytesIO(image_response.content))
                    st.image(image, caption=f"Image {idx + 1} for: '{prompt}'")
                    
                    # Download button for the image
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download Image",
                        data=byte_im,
                        file_name=f"{prompt.replace(' ', '_')}_{idx + 1}.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"An error occurred while generating images: {e}")
    else:
        st.warning("Please provide a description to generate images.")
else:
    st.write("Adjust the settings and click 'Generate Images' to proceed.")