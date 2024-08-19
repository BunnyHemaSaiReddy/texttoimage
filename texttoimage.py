import streamlit as st
import boto3
import json
import os
import io
import base64
import bunny_key
import asyncio
import datetime

st.header(":rainbow[Bunny Image-Generator]")

def generate_image(prompt, width=512, height=512, number_of_images=3, cfg_scale=10, seed=10):
    os.environ['AWS_ACCESS_KEY_ID'] = bunny_key.access_id   
    os.environ['AWS_SECRET_ACCESS_KEY'] = bunny_key.api_key
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.titan-image-generator-v1"
    native_request = {
        "textToImageParams": {
            "text": prompt
        },
        "taskType": "TEXT_IMAGE",
        "imageGenerationConfig": {
            "cfgScale": cfg_scale,
            "seed": seed,
            "width": width,
            "height": height,
            "numberOfImages": number_of_images
        }
    } 
    request = json.dumps(native_request)

    async def genmsg():
        return client.invoke_model(modelId=model_id, body=request)

    async def spin():
        with st.spinner("Generating..."):
            await asyncio.sleep(10)

    async def main():
        result, _ = await asyncio.gather(genmsg(), spin())
        return result

    response = asyncio.run(main())
    model_response = json.loads(response["body"].read())
    
    st.session_state.images = []
    for base64_image_data in model_response["images"]:
        image_data = base64.b64decode(base64_image_data)
        st.session_state.images.append(image_data)

if "images" not in st.session_state:
    st.session_state.images = []

if __name__ == "__main__":
    st.markdown(f'<span style="font-size: 25px;">🕗</span> {datetime.datetime.today().hour}:{datetime.datetime.today().minute}:{datetime.datetime.today().second}', unsafe_allow_html=True)
    with st.sidebar:
        size = st.selectbox("Enter the size image:", ['256x256', '512x512', '1024x1024'], index=2)
        number_images = st.slider("Select the number of images:", min_value=1, max_value=5)
    
    prompt = st.text_input('Enter a prompt:')
    
    if size:
        width, height = map(int, size.split('x'))
    
    if st.button("Generate"):
        generate_image(prompt=prompt, width=width, height=height, number_of_images=int(number_images))
    
    if st.session_state.images:
        st.markdown("### :rainbow[The images for the prompt]🔥")
        col = st.columns(len(st.session_state.images))
        for idx, image_data in enumerate(st.session_state.images):
            with col[idx]:
                st.image(image_data, caption=f"Image {idx + 1}", use_column_width=True)
                image_bytes = io.BytesIO(image_data)
                download_filename = f"generated_image_by_bunny{idx + 1}.png"
                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name=download_filename,
                    mime="image/png"
                )
