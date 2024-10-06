import streamlit as st
from scapy.all import get_if_list


def setup_ui():
    # Set the tab name and any global UI configuration
    st.set_page_config(page_title="Network Traffic Analyzer",layout="wide")
    
    # Configure the layout structure here, such as sidebars, containers, etc.
    with st.sidebar:
        st.title("Controls")
        interfaces = get_if_list()  # Import this from main or pass as parameter
        selected_interface = st.selectbox("Select a network interface:", interfaces)

        # Start/Stop Capture Buttons
        start_button = st.button("Start Capture")
        stop_button = st.button("Stop Capture")

        # Analytics Section
        st.subheader("Analytics")
        analytics_options = st.selectbox("Select Analytics:", [
        "Protocol Distribution",
        "Packet Size Distribution",
        "Packet Frequency Over Time",
        "Top IP Addresses",   
    ])
    
    st.session_state.selected_analytics = analytics_options
    


    return selected_interface, start_button, stop_button