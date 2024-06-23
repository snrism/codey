# GitHub Code Tutor

A Streamlit application to analyze GitHub repositories and provide coding assistance using an AI model.

## Features

- Clone GitHub repositories and extract code.
- Generate responses to questions about the codebase.
- Modern dark-themed UI.
- Command-line argument for specifying the temp folder.
- Support for both Gemini AI and Anthropic Claude AI.
- Automatic cleanup of temp folder on exit.

## Setup

### Prerequisites

- Python 3.7+
- Streamlit
- Anthropic
- Git
- Google Cloud Platform (GCP) account
- GCP project with Vertex AI enabled

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/codey.git
    cd codey
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your Google Cloud Platform (GCP) credentials:
    - Follow [these instructions](https://cloud.google.com/docs/authentication/getting-started) to create a service account and download the JSON key file.
    - Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON key file:
        ```sh
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
        ```

4. Set up your GCP project details in the `config.py` file:
    - Open `config.py` and set the `PROJECT_ID` and `LOCATION` variables to your GCP project ID and location.

    Example `config.py`:
    ```python
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "your-gcp-location"
    MODEL_ID = "your-model-id"
    ```
5. Set up your Anthropic API Key:
    - Obtain your Anthropic [API key](https://console.anthropic.com/settings/keys) from the Anthropic platform.
    - Set the environment variable `ANTHROPIC_API_KEY` to your Anthropic API key:
        ```sh
        export ANTHROPIC_API_KEY="your-anthropic-api-key"
        ```

### Usage

1. Run the Streamlit app with the following command:
    ```sh
    streamlit run codey.py --temp_folder ./temp
    ```

2. Open your browser and navigate to `http://localhost:8501`.

### Arguments

- `--temp_folder`: Specify the temporary folder to store GitHub files (default: `./temp`).

## Code Structure

- `codey.py`: Main code to run the Streamlit application.
- `services/code_analyzer.py`: Module for cloning and extracting code from GitHub repositories.
- `services/streamlit_helpers.py`: Helper functions for the Streamlit app.

## License

This project is licensed under the MIT License.
