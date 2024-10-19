from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, DNS, Raw
from analyzer.store import save_to_csv
import time
import threading
import csv

last_packet_time = None
stop_event = threading.Event()  # Event to signal when to stop capturing

def capture(interface, stopper, callback=None):
    clear_csv_file()
    print(f"Stop event cleared: {not stop_event.is_set()}")
    try:
        print("Starting packet capture...")
        # Use the stop_filter to check for the stop event
        sniff(iface=interface, prn=callback, stop_filter=lambda x: stopper.is_set())
    except Exception as e:
        print(f"Error capturing on interface {interface}: {e}")

def clear_csv_file(filename='data/captured_packets.csv'):
    """Clear CSV data but retain the header."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
        'Source IP', 'Destination IP', 'Protocol', 'Timestamp', 'Delta Time',
        'TTL', 'IP Header Length', 'Total Length', 'Source Port', 'Destination Port', 'Packet Size'
    ])  # Write the header row at the start of the file



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
        protocol = None
        src_port = None
        dst_port = None

        # Determine the protocol and extract additional information
        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            if dst_port == 443 or src_port == 443:  # Port 443 is typically used for HTTPS
                protocol = 'HTTPS'
            else:
                protocol = 'TCP'
        elif UDP in packet:
            protocol = 'UDP'
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif ICMP in packet:
            protocol = 'ICMP'
        elif DNS in packet:
            protocol = 'DNS'
            query = packet[DNS].qd.qname if packet[DNS].qd else None
            return {
                'Source IP': packet[IP].src,
                'Destination IP': packet[IP].dst,
                'Protocol': protocol,
                'Timestamp': formatted_time,
                'Delta Time': round(delta_time, 6),
                'TTL': packet[IP].ttl,
                'Packet Size': len(packet)
            }
        elif Raw in packet:
            protocol = 'Raw'
        else:
            protocol = 'Other'

        # Return the processed packet data
        return {
            'Source IP': packet[IP].src,
            'Destination IP': packet[IP].dst,
            'Protocol': protocol,
            'Timestamp': formatted_time,
            'Delta Time': round(delta_time, 6),
            'TTL': packet[IP].ttl,
            'IP Header Length': packet[IP].ihl * 4,
            'Total Length': packet[IP].len,
            'Source Port': src_port,
            'Destination Port': dst_port,
            'Packet Size': len(packet)
        }

    elif ARP in packet:
        return {
            'Source IP': packet[ARP].psrc,
            'Destination IP': packet[ARP].pdst,
            'Protocol': 'ARP',
            'Timestamp': formatted_time,
            'Delta Time': round(delta_time, 6),
            'Packet Size': len(packet)
        }

    return None
