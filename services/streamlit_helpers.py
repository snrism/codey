import streamlit as st
import asyncio
import concurrent.futures
from . import code_analyzer

def apply_custom_css():
    """
    Applies custom CSS for the Streamlit app to provide a modern, dark theme.
    """
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput input {
        background-color: #fff;
        color: #000;
        border: 0.51px solid #333333;
    }
    .stMarkdown h3 {
        color: #4CAF50;
    }
    .stSelectbox>div[data-baseweb="select"] {
        background-color: #ffffff;
        color: #000000;
        border: 0.51px solid #333333;
    }
    .stSelectbox>div[data-baseweb="select"] .css-1wa3eu0-placeholder {
        color: #ffffff;
    }
    .stSelectbox>div[data-baseweb="select"] .css-1hb7zxy-IndicatorsContainer {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_state():
    """
    Initializes the session state variables for the Streamlit app.
    """
    if 'code_index' not in st.session_state:
        st.session_state.code_index = None
    if 'code_text' not in st.session_state:
        st.session_state.code_text = None
    if 'model_chat_initialized' not in st.session_state:
        st.session_state.model_chat_initialized = False
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'chat' not in st.session_state:
        st.session_state.chat = None
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = 'Gemini AI'

def extract_code(github_link: str, temp_folder: str) -> None:
    """
    Extracts code from the provided GitHub link and stores it in the specified temporary folder.

    Args:
        github_link (str): The GitHub repository URL.
        temp_folder (str): The path to the temporary folder.

    Returns:
        None
    """
    code_analyzer.clone_repo(github_link, temp_folder)
    code_index, code_text = code_analyzer.extract_code(temp_folder)
    st.session_state.code_index = code_index
    st.session_state.code_text = code_text

def initialize_model_and_chat() -> None:
    """
    Initializes the model and chat session for code analysis.

    Returns:
        None
    """
    if st.session_state.selected_model == 'Gemini AI':
        if not st.session_state.model_chat_initialized:
            code_analyzer.init_model_session()
            model = code_analyzer.get_model()
            chat = model.start_chat(response_validation=False)  # Disable response validation
            st.session_state.model = model
            st.session_state.chat = chat
            st.session_state.model_chat_initialized = True
    elif st.session_state.selected_model == 'Anthropic Claude AI':
        # Initialize Claude AI specific settings if required
        st.session_state.model_chat_initialized = True

async def generate_response(prompt: str) -> str:
    """
    Generates a response from the model based on the provided prompt.

    Args:
        prompt (str): The input prompt for the model.

    Returns:
        str: The generated response.
    """
    if st.session_state.selected_model == 'Gemini AI':
        response = await code_analyzer.get_chat_response(st.session_state.chat, prompt)
    elif st.session_state.selected_model == 'Anthropic Claude AI':
        response = code_analyzer.get_claude_response(prompt)
    return response

