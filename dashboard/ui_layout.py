import streamlit as st
from scapy.all import get_if_list

def setup_ui():
    st.set_page_config(page_title="Network Traffic Analyzer", layout="wide")
    
    with st.sidebar:
        st.title("Controls")
        interfaces = get_if_list()
        selected_interface = st.selectbox("Select a network interface:", interfaces)

        start_button = st.button("Start Capture")
        stop_button = st.button("Stop Capture")        

        should_filter = st.radio("Filter", ("Off", "On"))
        if should_filter == "On":
            st.subheader("Filter Options")
            protocol_options = st.multiselect("Select Protocols:", ['TCP', 'UDP', 'ICMP', 'DNS', 'ARP', 'Raw', 'HTTPS', 'HTTP', 'Other'])
            source_ip = st.text_input("Source IP Address:")
            destination_ip = st.text_input("Destination IP Address:")
            source_port = st.number_input("Source Port:", min_value=0, max_value=65535)
            destination_port = st.number_input("Destination Port:", min_value=0, max_value=65535)
            packet_size= st.number_input("Enter Packet Size", min_value=0, value=0)
            size_comparison = st.selectbox("Select Size Comparison", ["Equal To","Greater Than", "Less Than"])

            return selected_interface, start_button, stop_button, {
                'protocol_options': protocol_options,
                'source_ip': source_ip,
                'destination_ip': destination_ip,
                'source_port': source_port,
                'destination_port': destination_port,
                'packet_size': packet_size,
                'size_comparison': size_comparison

            }
         

    return selected_interface, start_button, stop_button, None
