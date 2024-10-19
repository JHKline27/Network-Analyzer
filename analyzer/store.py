import csv
import os

def save_to_csv(data, filename='data/captured_packets.csv'):
    """Save processed packet data to a specified CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Check if the first line (header) is missing and write it if necessary
        if file_exists:
            with open(filename, 'r') as f:
                first_line = f.readline().strip()
                if not first_line:  # If the first line is empty, write the headers
                    writer.writerow([
        'Source IP', 'Destination IP', 'Protocol', 'Timestamp', 'Delta Time',
        'TTL', 'IP Header Length', 'Total Length', 'Source Port', 'Destination Port', 'Packet Size'
    ])
        else:
            # If the file doesn't exist, write headers
            writer.writerow([
        'Source IP', 'Destination IP', 'Protocol', 'Timestamp', 'Delta Time',
        'TTL', 'IP Header Length', 'Total Length', 'Source Port', 'Destination Port', 'Packet Size'
    ])

        # Write the data row
        writer.writerow([
            data.get('Source IP'),
            data.get('Destination IP'),
            data.get('Protocol'),
            data.get('Timestamp'),
            data.get('Delta Time'),
            data.get('TTL'),
            data.get('IP Header Length'),
            data.get('Total Length'),
            data.get('Source Port'),
            data.get('Destination Port'),
            data.get('Packet Size')
        ])