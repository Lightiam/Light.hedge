import streamlit as st
import hashlib
import os
import json
from pathlib import Path

# Define the path for storing user credentials
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"

# Default admin credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "lighthedge2024"

def initialize_credentials():
    """Initialize the credentials file with default admin account if it doesn't exist."""
    if not CREDENTIALS_PATH.exists():
        # Create default admin account
        hashed_password = hashlib.sha256(DEFAULT_PASSWORD.encode()).hexdigest()
        credentials = {
            DEFAULT_USERNAME: {
                "password": hashed_password,
                "role": "admin"
            }
        }
        
        # Save to file
        with open(CREDENTIALS_PATH, 'w') as f:
            json.dump(credentials, f)
        
        return True
    return False

def verify_credentials(username, password):
    """Verify user credentials against stored credentials."""
    if not CREDENTIALS_PATH.exists():
        initialize_credentials()
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    
    # Check if username exists
    if username not in credentials:
        return False
    
    # Verify password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return credentials[username]["password"] == hashed_password

def register_user(username, password, role="user"):
    """Register a new user."""
    if not CREDENTIALS_PATH.exists():
        initialize_credentials()
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    
    # Check if username already exists
    if username in credentials:
        return False
    
    # Add new user
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    credentials[username] = {
        "password": hashed_password,
        "role": role
    }
    
    # Save updated credentials
    with open(CREDENTIALS_PATH, 'w') as f:
        json.dump(credentials, f)
    
    return True

def login_page():
    """Display the login page and handle authentication."""
    # Initialize credentials if needed
    initialize_credentials()
    
    st.markdown('<div class="login-header">', unsafe_allow_html=True)
    st.markdown('<h1>🚀 LightHedge AI</h1>', unsafe_allow_html=True)
    st.markdown('<h3>Sign in to access the AI-powered hedge fund</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom CSS for login page with modern styling
    st.markdown("""
    <style>
    /* Login Container */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2.5rem;
        background-color: white;
        border-radius: 1rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .login-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.15);
    }

    /* Header Styles */
    .login-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .login-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .login-header h3 {
        font-size: 1.25rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Input Fields */
    .stTextInput input {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 2px solid #e2e8f0;
        border-radius: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background-color: #f8fafc;
    }
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        outline: none;
    }
    .stTextInput label {
        font-weight: 500;
        color: #1e293b;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* Button Styles */
    .stButton button {
        width: 100%;
        padding: 0.875rem 1.5rem;
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
    }
    .stButton button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.3);
    }
    .stButton button:active {
        transform: translateY(0);
    }

    /* Info Box */
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid #3b82f6;
        background-color: #f1f5f9;
    }

    /* Footer */
    .login-footer {
        text-align: center;
        margin-top: 2rem;
        font-size: 0.875rem;
        color: #64748b;
    }

    /* Error Message */
    .login-error {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login container with modern styling
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Sign In", key="login_button"):
        if verify_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    # Default credentials info in styled info box
    st.info(f"Default credentials: Username: {DEFAULT_USERNAME}, Password: {DEFAULT_PASSWORD}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with copyright
    st.markdown('<div class="login-footer">© 2024 LightHedge AI. All rights reserved.</div>', unsafe_allow_html=True)
    
    # Add spacing at the bottom
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    return False

def is_authenticated():
    """Check if the user is authenticated."""
    return st.session_state.get("authenticated", False)

def logout():
    """Log out the current user."""
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    if "username" in st.session_state:
        del st.session_state.username
