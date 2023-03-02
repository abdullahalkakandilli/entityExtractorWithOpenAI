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

openai.api_key = os.getenv('OPEN_API_KEY')

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

st.set_page_config(page_icon="images/icon.png", page_title="Entity Extractor")


c2, c3 = st.columns([6, 1])

with c2:
    c31, c32 = st.columns([12, 2])
    with c31:
        st.caption("")
        st.title("Entity Extractor")
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
result_ = ""
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

def entity_extractor():
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Find entities from the given article. Create a dataframe with two column which are the names are 'Entity name' and 'Entity value' and put the values accordingly."
                        "I want to you check names, locations(it might be a place like a school name, or hospital name), ids, dates, companies, emails, phone numbers, and IBANs. Only chek these values. Don't check other values."
                        "Don't check other entities. There might be more than one name, location etc. Find all of them. Giving article: " +"'" +  pdf_text_result_ + "'"}

        ]
    )

    content_value = result['choices'][0]['message']['content']
    return(content_value)

form = st.form(key="annotation")

with form:

    submitted = st.form_submit_button(label="Get entities as an excel file")

result_df = pd.DataFrame()
if submitted:

    result = entity_extractor()

    result_df = result

buffer = io.BytesIO()
# Create a Pandas Excel writer using XlsxWriter as the engine.
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    result_df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()
    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name="Entity-results.xlsx",
        mime="application/vnd.ms-excel"
    )