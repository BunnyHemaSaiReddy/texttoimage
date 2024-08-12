import streamlit as st
import boto3
import json
import os
import base64
import bunny_key
import asyncio
import datetime

def generate_image(prompt, width=512, height=512, number_of_images=3,cfg_scale=10, seed=10):
  for _ in '1':
      if st.button(":[red]cancel"):
        break
      os.environ['AWS_ACCESS_KEY_ID'] = bunny_key.access_id   
      os.environ['AWS_SECRET_ACCESS_KEY'] = bunny_key.api_key
      # os.environ['AWS_SESSION_TOKEN'] = 'YOUR_SESSION_TOKEN' 
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
      l=[]
      for _ in range(len(model_response["images"])):
          base64_image_data = model_response["images"][_]
          image_data = base64.b64decode(base64_image_data)
          l.append(image_data)
      st.markdown("### :rainbow[The images for the prompt]🔥")
      col= st.columns(len(model_response["images"]))
      j=1
      for i in col:
          with i:
           st.image(l[j-1], caption=f"Image {j}", use_column_width=True)
          j+=1



if __name__=="__main__":
    st.markdown(f'<span style="font-size: 25px;">🕗</span> {datetime.datetime.today().hour}:{datetime.datetime.today().minute}:{datetime.datetime.today().second}', unsafe_allow_html=True)
    with st.sidebar :
      size=st.selectbox("** Enter the size image :",['256x256','512x512','1024x1024','2048x2048'],index=2)
      number_images=st.slider("** Select the number of images :",min_value=1,max_value=5)
    prompt=st.text_input('** :blue[Enter a prompt]')
    if size:
        width=size.split('x')[0]
        height=size.split('x')[1]
    if st.button("** :black[Generate]"):
        generate_image(prompt=prompt,width=int(width),height=int(height),number_of_images=int(number_images))
