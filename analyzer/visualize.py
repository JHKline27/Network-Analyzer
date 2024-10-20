import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_protocol_distribution():
    csv_file_path = 'data/captured_packets.csv'
    
    
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        st.write("No data available for plotting.")
        return

   
    df = pd.read_csv(csv_file_path)

    
    if df.empty or 'Protocol' not in df.columns:
        st.write("No protocol data available for plotting.")
        return

   
    protocol_counts = df['Protocol'].value_counts()

    
    if protocol_counts.empty:
        st.write("No protocol data to plot.")
        return

   
    fig, ax = plt.subplots()
    protocol_counts.plot(kind='bar', ax=ax)
    ax.set_title('Protocol Distribution')
    ax.set_xlabel('Protocol')
    ax.set_ylabel('Count')

    
    st.pyplot(fig)

def plot_packet_size_distribution():
    csv_file_path = 'data/captured_packets.csv'

    if not st.session_state.capturing and csv_file_path and os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)

        if not df.empty:
            fig, ax = plt.subplots()
            df['Packet Size'].plot(kind='hist', bins=30, ax=ax)
            ax.set_title('Packet Size Distribution')
            ax.set_xlabel('Packet Size')
            ax.set_ylabel('Frequency')

            st.pyplot(fig)
        else:
            st.write("No data available to plot.")
    else:
        st.write("Capture has not stopped or file does not exist.")

def plot_packet_frequency_over_time():
    csv_file_path = 'data/captured_packets.csv'

    if not st.session_state.capturing and csv_file_path and os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)

        if not df.empty:
            
            
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])  

            capture_duration = (df['Timestamp'].max() - df['Timestamp'].min()).total_seconds()

            if capture_duration < 600:
                freq = 'S'  # Seconds if duration is less than 10 minutes
                xlabel = 'Time (Seconds)'
            elif capture_duration < 36000:
                freq = 'T'  # Minutes if duration is less than 10 hours
                xlabel = 'Time (Minutes)'
            elif capture_duration < 216000:
                freq = 'H'  # Hours for longer durations
                xlabel = 'Time (Hours)'

            
            packet_counts = df.groupby(pd.Grouper(key='Timestamp', freq=freq)).size()

           
            fig, ax = plt.subplots()
            packet_counts.plot(ax=ax)

            ax.set_title('Packet Frequency Over Time')
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Number of Packets')

            
            st.pyplot(fig)
        else:
            st.write("No data available to plot.")
    else:
        st.write("Capture has not stopped or file does not exist.")

def plot_top_ip_addresses():
    csv_file_path = 'data/captured_packets.csv'

    if not st.session_state.capturing and csv_file_path and os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)

        if not df.empty:
            
            print("DataFrame columns:", df.columns) 
            ip_counts = pd.concat([df['Source IP'], df['Destination IP']]).value_counts().head(10)

            
            fig, ax = plt.subplots()
            ip_counts.plot(kind='barh', ax=ax) 
            ax.set_title('Top IP Addresses')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('IP Address')

            
            st.pyplot(fig)
        else:
            st.write("No data available to plot.")
    else:
        st.write("Capture has not stopped or file does not exist.")

if __name__ == "__main__":
    plot_protocol_distribution()
    plot_packet_size_distribution()
    plot_packet_frequency_over_time()
    plot_top_ip_addresses()
