import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import requests
from PIL import Image
import io
## Function To get response from LLAma 2 model

def getLLamaresponse(input_text,no_words,blog_style):

    ### LLama2 model
    llm=CTransformers(model=r'C:\Users\pooja\OneDrive\Desktop\Blog Generation\llama-2-7b-chat.ggmlv3.q2_K.bin',
                  model_type='llama',
                  config={'max_new_tokens':256,
                          'temperature':0.01})
    
    ## Prompt Template

    template="""
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
            """
    
    prompt=PromptTemplate(input_variables=["blog_style","input_text",'no_words'],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm(prompt.format(blog_style=blog_style,input_text=input_text,no_words=no_words))
    return response
def create_word_docx(blog_text, image_url):
    doc = Document()
    doc.add_paragraph(blog_text)
    if image_url:
        response = requests.get(image_url)
        image_stream = io.BytesIO(response.content)
        image = Image.open(image_stream)
        image.thumbnail((400, 400))  # Adjust size as needed
        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)
        doc.add_picture(image_stream, width=Inches(4))  # Adjust width as needed
    return doc
def fetch_photo(query):
    api_key = 'K9RdcbmPcuvUFGHU7hSaWNdwYewuJjwgerRtzV8DxmvOhIdzshVQtuAz' # Replace with your Pexels API key

    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': api_key,
    }

    params = {
        'query': query,
        'per_page': 1,
    }

    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            src_original_url = photos[0]['src']['original']
            return src_original_url
        else:
            print("No photos found for the given query.")
    else:
        print(f"Error: {response.status_code}, {response.text}")
    
    return None





st.set_page_config(page_title="Auto Blogger using llama2",
                    page_icon='🤖',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header(" Auto Blogger using llama2🤖")

input_text=st.text_input("Enter the Blog Topic")

## creating to more columns for additonal 2 fields

col1,col2=st.columns([5,5])

with col1:
    no_words=st.text_input('No of Words')
with col2:
    blog_style=st.selectbox('Writing the blog for',
                            ('Researchers','Data Scientist','Common People'),index=0)
    
submit=st.button("Generate")

## Final response
if submit:
    image_input = fetch_photo(input_text)
    if image_input:
        st.image(image_input, width=250,use_column_width=False, output_format='PNG')   # Adjust the width as needed
    st.write(getLLamaresponse(input_text,no_words,blog_style))
    ## Fetch and display photo based on the blog topic
