import streamlit as st
import hashlib
import os
import json
from pathlib import Path
import uuid
import time
from datetime import datetime, timedelta

# Define the path for storing user credentials
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
# Define the path for storing password reset tokens
TOKENS_PATH = Path(__file__).parent / "reset_tokens.json"

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
    
    # Create tabs for login, registration, and password reset
    login_tab, register_tab, reset_tab = st.tabs(["Login", "Register", "Reset Password"])
    
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
    
    with login_tab:
        # Login container with modern styling
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Login form
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
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
        
    with register_tab:
        # Registration container with modern styling
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Registration form
        new_username = st.text_input("Choose a Username", key="register_username")
        new_password = st.text_input("Choose a Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        # Password strength indicator
        if new_password:
            strength = 0
            feedback = []
            
            if len(new_password) >= 8:
                strength += 1
            else:
                feedback.append("Password should be at least 8 characters long")
                
            if any(c.isdigit() for c in new_password):
                strength += 1
            else:
                feedback.append("Password should contain at least one number")
                
            if any(c.isupper() for c in new_password):
                strength += 1
            else:
                feedback.append("Password should contain at least one uppercase letter")
                
            if any(not c.isalnum() for c in new_password):
                strength += 1
            else:
                feedback.append("Password should contain at least one special character")
            
            # Display strength meter
            st.progress(strength / 4)
            st.caption(f"Password strength: {['Weak', 'Fair', 'Good', 'Strong'][min(strength, 3)]}")
            
            if feedback and strength < 3:
                st.warning("\n".join(feedback))
        
        # Registration button
        if st.button("Register", key="register_button"):
            if not new_username:
                st.error("Username cannot be empty")
            elif not new_password:
                st.error("Password cannot be empty")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long")
            else:
                if register_user(new_username, new_password, role="user"):
                    st.success("Registration successful! You can now login.")
                else:
                    st.error("Username already exists")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with reset_tab:
        # Password reset container with modern styling
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Create tabs for requesting token and resetting password
        request_tab, reset_password_tab = st.tabs(["Request Reset Token", "Reset Password"])
        
        with request_tab:
            # Form to request password reset token
            reset_username = st.text_input("Username", key="reset_username")
            
            if st.button("Request Reset Token", key="request_token_button"):
                if not reset_username:
                    st.error("Username cannot be empty")
                else:
                    token = generate_reset_token(reset_username)
                    if token:
                        st.success(f"Reset token generated. Please use this token to reset your password: {token}")
                        st.info("This token will expire in 24 hours.")
                    else:
                        st.error("Username not found")
        
        with reset_password_tab:
            # Form to reset password using token
            reset_token = st.text_input("Reset Token", key="reset_token")
            new_password = st.text_input("New Password", type="password", key="new_password")
            confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")
            
            if st.button("Reset Password", key="reset_password_button"):
                if not reset_token:
                    st.error("Reset token cannot be empty")
                elif not new_password:
                    st.error("New password cannot be empty")
                elif new_password != confirm_new_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters long")
                else:
                    if reset_password(reset_token, new_password):
                        st.success("Password reset successful! You can now login with your new password.")
                    else:
                        st.error("Invalid or expired reset token")
        
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

def generate_reset_token(username):
    """Generate a password reset token for a user."""
    if not CREDENTIALS_PATH.exists():
        initialize_credentials()
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    
    # Check if username exists
    if username not in credentials:
        return None
    
    # Generate token
    token = str(uuid.uuid4())
    expiry = (datetime.now() + timedelta(hours=24)).timestamp()
    
    # Initialize tokens file if it doesn't exist
    if not TOKENS_PATH.exists():
        with open(TOKENS_PATH, 'w') as f:
            json.dump({}, f)
    
    # Load existing tokens
    with open(TOKENS_PATH, 'r') as f:
        tokens = json.load(f)
    
    # Add new token
    tokens[token] = {
        "username": username,
        "expiry": expiry
    }
    
    # Save tokens
    with open(TOKENS_PATH, 'w') as f:
        json.dump(tokens, f)
    
    return token

def validate_reset_token(token):
    """Validate a password reset token."""
    if not TOKENS_PATH.exists():
        return None
    
    # Load tokens
    with open(TOKENS_PATH, 'r') as f:
        tokens = json.load(f)
    
    # Check if token exists
    if token not in tokens:
        return None
    
    # Check if token has expired
    if tokens[token]["expiry"] < time.time():
        # Remove expired token
        del tokens[token]
        with open(TOKENS_PATH, 'w') as f:
            json.dump(tokens, f)
        return None
    
    return tokens[token]["username"]

def reset_password(token, new_password):
    """Reset a user's password using a token."""
    username = validate_reset_token(token)
    if not username:
        return False
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    
    # Update password
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    credentials[username]["password"] = hashed_password
    
    # Save credentials
    with open(CREDENTIALS_PATH, 'w') as f:
        json.dump(credentials, f)
    
    # Remove used token
    with open(TOKENS_PATH, 'r') as f:
        tokens = json.load(f)
    
    del tokens[token]
    
    with open(TOKENS_PATH, 'w') as f:
        json.dump(tokens, f)
    
    return True

def get_user_role(username):
    """Get the role of a user."""
    if not CREDENTIALS_PATH.exists():
        initialize_credentials()
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
    
    # Check if username exists
    if username not in credentials:
        return None
    
    return credentials[username]["role"]

def is_admin():
    """Check if the current user is an admin."""
    if not is_authenticated():
        return False
    
    username = st.session_state.username
    return get_user_role(username) == "admin"
