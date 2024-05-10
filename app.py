import openai
import streamlit as st

# Setup the API key from Streamlit's secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_image(prompt, model="dalle-3", session_info=None):
    try:
        response = openai.Image.create(
            model=model, 
            prompt=prompt, 
            n=1,  # Number of images to generate
            size="1024x1024"  # Image resolution
        )
        
        image_url = response['data'][0]['url']  # Assuming the API returns an image URL
        return image_url

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title('AI-Based Image Generator with OpenAI')

    prompt = st.text_area("Enter a description for the image you want to generate:", height=150)
    button = st.button("Generate Image")

    if button and prompt:
        with st.spinner('Generating Image...'):
            image_url = generate_image(prompt)
            if image_url:
                st.image(image_url, caption='Generated Image')
            else:
                st.error("Failed to generate image.")

if __name__ == "__main__":
    main()