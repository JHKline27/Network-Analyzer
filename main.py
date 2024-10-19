import streamlit as st
from analyzer.capture import capture, clear_csv_file, packet_summary, stop_event 
from analyzer.store import save_to_csv
from scapy.all import get_if_list
import threading
import os
import pandas as pd
import time
from dashboard.ui_layout import setup_ui
from analyzer.visualize import (
    plot_protocol_distribution,
    plot_packet_size_distribution,
    plot_packet_frequency_over_time,
    plot_top_ip_addresses
)
from analyzer.filter import apply_filters

def capture_packets(interface):
    stop_event.clear()
    clear_csv_file()
    capture(interface=interface, stopper=stop_event, callback=packet_summary)

def display_analytics():
    # Create tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs(["Protocol Distribution", "Packet Size Distribution", "Packet Frequency Over Time", "Top IP Addresses"])

    with tab1:
        st.header("Protocol Distribution")
        plot_protocol_distribution()

    with tab2:
        st.header("Packet Size Distribution")
        plot_packet_size_distribution()

    with tab3:
        st.header("Packet Frequency Over Time")
        plot_packet_frequency_over_time()

    with tab4:
        st.header("Top IP Addresses")
        plot_top_ip_addresses()

def main():
    if "capturing" not in st.session_state:
        st.session_state.capturing = False
    if "show_analytics" not in st.session_state:
        st.session_state.show_analytics = False

    selected_interface, start_capture, stop_capture, filter_params = setup_ui()

    if start_capture and not st.session_state.capturing:
        st.session_state.capturing = True
        st.sidebar.success(f"Started capturing on interface: {selected_interface}")
        threading.Thread(target=capture_packets, args=(selected_interface,), daemon=True).start()

    if stop_capture and st.session_state.capturing:
        stop_event.set()
        st.session_state.capturing = False
        st.sidebar.success("Stopped capturing packets.")

    csv_file_path = 'data/captured_packets.csv'
    captured_packets_placeholder = st.empty()

    while st.session_state.capturing:
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            try:
                df = pd.read_csv(csv_file_path)
                captured_packets_placeholder.dataframe(df.iloc[::-1], height=600, use_container_width=True)
            except pd.errors.EmptyDataError:
                captured_packets_placeholder.write("CSV file is empty or corrupt. No columns to parse.")
        else:
            captured_packets_placeholder.write("No packets captured yet or file is empty.")
        time.sleep(1)

    if not st.session_state.capturing:
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            df = pd.read_csv(csv_file_path)
            captured_packets_placeholder.dataframe(df.iloc[::-1], height=600, use_container_width=True)

    # Apply Filters
    if st.button("Apply Filters"):
        if filter_params:  # Check if filtering options were set
            filtered_df = apply_filters(df, filter_params)
            captured_packets_placeholder.dataframe(filtered_df)  # Show filtered packets

    # Add a button to toggle analytics visibility
    if st.button("Show/Hide Analytics"):
        st.session_state.show_analytics = not st.session_state.show_analytics

    # Show analytics based on the toggle
    if st.session_state.show_analytics:
        display_analytics()

if __name__ == "__main__":
    main()
