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

# Function to handle the packet capturing in a separate thread
def capture_packets(interface):
    stop_event.clear()  # Reset the stop event before starting a new capture session
    clear_csv_file()  # Clear CSV at the start of a new capture session
    capture(interface=interface, stopper=stop_event, callback=packet_summary)  # Capture packets

# Streamlit App
def main():

    if "capturing" not in st.session_state:
        st.session_state.capturing = False


    selected_interface, start_capture, stop_capture = setup_ui() 

   

    # Start/Stop Capture Button
    if start_capture and not st.session_state.capturing:
        st.session_state.capturing = True
        st.sidebar.success(f"Started capturing on interface: {selected_interface}")
        threading.Thread(target=capture_packets, args=(selected_interface,), daemon=True).start()

    if stop_capture and st.session_state.capturing:
        stop_event.set()  # Correctly call the set method
        st.session_state.capturing = False
        st.sidebar.success("Stopped capturing packets.")

    csv_file_path = 'data/captured_packets.csv'
    captured_packets_placeholder = st.empty()

    while st.session_state.capturing:
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            try:
                df = pd.read_csv(csv_file_path)
                if not df.empty:  # Check if the dataframe is not empty
                    # Reverse the order to show the most recent packets at the top
                    captured_packets_placeholder.dataframe(df.iloc[::-1], height=600, use_container_width=True)  # Update display
                else:
                    captured_packets_placeholder.write("No data in CSV file.")
            except pd.errors.EmptyDataError:
                captured_packets_placeholder.write("CSV file is empty or corrupt. No columns to parse.")
        else:
            captured_packets_placeholder.write("No packets captured yet or file is empty.")

        # Sleep to avoid constant reruns (adjust time interval for smoother updates)
        time.sleep(1)  # Adjust the refresh interval

    # Once capturing is stopped, show final captured data without loop
    if not st.session_state.capturing:
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            df = pd.read_csv(csv_file_path)
            if not df.empty:
                captured_packets_placeholder.dataframe(df.iloc[::-1], height=600, use_container_width=True)
            else:
                captured_packets_placeholder.write("No data in CSV file.")
        else:
            captured_packets_placeholder.write("No packets captured yet or file is empty.")


    selected_option = st.session_state.get('selected_analytics', None)
    
    if selected_option:
        with st.expander("Analytics", expanded=False):
            if selected_option == "Protocol Distribution":
                plot_protocol_distribution()
            elif selected_option == "Packet Size Distribution":
                plot_packet_size_distribution()
            elif selected_option == "Packet Frequency Over Time":
                plot_packet_frequency_over_time()
            elif selected_option == "Top IP Addresses":
                plot_top_ip_addresses()

if __name__ == "__main__":
    main()
