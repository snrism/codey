import os
import git
import asyncio
import magika
import requests
import shutil
import vertexai
from typing import Tuple, List
from pathlib import Path
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Tool,
    ChatSession
)
import anthropic
import config

def init_model_session() -> None:
    """
    Initialize the Vertex AI session.

    Returns:
        None
    """
    vertexai.init(project=config.PROJECT_ID, location=config.LOCATION)

def get_magika_instance() -> magika.Magika:
    """
    Get an instance of the Magika class.

    Returns:
        magika.Magika: An instance of the Magika class.
    """
    return magika.Magika()

def get_model() -> GenerativeModel:
    """
    Get an instance of the GenerativeModel configured for code assistance.

    Returns:
        GenerativeModel: A configured instance of the GenerativeModel.
    """
    model = GenerativeModel(
        config.MODEL_ID,
        system_instruction=[
            "You are a coding expert and a tutor to help the user learn more about the codebase.",
            "Your mission is to answer all code related questions with given context and instructions.",
        ],
    )
    return model

def get_claude_response(prompt: str) -> str:
    """
    Get a response from the Anthropic Claude AI model.

    Args:
        prompt (str): The input prompt for the model.

    Returns:
        str: The generated response.
    """
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You are a coding expert and a tutor to help the user learn more about the codebase.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def clone_repo(repo_url: str, repo_dir: str) -> None:
    """
    Clone a GitHub repository to a specified directory.

    Args:
        repo_url (str): The URL of the GitHub repository.
        repo_dir (str): The directory to clone the repository into.

    Returns:
        None
    """
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    try:
        git.Repo.clone_from(repo_url, repo_dir)
    except Exception as e:
        raise RuntimeError(f"Failed to clone repository: {e}")

def extract_code(repo_dir: str) -> Tuple[List[str], str]:
    """
    Create an index and extract content from code/text files in the repository.

    Args:
        repo_dir (str): The directory of the cloned repository.

    Returns:
        Tuple[List[str], str]: A tuple containing the code index and concatenated code text.
    """
    code_index = []
    code_text = ""
    magika_instance = get_magika_instance()
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_dir)
            code_index.append(relative_path)

            file_type = magika_instance.identify_path(Path(file_path))
            if file_type.output.group in ("text", "code"):
                try:
                    with open(file_path, "r") as file_content:
                        code_text += f"----- File: {relative_path} -----\n"
                        code_text += file_content.read()
                        code_text += "\n-------------------------\n"
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return code_index, code_text

def generate_code_prompt(question: str, code_index: List[str], code_text: str) -> str:
    """
    Generate a prompt to a code-related question.

    Args:
        question (str): The question about the codebase.
        code_index (List[str]): The index of files in the codebase.
        code_text (str): The concatenated text of all code files.

    Returns:
        str: The generated prompt.
    """
    prompt = f"""
    Question: {question}

    Context:
    - The entire codebase is provided below.
    - Here is an index of all of the files in the codebase:
      \n\n{code_index}\n\n.
    - Then each of the files is concatenated together. You will find all of the code you need:
      \n\n{code_text}\n\n

    Answer:
    """
    return prompt

async def get_chat_response(chat: ChatSession, prompt: str) -> str:
    """
    Generate a response from the chat session based on the provided prompt.

    Args:
        chat (ChatSession): The chat session.
        prompt (str): The prompt to send to the chat session.

    Returns:
        str: The generated response.
    """
    text_response = []
    try:
        responses = chat.send_message(prompt, stream=True)
        for chunk in responses:
            text_response.append(chunk.text)
    except Exception as e:
        raise RuntimeError(f"Error generating chat response: {e}")
    return "".join(text_response)
