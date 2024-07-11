import streamlit as st
import requests
import base64
import os

# Set up the title and description of the app
st.markdown("<h1 style='text-align: center;'>Image Caption Generator</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 20px;'>Use AI to generate captions for any images.</h1>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# Function to check if file size is acceptable
def is_file_size_acceptable(file, max_size):
    return file.size <= max_size  

# Function to handle image upload
def upload_image():
    uploaded_file = st.file_uploader('1. UPLOAD AN IMAGE OR PHOTO (MAX 4MB)', type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        if is_file_size_acceptable(uploaded_file, 4*1024*1024):
            st.image(uploaded_file, width=300)
            st.success("Image uploaded successfully")
            filename = os.path.basename(uploaded_file.name)
            image_data = uploaded_file.getvalue()  # Already bytes
            base64_image = encode_image(image_data)
            
            return filename, image_data, base64_image
        else:
            st.error("File size exceeds the maximum limit of 4 MB")
    return None, None, None  # Indicate no image uploaded

# Function to encode image to base64
def encode_image(image_data):
    return base64.b64encode(image_data).decode()

# Function to select the vibe for the caption
def select_vibe():
    vibes = [
        "😆 Fun",
        "😜 Joke",
        "🤣 Funny",
        "🥳 Happy",
        "😑 Serious",
        "😭 Sad",
        "😡 Angry",
        "🙌🏻 Ecstatic",
        "🧐 Curious",
        "📔 Informative",
        "😻 Cute",
        "🧊 Cool",
        "😲 Controversial",
    ]
    selected_vibe = st.selectbox("2. SELECT VIBE", options=vibes)
    return selected_vibe

# Function to get additional prompt from the user
def additional_prompt():    
    add_prompt = st.text_input("3. ADDITIONAL PROMPT (OPTIONAL)", placeholder="e.g., the photo is in Byron Bay")
    return add_prompt

# Function to generate caption using OpenAI API
def generate_caption(image_filename, image_data, vibe, prompt):
    try:
        api_key = st.secrets['openai']['openai_apikey']
    except KeyError:
        st.error("API key not found. Please add your OpenAI API key to the secrets.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simplified payload without image data
    payload = {
        "model": "text-davinci-003",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates captions for images."
            },
            {
                "role": "user",
                "content": f"Create a caption for an image with vibe '{vibe}' and prompt '{prompt}'. (Image description: {image_filename})"
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        content = data['choices'][0]['message']['content']
        st.write(content)
        return content
    else:
        st.error(f"Error generating caption, please try later... (Status code: {response.status_code})")
        st.error(f"Response: {response.text}")
        return None

# Main function to run the app
def main():
    image_filename, image_data, base64_image = upload_image()
    
    if image_filename and image_data:
        selected_vibe = select_vibe()
        additional_prompt_text = additional_prompt()
        
        if st.button("Generate Caption"):
            generate_caption(image_filename, image_data, selected_vibe, additional_prompt_text)

if __name__ == "__main__":
    main()
