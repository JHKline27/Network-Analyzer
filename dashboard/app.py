import threading
import tkinter as tk
from tkinter import messagebox
from analyzer.capture import capture, process_packet  # Import your capture and processing functions
from analyzer.store import save_to_csv  # Import your save function
from scapy.all import get_if_list
from dashboard.templates.gui_layout import TrafficAnalyzerGUI  # Import the GUI layout

class TrafficAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.gui = TrafficAnalyzerGUI(root)

        # Load interfaces
        self.load_interfaces()

        # Bind buttons to methods
        self.gui.start_button.config(command=self.on_interface_selected)
        self.gui.stop_button.config(command=self.stop_capture)

        self.capturing = False

    def load_interfaces(self):
        interfaces = get_if_list()
        self.gui.interface_var.set(interfaces[0])  # Set default selection
        self.gui.interface_menu['menu'].delete(0, 'end')  # Clear the menu
        for interface in interfaces:
            self.gui.interface_menu['menu'].add_command(label=interface, command=lambda value=interface: self.gui.interface_var.set(value))

    def on_interface_selected(self):
        selected_interface = self.gui.interface_var.get()  # Get the selected interface
        if selected_interface:
            self.start_capture(selected_interface)  # Pass the selected interface
        else:
            messagebox.showwarning("Warning", "Please select a network interface.")

    def start_capture(self, selected_interface):
        self.clear_csv_file('data/captured_packets.csv')
        self.capturing = True
        self.gui.update_status("Status: Capturing...")
        self.gui.start_button.config(state=tk.DISABLED)
        self.gui.stop_button.config(state=tk.NORMAL)

        # Start capturing packets in a new thread
        threading.Thread(target=self.capture_packets, args=(selected_interface,), daemon=True).start()
    def clear_csv_file(self, filename):
        """Clear the contents of the specified CSV file."""
        with open(filename, 'w') as file:
            # Write the header row if necessary
            file.write("timestamp,src_ip,dst_ip,protocol,packet_size\n")
    def stop_capture(self):
        self.capturing = False
        self.gui.update_status("Status: Capture Stopped")
        self.gui.start_button.config(state=tk.NORMAL)
        self.gui.stop_button.config(state=tk.DISABLED)

    def capture_packets(self, selected_interface):
        if selected_interface:
            print(f"Capturing on interface: {selected_interface}")  # Debugging output
            capture(interface=selected_interface, callback=self.packet_summary)
        else:
            messagebox.showwarning("Warning", "No interface selected for capturing.")

    def packet_summary(self, packet):
        """Process packet and update GUI."""
        data = process_packet(packet)
        if data:
            packet_summary = packet.summary()
            print("Packet captured:", packet_summary)  # Debugging output
            self.gui.update_packet_display(packet_summary)  # Update display with packet summary
            save_to_csv(data)  # Save data to CSV
