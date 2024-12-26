import streamlit as st
# from document_generation import populate_docx_with_gpt
from document_generation_hr import DocumentGeneration
import pandas as pd


# Hardcoded credentials (replace with secure storage in production)
USER_CREDENTIALS = {
    st.secrets["LOGIN_USERNAME"]: st.secrets["LOGIN_PASSWORD"]
}

def authenticate(username, password):
    """
    Authenticate the user by checking the username and password.
    Replace this with a secure database or API in production.
    """
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

def login_form():
    """
    Display the login form and handle authentication logic.
    Returns True if authenticated, False otherwise.
    """
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Welcome, you are authenticated!")
            st.rerun()  # Refresh the page to load the main app
        else:
            st.error("Invalid username or password.")
            return False
    return False

def logout_button():
    """
    Display a logout button if the user is authenticated.
    """
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()


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
    
        # Initialize session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


    if not st.session_state.authenticated:
        # Authentication form
        login_form()
    else:
        logout_button()

        template_paths = {
            "Offshore_Appointment letter": "templates/Offshore_Appointment letter.docx",
            "Offshore_Relieving Letter": "templates/Offshore_Relieving Letter.docx",
            "Offshore_Appointment letter_with Relocation": "templates/Offshore_Appointment letter_with Relocation.docx",
            "Offshore_Internship Letter": "templates/Offshore_Internship Letter.docx",
            "Onsite_Internship letter": "templates/Onsite_Internship letter-1.docx",
            "Onsite_Offer letter.docx": "templates/Onsite_Offer letter-2.docx",
            "Onsite_Relieving Letter.docx":"templates/Onsite_Relieving Letter-2.docx"
        }


    #        "Onsite_Offer Letter": "templates/Onsite_Offer Letter.docx",
            # "Onsite_Relieving Letter": "templates/Onsite_Relieving Letter.docx",
            # "Onsite_Internship letter": "templates/Onsite_Internship letter.docx",

        # Dropdown to select a template
        selected_template = st.selectbox("Select a Template", list(template_paths.keys()))
        template_path = ''
        template_path = template_paths[selected_template]


        # File upload for CSV
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

        data = None

        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)  # Read CSV
            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                data = pd.read_excel(uploaded_file)  # Read Excel
            
            # Display the uploaded data in the Streamlit app
            st.write("Uploaded Data:")
            st.dataframe(data)

        # Submit button
        if any(template_path) and data is not None:
            if st.button("Generate Document"):
                doc_gen = DocumentGeneration(template_path=template_path, data=data, template=selected_template)
                with st.spinner("Wait for it... Document generation in progess"):
                    # buffer_doc = populate_docx_with_gpt(template_path, data)
                    buffer_doc, file_name = doc_gen.doc_gen_main()
                    # Provide a download button
                    # if '.zip' in file_name:
                    st.download_button(
                        label="Download Generated Document",
                        data=buffer_doc.getvalue(),
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                    # else:
                    #     st.download_button(
                    #         label="Download Generated Document",
                    #         data=buffer_doc.getvalue(),
                    #         file_name=file_name,
                    #         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        # ) 

if __name__ == "__main__":
    main()