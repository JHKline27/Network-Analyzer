Network Traffic Analyzer
Overview
The Network Traffic Analyzer is a Python-based tool designed to capture, analyze, and visualize network traffic in real time. It includes filtering and flagging features to detect suspicious activities, such as bursts of packets from the same source or unusually large packet sizes.

Features
Real-time packet capture using Scapy.
Packet filtering by source/destination IP, ports, protocol, and packet size.
Suspicious activity flagging, including bursts of packets from the same source.
Interactive dashboard for visualizing network traffic using Streamlit.
Graphical representation of packet statistics.
Getting Started
Prerequisites
Python 3.11 or higher
WSL 2 (if on Windows)
Administrator privileges to run packet sniffing
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/network_traffic_analyzer.git
cd network_traffic_analyzer
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
streamlit run main.py
Usage
Select network interface: From the dropdown, choose the network interface you want to monitor.
Start capturing: Click the start button to begin capturing network packets.
Filtering options: Use the sidebar to filter traffic by IPs, ports, protocol, and packet size.
View analytics: After capturing traffic, use the analytics section to visualize network activity and flag suspicious packets.
Flagging Rules
Burst flagging: Packets coming from the same source IP in rapid succession are flagged if they exceed a predefined threshold and occur within a certain time frame.
Customizable filters: Filter traffic based on specific criteria such as protocol, packet size, or ports.
Example

File Structure
main.py: The entry point of the application.
analyzer/flag.py: Contains the logic for flagging suspicious activity.
analyzer/capture.py: Handles packet capturing.
analyzer/filter.py: Manages filtering of network traffic.
ui_layout.py: Defines the layout and design of the Streamlit dashboard.
tests/: Contains unit tests for burst detection and flagging logic.
Future Improvements
Expand detection rules to include more suspicious behaviors.
Implement more complex traffic analysis algorithms.
Contributing
Contributions are welcome! Please create a pull request or open an issue if you have suggestions or find bugs.

License
This project is licensed under the MIT License - see the LICENSE file for details.