import streamlit as st
import time
from pathlib import Path

# Define a function to simulate document generation
def generate_document(template, uploaded_file):
    time.sleep(3)  # Simulate processing time
    output_path = Path("generated_document.docx")
    with open(output_path, "w") as f:
        f.write(f"Generated document based on {template} with data from {uploaded_file.name}")
    return output_path

def main():
    st.set_page_config(page_title="DocuHR", layout="centered")

    # Page header with Affine logo
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="https://acis.affineanalytics.co.in/assets/images/logo_small.png" alt="Affine Logo" width="80" height="70">
            <h1 style='color: #1a1a1a; font-family: "Helvetica Neue", Arial, sans-serif;'>
                DocuHR: Smart HR Documentation
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Styling
    st.markdown(
        """
        <style>
            .stButton > button {
                background-color: #008080;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                transition: transform 0.3s, background-color 0.3s;
            }
            .stButton > button:hover {
                transform: scale(1.05);
                background-color: #006666;
            }
            .header-div {
                background: linear-gradient(135deg, #20c997, #007f80);
                padding: 5px 10px;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                text-align: center;
                font-size: 14px;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                letter-spacing: 0.5px;
            }
            body {
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Select a template
    st.markdown("<div class='header-div'>Select a Template:</div>", unsafe_allow_html=True)
    template_paths = {
        "Offshore Appointment Letter": "templates/Offshore_Appointment_letter.docx",
        "Offshore Relieving Letter": "templates/Offshore_Relieving_Letter.docx",
        "Onsite Relieving Letter": "templates/Onsite_Relieving_Letter.docx",
        "Onsite Internship Letter": "templates/Onsite_Internship_Letter.docx",
    }
    selected_template = st.selectbox("Templates", list(template_paths.keys()))

    # File uploader for input
    st.markdown("<div class='header-div'>Upload Input CSV/Excel File:</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

    # Text input for output file name
    st.markdown("<div class='header-div'>Enter Output File Name:</div>", unsafe_allow_html=True)
    output_file_name = st.text_input("", placeholder="Enter a name for the output file (e.g., HR_Document.docx)")

    # Generate Document button
    if st.button("Generate Document"):
        if not uploaded_file or not output_file_name:
            st.error("Please upload a file and enter a valid output name.")
        else:
            with st.spinner("Generating your document. Please wait..."):
                output_path = generate_document(selected_template, uploaded_file)
                st.success("Document generated successfully!")
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Document",
                        data=file,
                        file_name=output_file_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

if __name__ == "__main__":
    main()

