import streamlit as st
import logging
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
API_DOCS_URL = "https://docs.streamlit.io/library/api-reference"

# Retrieve and validate API key
CUSTOM_API_KEY = st.secrets.get("CUSTOM_API_KEY", None)
if not CUSTOM_API_KEY:
    st.error("Please add your custom API key to the Streamlit secrets.toml file.")
    st.stop()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Streamly - An Intelligent Streamlit Assistant",
    page_icon="imgs/avatar_streamly.png",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://github.com/AdieLaine/Streamly",
        "Report a bug": "https://github.com/AdieLaine/Streamly",
        "About": """
            ## PY-GPT - An Intelligent Assistant
            ### Powered by PYINDIA

            **GitHub**: https://github.com/AdieLaine/

            The AI Assistant, Streamly, aims to provide the latest updates from Streamlit,
            generate code snippets for Streamlit widgets,
            and answer questions about Streamlit's latest features, issues, and more.
        """
    }
)

# Streamlit Title
st.title("PY-GPT - An Intelligent Assistant")

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def long_running_task(duration):
    """Simulates a long-running operation."""
    time.sleep(duration)
    return "Long-running operation completed."

@st.cache_data(show_spinner=False)
def load_streamlit_updates():
    """Load the latest Streamlit updates from a local JSON file."""
    try:
        with open("data/streamlit_updates.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON: {str(e)}")
        return {}

def initialize_conversation():
    """Initialize the conversation history."""
    assistant_message = "Hello! I am Streamly. How can I assist you with Streamlit today?"
    conversation_history = [
        {"role": "system", "content": "You are Streamly, a specialized AI assistant trained in Streamlit."},
        {"role": "assistant", "content": assistant_message}
    ]
    return conversation_history

@st.cache_data(show_spinner=False)
def on_chat_submit(chat_input, latest_updates):
    """
    Handle chat input submissions and interact with the custom API.

    Parameters:
    - chat_input (str): The chat input from the user.
    - latest_updates (dict): The latest Streamlit updates fetched from a JSON file or API.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip()

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = initialize_conversation()

    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    try:
        # Replace OpenAI with your custom API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CUSTOM_API_KEY}"
        payload = json.dumps({
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_input
                        }
                    ]
                }
            ]
        })
        
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            # response_data = response.json()["candidates"][0]
            assistant_reply = response.json()["candidates"][0]["content"]["parts"][0].get('text', "I couldn't process your request.")
            # assistant_reply = response_data.get('contents')["parts"][0].get('text', "I couldn't process your request.")
        else:
            logging.error(f"API request failed with status {response.status_code}: {response.text}")
            assistant_reply = "I'm unable to fetch a response at the moment. Please try again later."

        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        st.error(f"Error: {str(e)}")

def initialize_session_state():
    """Initialize session state variables."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def main():
    """Display Streamlit updates and handle the chat interface."""
    initialize_session_state()

    if not st.session_state.history:
        initial_bot_message = "Hello! How can I assist you with PY-GPT today?"
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
        st.session_state.conversation_history = initialize_conversation()

    # Sidebar setup
    st.sidebar.title("PY-GPT")
    mode = st.sidebar.radio("Select Mode:", options=["Latest Updates", "Chat with Streamly"], index=1)

    if mode == "Chat with Streamly":
        chat_input = st.chat_input("Ask me about PY-GPT updates:")
        if chat_input:
            latest_updates = load_streamlit_updates()
            on_chat_submit(chat_input, latest_updates)

        # Display chat history
        for message in st.session_state.history[-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
            role = message["role"]
            avatar_image = "imgs/avatar_streamly.png" if role == "assistant" else "imgs/stuser.png"
            with st.chat_message(role, avatar=avatar_image):
                st.write(message["content"])

    else:
        st.markdown(
    """
    <style>
    .pyindia-section {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
    }
    .pyindia-header {
       
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .pyindia-content {
       
        font-size: 16px;
        line-height: 1.6;
        text-align: justify;
    }
    </style>

    <div class="pyindia-section">
        <div class="pyindia-header">PyIndia: Empowering Python and AI Enthusiasts Across India</div>
        <div class="pyindia-content">
            PyIndia is a dynamic community for Python developers, AI enthusiasts, and tech learners across India. It serves as a hub for knowledge sharing, collaboration, and fostering innovation in Python programming and artificial intelligence. Through engaging meetups, hackathons, and workshops, PyIndia explores Python’s applications in AI, data science, web development, and beyond. 
            <br><br>
            The community keeps members updated on cutting-edge AI advancements, tools, and trends, empowering them to stay ahead in the evolving tech landscape. By promoting open-source contributions, networking, and professional growth, PyIndia inspires creativity and drives Python and AI adoption nationwide. Join PyIndia and shape the future!
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


if __name__ == "__main__":
    main()
