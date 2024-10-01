#use pandas and matplotlib to visualize the data and trends found
import pandas as pd
import matplotlib.pyplot as plt

def plot_protocol_distribution(filename='data/captured_packets.csv'):
    """Visualize the distribution of network protocols (TCP, UDP, etc.)."""
    df = pd.read_csv(filename)
    protocol_counts = df['protocol'].value_counts()

    protocol_counts.plot(kind='bar', color='skyblue')
    plt.title('Protocol Distribution')
    plt.xlabel('Protocol')
    plt.ylabel('Packet Count')
    plt.show()

def plot_packet_size_distribution(filename='data/captured_packets.csv'):
    """Visualize the distribution of packet sizes."""
    df = pd.read_csv(filename)
    
    # Plot a histogram of packet sizes
    df['packet_size'].plot(kind='hist', bins=20, color='purple', alpha=0.7)
    plt.title('Packet Size Distribution')
    plt.xlabel('Packet Size (Bytes)')
    plt.ylabel('Frequency')
    plt.show()

def plot_packet_frequency_over_time(filename='data/captured_packets.csv'):
    """Visualize the number of packets captured over time."""
    df = pd.read_csv(filename)

    # Convert the timestamp column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by minute or second for packet frequency analysis
    packet_frequency = df.groupby(pd.Grouper(key='timestamp', freq='1Min')).size()

    packet_frequency.plot(kind='line', color='green')
    plt.title('Packet Frequency Over Time')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Number of Packets')
    plt.show()

def plot_top_ip_addresses(filename='data/captured_packets.csv', top_n=10):
    """Visualize the top N source IP addresses."""
    df = pd.read_csv(filename)

    # Count occurrences of source IP addresses
    src_ip_counts = df['src_ip'].value_counts().head(top_n)

    src_ip_counts.plot(kind='bar', color='orange')
    plt.title(f'Top {top_n} Source IP Addresses')
    plt.xlabel('Source IP')
    plt.ylabel('Packet Count')
    plt.show()

if __name__ == "__main__":
    # Call each function to visualize
    plot_protocol_distribution()
    plot_packet_size_distribution()
    plot_packet_frequency_over_time()
    plot_top_ip_addresses()
