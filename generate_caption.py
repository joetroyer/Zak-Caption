import streamlit as st
import requests
import base64
import os
import time
    
st.markdown("<h1 style='text-align: center;'>Image Caption Generator</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 20px;'>Use AI to generate captions for any images.</h1>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

def is_file_size_acceptable(file, max_size):
    return file.size <= max_size  

def upload_image():
    uploaded_file = st.file_uploader('1.UPLOAD AN IMAGE OR PHOTO (MAX 4MB)', type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    
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
    selected_vibe = st.selectbox("2.SELECT VIBE", options=vibes)
    return selected_vibe

def additional_prompt():    
    add_prompt = st.text_input("3.ADDITIONAL PROMPT (OPTIONAL)", placeholder="eg. the photo is in Byron Bay")
    return add_prompt

def generate_caption(image_filename, image_data, vibe, prompt):
    
    placeholder = st.empty()
 

    st.write("""
    <style>
    .stButton > button {
        width: 250px;
        height: 60px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Generate Captions"):
        if image_filename is not None and image_data is not None:

            with placeholder.container():
                st.write("Generating captions...")   
            caption = call_api(image_data, vibe, prompt)
            caption_2 = call_api(image_data, vibe, prompt)

            source_background_color = st.get_option("theme.backgroundColor")

            placeholder.empty()

            box_style = """
            <style>
            .shadow-box {
                background-color: #333333;
                border-radius: 15px; /* Increase the curvature of the edges */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                padding: 20px;
                margin: 20px 0;
                max-width: auto;
                color: #ffffff; /* Set text color to white */
            }
            </style>
            """

            # Add the CSS to the Streamlit app
            st.markdown(box_style, unsafe_allow_html=True)

            # st.markdown("<h1 style='text-align: center; font-size: 20px;'>Generated Captions:</h1>", unsafe_allow_html=True)
            
            box_content = f"""
            <div class="shadow-box">
                {caption}
            </div>
            """
            st.markdown(box_content, unsafe_allow_html=True)

            time.sleep(2)
            box_content = f"""
            <div class="shadow-box">
                {caption_2}
            </div>
            """
            st.markdown(box_content, unsafe_allow_html=True)

        else:
            st.error("Please upload an image first.")

def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')
  
def call_api(image_data, vibe, prompt):

    code_k=st.secrets["openai_apikey"]

    placeholder = st.empty()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {code_k}"
    }

    base64_image = base64.b64encode(image_data).decode('utf-8')

    prompt_use = f"Generate a caption for the image. Include 3 smileys. Caption must be 150 characters at least for the uploaded image. The caption must reflect the specified vibe {vibe} and any additional details provided : {prompt}. Include three relevant hashtags at the end of the caption."
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_use,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


    if response.status_code == 200:
        data = response.json()
        content = data['choices'][0]['message']['content']
        print(content)

        # source_background_color = st.get_option("theme.backgroundColor")

        # placeholder.empty()

        # box_style = """
        # <style>
        # .shadow-box {
        #     background-color: #333333;
        #     border-radius: 15px; /* Increase the curvature of the edges */
        #     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        #     padding: 20px;
        #     margin: 20px 0;
        #     max-width: auto;
        #     color: #ffffff; /* Set text color to white */
        # }
        # </style>
        # """

        # # Add the CSS to the Streamlit app
        # st.markdown(box_style, unsafe_allow_html=True)

        # box_content = f"""
        # <div class="shadow-box">
        #     <h3>Generated Captions:</h3>
        #     {content}
        # </div>
        # """
        # st.markdown(box_content, unsafe_allow_html=True)

        return content
    else:
        placeholder.empty()

        source_background_color = st.get_option("theme.backgroundColor")

        print("Error:", response.text)
        st.markdown(f"""
        <div style="background-color:{source_background_color};border-radius:10px;">
            <h3>Error generating caption, please try later...</h3>
        </div>
        """, unsafe_allow_html=True)
        return None
    

def main():
    image_filename, image_data, base64_image = upload_image()
    
    selected_vibe = select_vibe()

    additional_prompt_text = additional_prompt()
    
    generate_caption(image_filename, image_data, selected_vibe, additional_prompt_text)

if __name__ == "__main__":
    main()
