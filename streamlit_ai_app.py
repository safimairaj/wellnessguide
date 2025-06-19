import streamlit as st
import requests
import json
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Wellness Guide Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and beautiful UI
st.markdown("""
<style>
    /* Dark theme variables */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1d29;
        --bg-tertiary: #262730;
        --text-primary: #ffffff;
        --text-secondary: #a0a0a0;
        --accent-color: #ff6b6b;
        --success-color: #4ecdc4;
        --border-color: #333333;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1d29 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background: var(--bg-secondary);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #4ecdc4, #44b7b8);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: var(--bg-tertiary);
        border: 2px solid var(--border-color);
        border-radius: 25px;
        color: var(--text-primary);
        padding: 15px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--bg-secondary);
    }
    
    /* Status indicators */
    .typing-indicator {
        display: flex;
        align-items: center;
        color: var(--text-secondary);
        font-style: italic;
        margin: 10px 0;
    }
    
    .typing-indicator::after {
        content: "...";
        animation: dots 1.5s infinite;
    }
    
    @keyframes dots {
        0%, 20% { color: transparent; }
        40% { color: var(--text-secondary); }
        100% { color: transparent; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .user-message, .bot-message {
            margin-left: 5%;
            margin-right: 5%;
        }
        
        .main-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

def call_huggingface_api(message, api_key):
    """
    Call Hugging Face API for Wellness Guide assistant
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Your Wellness Guide assistant ID
        assistant_id = "6852d7140fc76543c8fed690"
        
        # Note: HuggingChat assistants don't have direct REST API access yet
        # You'll need to implement one of these approaches:
        # 1. Use HuggingChat's web interface with automation (selenium/playwright)
        # 2. Use a similar wellness-focused model from Hugging Face Inference API
        # 3. Wait for official HuggingChat Assistant API
        
        # For now, using a general health/wellness focused model as fallback
        # Replace with your preferred wellness model
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        
        payload = {
            "inputs": f"Wellness and health guidance: {message}",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.5,  # Balanced temperature for empathetic responses
                "return_full_text": False
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "No response generated.")
            elif isinstance(result, dict):
                return result.get("generated_text", result.get("response", "No response generated."))
            else:
                return str(result)
        else:
            return f"API Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def simulate_wellness_response(message):
    """
    Simulate Wellness Guide responses for demo purposes
    Remove this function when you implement the actual API call
    """
    wellness_responses = [
        f"Thank you for sharing your wellness concern about '{message}'. Let me provide some guidance to help you on your wellness journey...",
        f"I understand you're asking about '{message}'. Here are some holistic approaches to support your wellbeing...",
        f"Regarding '{message}', wellness is a personal journey. Let me share some insights that might help...",
        f"Your question about '{message}' is important for your wellness. Here's what I recommend for a balanced approach...",
        f"I appreciate you reaching out about '{message}'. Let's explore some healthy strategies together...",
        f"Wellness involves mind, body, and spirit. For your concern about '{message}', here's some guidance...",
    ]
    import random
    return random.choice(wellness_responses)

# Main UI
st.markdown('<h1 class="main-title">🌿 Wellness Guide Assistant</h1>', unsafe_allow_html=True)

# Sidebar for API configuration
with st.sidebar:
    st.markdown("### 🔧 Configuration")
    api_key = st.text_input(
        "Hugging Face API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your Hugging Face API key"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key configured")
    
    st.markdown("### 📊 Chat Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### 🌿 About Your Wellness Guide")
    st.markdown("""
    **Your Personal Wellness Assistant**
    
    I'm here to support your wellness journey:
    - 🧘‍♀️ **Mental Health**: Stress management and mindfulness
    - 💪 **Physical Wellness**: Exercise and movement guidance  
    - 🥗 **Nutrition**: Healthy eating habits and tips
    - 😴 **Sleep Health**: Better rest and recovery
    - 🌱 **Holistic Approach**: Mind-body-spirit balance
    - 💖 **Self-Care**: Daily wellness practices
    
    *Remember: This is for guidance only, not medical advice.*
    """)

# Main chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">👤 {message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-message">🤖 {message["content"]}</div>',
                unsafe_allow_html=True
            )

# Chat input
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Type your message here...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle message sending
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Show typing indicator
    with st.spinner("🤖 AI is thinking..."):
        # Call your AI model here
        if st.session_state.api_key:
            # Replace with actual API call
            ai_response = call_huggingface_api(user_input, st.session_state.api_key)
        else:
            # Use simulation for demo
            ai_response = simulate_wellness_response(user_input)
            st.warning("⚠️ Using simulated response. Please add your API key in the sidebar for real Wellness Guide responses.")
    
    # Add AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Clear input and rerun
    st.rerun()

# Welcome message for new users
if not st.session_state.messages:
    st.markdown("""
    <div class="chat-container">
        <h3>🌿 Welcome to Your Personal Wellness Guide!</h3>
        <p>I'm here to support you on your wellness journey. I can help you with various aspects of health and wellbeing:</p>
        <ul>
            <li><strong>🧘‍♀️ Mental Health</strong> - Stress management, anxiety relief, mindfulness practices</li>
            <li><strong>💪 Physical Wellness</strong> - Exercise routines, movement, fitness guidance</li>
            <li><strong>🥗 Nutrition</strong> - Healthy eating habits, meal planning, dietary advice</li>
            <li><strong>😴 Sleep Health</strong> - Better sleep hygiene, rest and recovery tips</li>
            <li><strong>🌱 Holistic Health</strong> - Mind-body-spirit balance and integration</li>
            <li><strong>💖 Self-Care</strong> - Daily wellness practices and routines</li>
        </ul>
        <p><strong>Try asking me about:</strong></p>
        <ul>
            <li>"How can I manage stress better?"</li>
            <li>"What are some healthy breakfast ideas?"</li>
            <li>"I'm having trouble sleeping, any tips?"</li>
            <li>"How do I start a meditation practice?"</li>
            <li>"What exercises are good for beginners?"</li>
        </ul>
        <p>Remember: I provide general wellness guidance. For serious health concerns, please consult with healthcare professionals. 💙</p>
    </div>
    """, unsafe_allow_html=True) or tasks you might have. Here are some things you can try:</p>
        <ul>
            <li>Ask me questions about any topic</li>
            <li>Request help with coding problems</li>
            <li>Get creative writing assistance</li>
            <li>Brainstorm ideas for projects</li>
        </ul>
        <p>Simply type your message in the input box below and click Send to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Powered by Hugging Face 🤗 | Built with Streamlit ⚡</p>",
    unsafe_allow_html=True
)