import streamlit as st
from document_generation import populate_docx_with_gpt
import pandas as pd

def main():
    # Initialize session state for the result if it doesn't exist
    if "result" not in st.session_state:
        st.session_state.result = None

    st.markdown("""
    <div style='text-align: center; margin-top:-40px; margin-bottom: 5px;margin-left: -50px;'>
    <h2 style='font-size: 40px; font-family: Courier New, monospace;
                    letter-spacing: 2px; text-decoration: none;'>
    <img src="https://acis.affineanalytics.co.in/assets/images/logo_small.png" alt="logo" width="70" height="60">
    <span style='background: linear-gradient(45deg, #ed4965, #c05aaf);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            text-shadow: none;'>
                    DocuHR: Smart HR Documentation!
    </span>
    <span style='font-size: 40%;'>
    </span>
    </h2>
    </div>
    """, unsafe_allow_html=True)

    st.write("Select a template and upload a input csv/excel file:")

    template_paths = {
        "Offshore_Appointment letter": "templates/Offshore_Appointment letter.docx",
        "Offshore_Relieving Letter": "templates/Offshore_Relieving Letter.docx",
        "Onsite_Relieving Letter": "templates/Onsite_Relieving Letter.docx",
        "Offshore_Appointment letter_with Relocation": "templates/Offshore_Appointment letter_with Relocation.docx",
        "Onsite_Internship letter": "templates/Onsite_Internship letter.docx",
        "Offshore_Internship Letter": "templates/Offshore_Internship Letter.docx",
        "Onsite_Offer Letter": "templates/Onsite_Offer Letter.docx",
    }

    # Dropdown to select a template
    selected_template = st.selectbox("Select a Template", list(template_paths.keys()))
    template_path = template_paths[selected_template]


    # File upload for CSV
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

    data = None
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)  # Read CSV
    elif uploaded_file.name.endswith((".xlsx", ".xls")):
        data = pd.read_excel(uploaded_file)  # Read Excel
    
    # Display the uploaded data in the Streamlit app
    st.write("Uploaded Data:")
    st.dataframe(data)

    # Submit button
    if st.button("Generate Document"):
        with st.spinner("Wait for it... Document generation in progess"):
            buffer_doc = populate_docx_with_gpt(template_path, data)
            # Provide a download button
            st.download_button(
                label="Download Generated Document",
                data=buffer_doc.getvalue(),
                file_name="generated_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

if __name__ == "__main__":
    main()