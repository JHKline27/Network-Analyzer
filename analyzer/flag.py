import pandas as pd
import time

def flag_suspicious_packets(df, index, ip_counts):
    flagged = False

    # Get the precise timestamp for the current packet
    current_timestamp = df['Precise Timestamp'].iloc[index]  # This should be a Timestamp object
    source_ip = df['Source IP'].iloc[index]
    # Check for large packet size
    if flag_large_size(df, index):
        flagged = True

    # Check for burst packets using the current timestamp
    if flag_burst_packets(source_ip, index, ip_counts, current_timestamp):
        flagged = True

    return flagged

def flag_large_size(df, index):
    HIGH_PACKET_SIZE = 15000  # Example threshold for high packet size
    return df['Packet Size'].iloc[index] > HIGH_PACKET_SIZE  # Return True if it exceeds


recent_packets = {}

def flag_burst_packets(source_ip, index, ip_counts, current_timestamp, threshold=10, time_frame=.1):
    """
    Check if a burst of packets is coming from the same IP address in a short time.
    """
    if source_ip not in recent_packets:
        # Initialize with first occurrence
        recent_packets[source_ip] = {'count': 1, 'timestamps': [current_timestamp]}
    else:
        # Update count and add new timestamp
        data = recent_packets[source_ip]
        data['count'] += 1
        data['timestamps'].append(current_timestamp)
        
        # Calculate the total time between first and last packet
        total_time = sum(abs(data['timestamps'][i] - data['timestamps'][i - 1]) for i in range(1, len(data['timestamps'])))
        
        # Check the burst condition: count exceeds threshold and total time is within the time frame
        if data['count'] >= threshold and total_time <= time_frame:
            return True  # Flag this packet sequence
        elif total_time > time_frame:
            # Reset if the time frame has been exceeded
            recent_packets[source_ip] = {'count': 1, 'timestamps': [current_timestamp]}

    return False  # No flag
