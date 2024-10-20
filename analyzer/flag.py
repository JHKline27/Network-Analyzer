def flag_suspicious_packets(df, index, ip_counts):
    flagged = False

    current_timestamp = df['Precise Timestamp'].iloc[index] 
    source_ip = df['Source IP'].iloc[index]
    if flag_large_size(df, index):
        flagged = True

    if flag_burst_packets(source_ip, index, ip_counts, current_timestamp):
        flagged = True

    return flagged

def flag_large_size(df, index):
    #HIGH_PACKET_SIZE can be adjusted for different flagging logic
    HIGH_PACKET_SIZE = 15000 
    return df['Packet Size'].iloc[index] > HIGH_PACKET_SIZE 


recent_packets = {}
#threshold and time_frame parameters can be changed to adjust burst flagging
def flag_burst_packets(source_ip, index, ip_counts, current_timestamp, threshold=10, time_frame=.1):
    """
    Check if a burst of packets is coming from the same IP address in a short time.
    """
    if source_ip not in recent_packets:
        
        recent_packets[source_ip] = {'count': 1, 'timestamps': [current_timestamp]}
    else:
        
        data = recent_packets[source_ip]
        data['count'] += 1
        data['timestamps'].append(current_timestamp)
        
        
        total_time = sum(abs(data['timestamps'][i] - data['timestamps'][i - 1]) for i in range(1, len(data['timestamps'])))
        
       
        if data['count'] >= threshold and total_time <= time_frame:
            return True  
        elif total_time > time_frame:
            
            recent_packets[source_ip] = {'count': 1, 'timestamps': [current_timestamp]}

    return False 
