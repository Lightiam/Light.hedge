import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.main import run_hedge_fund, create_workflow
from src.utils.analysts import ANALYST_ORDER
from src.llm.models import LLM_ORDER, get_model_info
from src.web.auth import login_page, is_authenticated, logout

# Set page configuration
st.set_page_config(
    page_title="LightHedge AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a more appealing UI
st.markdown("""
<style>
/* Global Styles */
.main {
    background-color: #f8fafc;
    padding: 1rem;
}
.stApp {
    max-width: 1200px;
    margin: 0 auto;
}

/* Header Styles */
h1, h2, h3 {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1e293b;
}
h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
}
h3 {
    font-size: 1.25rem !important;
    font-weight: 500 !important;
    color: #475569 !important;
    margin-top: 0 !important;
}

/* Sidebar Styles */
.css-1d391kg, .css-163ttbj, .css-1wrcr25 {
    background-color: #f1f5f9 !important;
    border-right: 1px solid #e2e8f0;
}
.sidebar .stButton button {
    width: 100%;
}

/* Tab Styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #f1f5f9;
    border-radius: 8px 8px 0px 0px;
    gap: 1px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background-color: #3b82f6;
    color: white;
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

/* Button Styles */
.stButton button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
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

/* Chat Interface Styles */
.chat-message {
    padding: 1.5rem;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    max-width: 85%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.chat-message.user {
    background-color: #3b82f6;
    color: #ffffff;
    border-radius: 0.75rem 0.75rem 0 0.75rem;
    align-self: flex-end;
    margin-left: auto;
}
.chat-message.bot {
    background-color: #1e293b;
    color: #ffffff;
    border-radius: 0.75rem 0.75rem 0.75rem 0;
    align-self: flex-start;
    margin-right: auto;
}
.chat-message .message-content {
    display: flex;
    margin-top: 0.5rem;
}
.avatar {
    width: 15%;
}
.avatar img {
    max-width: 48px;
    max-height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid white;
}
.message {
    width: 85%;
    padding: 0 1rem;
    line-height: 1.5;
}

/* Signal and Metric Styles */
.signal-bullish {
    color: #22c55e;
    font-weight: bold;
}
.signal-bearish {
    color: #ef4444;
    font-weight: bold;
}
.signal-neutral {
    color: #f59e0b;
    font-weight: bold;
}
.metric-card {
    background-color: white;
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    border: 1px solid #e2e8f0;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.metric-value {
    font-size: 2.25rem;
    font-weight: 700;
    color: #1e293b;
}
.metric-label {
    font-size: 1rem;
    color: #64748b;
    margin-top: 0.5rem;
}

/* Input Field Styles */
.stTextInput input, .stSelectbox, .stDateInput input {
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    padding: 0.75rem;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}
.stTextInput input:focus, .stSelectbox:focus, .stDateInput input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

/* Expander Styles */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #1e293b;
    background-color: #f8fafc;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    border: 1px solid #e2e8f0;
}
.streamlit-expanderContent {
    border: 1px solid #e2e8f0;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {
        "cash": 100000.0,
        "margin_requirement": 0.0,
        "positions": {},
        "realized_gains": {}
    }

# Check if user is authenticated
if not is_authenticated():
    login_page()
else:
    # Header
    st.title("🚀 LightHedge AI")
    st.markdown("### An AI-powered hedge fund team making intelligent trading decisions")

    # Sidebar for configuration
    with st.sidebar:
        # Add logout button at the top of the sidebar
        if st.button("Logout", key="logout_button"):
            logout()
            st.rerun()
        
        # Display user information
        username = st.session_state.username
        
        # User info container with styling
        st.markdown("""
        <div style="background-color: #f1f5f9; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;">
            <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">LOGGED IN AS</div>
            <div style="font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">{}</div>
        </div>
        """.format(username), unsafe_allow_html=True)
            
        st.header("Configuration")
    
    # Ticker input
    ticker_input = st.text_input("Enter stock tickers (comma-separated)", "AAPL,MSFT,NVDA")
    tickers = [ticker.strip() for ticker in ticker_input.split(",")]
    
    # Update portfolio positions if tickers change
    for ticker in tickers:
        if ticker not in st.session_state.portfolio["positions"]:
            st.session_state.portfolio["positions"][ticker] = {
                "long": 0,
                "short": 0,
                "long_cost_basis": 0.0,
                "short_cost_basis": 0.0,
            }
        if ticker not in st.session_state.portfolio["realized_gains"]:
            st.session_state.portfolio["realized_gains"][ticker] = {
                "long": 0.0,
                "short": 0.0,
            }
    
    # Date range selection
    st.subheader("Date Range")
    end_date = st.date_input("End Date", datetime.now())
    start_date = st.date_input("Start Date", end_date - relativedelta(months=3))
    
    # Analyst selection
    st.subheader("AI Analysts")
    selected_analysts = []
    for display, value in ANALYST_ORDER:
        if st.checkbox(display, value=True):
            selected_analysts.append(value)
    
    # LLM model selection
    st.subheader("LLM Model")
    model_options = [display for display, value, _ in LLM_ORDER]
    model_values = [value for _, value, _ in LLM_ORDER]
    selected_model_index = st.selectbox("Select LLM Model", range(len(model_options)), format_func=lambda i: model_options[i])
    selected_model = model_values[selected_model_index]
    
    # Get model info
    model_info = get_model_info(selected_model)
    if model_info:
        model_provider = model_info.provider.value
    else:
        model_provider = "Unknown"
    
    # Show reasoning option
    show_reasoning = st.checkbox("Show Reasoning", value=True)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Chat", "📈 Backtesting"])

with tab1:
    st.header("Trading Dashboard")
    
    # Run analysis button
    if st.button("Run Analysis", key="run_analysis"):
        with st.spinner("Running hedge fund analysis..."):
            # Create the workflow with selected analysts
            workflow = create_workflow(selected_analysts)
            
            # Run the hedge fund
            result = run_hedge_fund(
                tickers=tickers,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                portfolio=st.session_state.portfolio,
                show_reasoning=show_reasoning,
                selected_analysts=selected_analysts,
                model_name=selected_model,
                model_provider=model_provider,
            )
                
            # Store the result in session state
            st.session_state.last_result = result
            
            # Add to chat history
            system_message = f"Analysis completed for {', '.join(tickers)} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            st.session_state.chat_history.append({"role": "system", "content": system_message})
    
    # Display results if available
    if 'last_result' in st.session_state:
        result = st.session_state.last_result
        decisions = result.get("decisions", {})
        
        # Portfolio summary metrics
        st.subheader("Portfolio Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$100,000</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Portfolio Value</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$95,000</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Cash Balance</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$5,000</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Position Value</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">+2.5%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Return</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Trading decisions
        st.subheader("Trading Decisions")
        for ticker, decision in decisions.items():
            with st.expander(f"{ticker} - {decision.get('action', '').upper()}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Action and confidence
                    action = decision.get("action", "").upper()
                    confidence = decision.get("confidence", 0)
                    
                    action_color = {
                        "BUY": "green",
                        "SELL": "red",
                        "HOLD": "orange",
                    }.get(action, "gray")
                    
                    st.markdown(f"<h3 style='color: {action_color};'>{action}</h3>", unsafe_allow_html=True)
                    st.markdown(f"**Quantity:** {decision.get('quantity', 0)}")
                    st.markdown(f"**Confidence:** {confidence:.1f}%")
                    
                    # Create a gauge chart for confidence
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Confidence"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': action_color},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgray"},
                                {'range': [30, 70], 'color': "gray"},
                                {'range': [70, 100], 'color': "darkgray"}
                            ],
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Analyst signals
                    signals_data = []
                    for agent, signals in result.get("analyst_signals", {}).items():
                        if ticker not in signals:
                            continue
                        
                        signal = signals[ticker]
                        agent_name = agent.replace("_agent", "").replace("_", " ").title()
                        signal_type = signal.get("signal", "").upper()
                        confidence = signal.get("confidence", 0)
                        
                        signals_data.append({
                            "Analyst": agent_name,
                            "Signal": signal_type,
                            "Confidence": confidence
                        })
                    
                    if signals_data:
                        df = pd.DataFrame(signals_data)
                        
                        # Create a horizontal bar chart for analyst signals
                        fig = px.bar(
                            df,
                            y="Analyst",
                            x="Confidence",
                            color="Signal",
                            color_discrete_map={
                                "BULLISH": "green",
                                "BEARISH": "red",
                                "NEUTRAL": "orange"
                            },
                            orientation='h',
                            title="Analyst Signals",
                            labels={"Confidence": "Confidence (%)", "Analyst": ""},
                        )
                        fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Reasoning
                    st.subheader("Reasoning")
                    st.markdown(f"{decision.get('reasoning', 'No reasoning provided.')}")

with tab2:
    st.header("Chat with LightHedge AI")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user"><div class="message-content"><div class="message">{message["content"]}</div></div></div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="chat-message bot"><div class="message-content"><div class="message">{message["content"]}</div></div></div>', unsafe_allow_html=True)
        elif message["role"] == "system":
            st.markdown(f'<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 10px;">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask LightHedge AI about your portfolio or trading strategies...", key="user_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Process the user input (in a real app, this would call an AI model)
        if "portfolio" in user_input.lower() or "holdings" in user_input.lower():
            response = "Your current portfolio consists of:"
            for ticker, position in st.session_state.portfolio["positions"].items():
                if position["long"] > 0 or position["short"] > 0:
                    response += f"\n- {ticker}: {position['long']} shares long, {position['short']} shares short"
            response += f"\nCash balance: ${st.session_state.portfolio['cash']:,.2f}"
        elif "analyze" in user_input.lower() or "stock" in user_input.lower():
            response = "To analyze stocks, please go to the Dashboard tab and click 'Run Analysis' after selecting your desired tickers and configuration."
        else:
            response = "I'm your AI hedge fund assistant. I can help you analyze stocks, manage your portfolio, and make trading decisions. Try asking about your portfolio or specific stocks."
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to update the chat display
        st.rerun()

with tab3:
    st.header("Backtesting")
    
    st.markdown("Backtesting functionality will be implemented in a future update.")
    
    # Placeholder for backtesting UI
    st.info("Coming soon: Backtest your trading strategies against historical data.")
    
    # Advanced configuration options
    with st.expander("Advanced Configuration"):
        st.slider("Simulation Period (Days)", 30, 365, 180)
        st.number_input("Initial Capital", min_value=10000, max_value=10000000, value=100000, step=10000)
        st.selectbox("Risk Model", ["Conservative", "Moderate", "Aggressive"])
        st.checkbox("Enable Monte Carlo Simulation")
    
# End of authenticated content block
