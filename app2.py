import io
import base64
from pdf2image import convert_from_bytes, pdfinfo_from_bytes
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Environment setup
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input, pdf_content, prompt):
    # Update to use a supported model
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Debug: Check for poppler path
        st.write("Poppler path check:")
        os.system("where pdfinfo")  # Windows command to find path of pdfinfo

        # Convert the PDF to image
        try:
            images = convert_from_bytes(uploaded_file.read())
        except Exception as e:
            st.write(f"Error in converting PDF to images: {e}")
            raise

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Resume Analyzer")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of Data Science, Full Stack web development, Big Data Engineer, DEVOPS, Data Analyst,
 your task is to review the provided resume against the job description for these profiles.
 Please share your professional evaluation on whether the candidate's profile aligns with the role.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack web development, Big Data Engineer, DEVOPS, Data Analyst, and deep ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please upload the resume")