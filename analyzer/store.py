import csv
import os

def save_to_csv(data, filename='data/captured_packets.csv'):
    """Save processed packet data to a specified CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write header if the file is new
        if not file_exists:
            writer.writerow([
                'src_ip', 'dst_ip', 'protocol', 'timestamp', 'delta_time',
                'ttl', 'ip_header_length', 'total_length', 'src_port', 'dst_port', 'packet_size'
            ])

        # Write the data row
        writer.writerow([
            data.get('src_ip'),
            data.get('dst_ip'),
            data.get('protocol'),
            data.get('timestamp'),
            data.get('delta_time'),
            data.get('ttl'),
            data.get('ip_header_length'),
            data.get('total_length'),
            data.get('src_port'),
            data.get('dst_port'),
            data.get('packet_size')
        ])
