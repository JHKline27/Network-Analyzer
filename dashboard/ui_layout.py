import streamlit as st
from analyzer.visualize import (
    plot_protocol_distribution,
    plot_packet_size_distribution,
    plot_packet_frequency_over_time,
    plot_top_ip_addresses
)


def setup_ui():
    # Set the tab name and any global UI configuration
    st.set_page_config(page_title="Network Traffic Analyzer")
'''
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
        analytics_buttons = {
            "Show Protocol Distribution": plot_protocol_distribution,
            "Show Packet Size Distribution": plot_packet_size_distribution,
            "Show Packet Frequency Over Time": plot_packet_frequency_over_time,
            "Show Top IP Addresses": plot_top_ip_addresses,
        }

        for label, func in analytics_buttons.items():
            if st.button(label):
                func()

    return selected_interface, start_button, stop_button'''