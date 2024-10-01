from scapy.all import sniff, IP, TCP, UDP
from .store import save_to_csv 
import time

last_packet_time = None

def capture(interface, count=50, callback=None):
    try:
        sniff(iface=interface, prn=callback, count=count)
        
    except Exception as e:
        print(f"Error capturing on interface {interface}: {e}")

def packet_summary(packet):
    global last_packet_time
    data = process_packet(packet)
    if data:
        save_to_csv(data)
    
def process_packet(packet):
    global last_packet_time
    current_time = time.time()
    if last_packet_time:
        delta_time = current_time - last_packet_time
    else:
        delta_time = 0

    last_packet_time = current_time
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
    
    if IP in packet:
        return {
            'src_ip': packet[IP].src,
            'dst_ip': packet[IP].dst,
            'protocol': 'TCP' if TCP in packet else 'UDP' if UDP in packet else 'Other',
            'timestamp': formatted_time,
            'delta_time': round(delta_time, 6),
            'ttl': packet[IP].ttl,
            'ip_header_length': packet[IP].ihl * 4,  # IP header length in bytes
            'total_length': packet[IP].len,  # Total length of IP packet
            'src_port': packet[TCP].sport if TCP in packet else packet[UDP].sport if UDP in packet else None,
            'dst_port': packet[TCP].dport if TCP in packet else packet[UDP].dport if UDP in packet else None,
            'packet_size': len(packet)  # Total size of the packet in bytes
        }
    return None
