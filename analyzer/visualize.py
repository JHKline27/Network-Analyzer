#use pandas and matplotlib to visualize the data and trends found
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_protocol_distribution():
    csv_file_path = 'data/captured_packets.csv'

    if not st.session_state.capturing and csv_file_path and os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        
        if not df.empty:
            protocol_counts = df['protocol'].value_counts()

            # Create the plot
            fig, ax = plt.subplots()
            protocol_counts.plot(kind='bar', ax=ax)
            ax.set_title('Protocol Distribution')
            ax.set_xlabel('Protocol')
            ax.set_ylabel('Count')

            # Display the plot
            st.pyplot(fig)
        else:
            st.write("No data available to plot.")
    else:
        st.write("Capture has not stopped or file does not exist.")

def plot_packet_size_distribution():
    csv_file_path = 'data/captured_packets.csv'

    if not st.session_state.capturing and csv_file_path and os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)

        if not df.empty:
            fig, ax = plt.subplots()
            df['packet_size'].plot(kind='hist', bins=30, ax=ax)
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
            # Convert the 'timestamp' column to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Calculate the total capture duration
            capture_duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()

            # Determine the grouping frequency based on capture duration
            if capture_duration < 60:
                freq = 'S'  # Seconds if duration is less than a minute
                xlabel = 'Time (Seconds)'
            elif capture_duration < 3600:
                freq = 'T'  # Minutes if duration is less than an hour
                xlabel = 'Time (Minutes)'
            elif capture_duration < 216000:
                freq = 'H'  # Hours for longer durations
                xlabel = 'Time (Hours)'

            # Group by the selected frequency and count occurrences (frequency)
            packet_counts = df.groupby(pd.Grouper(key='timestamp', freq=freq)).size()

            # Create the plot
            fig, ax = plt.subplots()
            packet_counts.plot(ax=ax)

            ax.set_title('Packet Frequency Over Time')
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Number of Packets')

            # Display the plot
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
            # Combine source and destination IPs to get overall frequency
            ip_counts = pd.concat([df['src_ip'], df['dst_ip']]).value_counts().head(10)

            # Create the plot
            fig, ax = plt.subplots()
            ip_counts.plot(kind='barh', ax=ax)  # Horizontal bar plot for better readability
            ax.set_title('Top IP Addresses')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('IP Address')

            # Display the plot
            st.pyplot(fig)
        else:
            st.write("No data available to plot.")
    else:
        st.write("Capture has not stopped or file does not exist.")

if __name__ == "__main__":
    # Call each function to visualize
    plot_protocol_distribution()
    plot_packet_size_distribution()
    plot_packet_frequency_over_time()
    plot_top_ip_addresses()
