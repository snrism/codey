import streamlit as st
import os
import asyncio
import argparse
import atexit
from services import code_analyzer, streamlit_helpers

# Argument parser for temp folder
parser = argparse.ArgumentParser(description='GitHub Code Tutor')
parser.add_argument('--temp_folder', type=str, default='./temp', help='Temporary folder to store GitHub files')
args = parser.parse_args()

# Ensure temp folder exists
os.makedirs(args.temp_folder, exist_ok=True)

# Register atexit to delete temp folder on exit
def cleanup_temp_folder():
    if os.path.exists(args.temp_folder):
        import shutil
        shutil.rmtree(args.temp_folder)

atexit.register(cleanup_temp_folder)

# Initialize the Streamlit app
st.set_page_config(page_title="GitHub Code Tutor", layout="wide")
st.title("GitHub Code Tutor")
streamlit_helpers.apply_custom_css()
# State initialization
streamlit_helpers.initialize_state()

# Create columns for the model selection and GitHub link input
col1, col2 = st.columns([1, 3])

with col1:
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'Gemini AI'
    st.session_state.selected_model = st.selectbox(
        "Select AI Model:",
        ["Anthropic Claude AI", "Gemini AI"],
        index=["Anthropic Claude AI", "Gemini AI"].index(st.session_state.selected_model)
    )

with col2:
    if st.session_state.code_index is None:
        github_link = st.text_input("Enter GitHub Repository URL:")

# Button to trigger the analysis
if st.button("Analyze") and st.session_state.code_index is None and github_link:
    with st.spinner("Extracting code..."):
        streamlit_helpers.extract_code(github_link, args.temp_folder)

    # Initialize the model and chat only once
    streamlit_helpers.initialize_model_and_chat()

    st.success("GitHub repository processed. You can now ask questions about the codebase.")
else:
    st.info("GitHub repository processed. You can now ask questions about the codebase.")

# Additional chat prompt
chat_prompt = st.text_input("Ask a question about the codebase:")

if st.button("Send") and chat_prompt:
    # Create the prompt using the code_index and code_text
    prompt = code_analyzer.generate_code_prompt(chat_prompt, st.session_state.code_index, st.session_state.code_text)

    with st.spinner("Generating response..."):
        try:
            response = asyncio.run(streamlit_helpers.generate_response(prompt))
            # Display the response as Markdown
            st.markdown("### Response:")
            st.markdown(response, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")
