import io
import pandas as pd
import streamlit as st
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import openai
from dotenv import load_dotenv
load_dotenv()
import requests
from bs4 import BeautifulSoup
openai.api_key = os.getenv('OPEN_API_KEY')

result_ = ""
pdf_text_result_ = ""
def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}

    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="images/icon.png", page_title="Ask Question to PDF or Link")


c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Ask Question to PDF or Link")
    with c32:
        st.image(
            "images/logo.png",
            width=200,
        )
uploaded_file = st.file_uploader(
    " ",
    type="pdf",
    key="1",
    help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",

)

if uploaded_file is not None:
    output_string = io.StringIO()

    parser = PDFParser(uploaded_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

    # st.write(merged_text)
    pdf_text_result_ = output_string.getvalue()

link_ = st.text_input("Or enter the link of the website", help("You can put link and pdf at the same."))

def entity_extractor(question, pdftext, linktext):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": " Answer the question truthfully based on the given text below. Include verbatim quote and a comment where to find it in the text (paragraph). After the quote write a step by step explanation. Use bullet points. Question:" + question + "Given text: " +"'" +  pdftext + "-" + linktext + "'"}

        ]
    )

    content_value = result['choices'][0]['message']['content']
    return(content_value)
def scraper(link_):
    try:
        url = link_
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.get_text()

        clean_text = text.replace('\n', '').replace('\r', '').replace('\t', '')

    except:
        clean_text = ""
        st.write("Link is not correct!")
    return (clean_text)
form = st.form(key="annotation")
with form:
    question = st.text_area('Enter your question')
    submitted = st.form_submit_button(label="Submit Question")

if submitted:
    if link_ != "":
        text = scraper(link_)
    else:
        text = ""
    result_b = entity_extractor(question,pdf_text_result_, text)
    st.write(result_b)

