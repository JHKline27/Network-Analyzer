import tkinter as tk
from tkinter import font, Toplevel, messagebox
from analyzer.visualize import (plot_protocol_distribution, plot_packet_size_distribution,
                       plot_packet_frequency_over_time, plot_top_ip_addresses)

class TrafficAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        
        # Set minimum window size
        self.root.minsize(400, 300)
        self.root.title("Network Traffic Analyzer")
        
        # Set background color
        self.root.configure(bg="#2e2e2e")

        # Configure grid layout
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=4)
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Define custom font
        custom_font = font.Font(family="Helvetica", size=12)

        # Title Label
        self.title_label = tk.Label(root, text="Network Traffic Analyzer", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, columnspan=2, pady=(10, 20))

        # Interface selection
        self.interface_label = tk.Label(root, text="Select Network Interface:", bg="#2e2e2e", fg="#ffffff", font=custom_font)
        self.interface_label.grid(row=1, column=0, pady=10, sticky='ew')

        # Dropdown for network interfaces
        self.interface_var = tk.StringVar(root)
        self.interface_menu = tk.OptionMenu(root, self.interface_var, [])
        self.interface_menu.grid(row=2, column=0, pady=10, sticky='ew')
        self.interface_menu.configure(bg="#ffffff")

        # Start Capture Button
        self.start_button = tk.Button(root, text="Start Capture", bg="#4CAF50", fg="#ffffff", font=custom_font)
        self.start_button.grid(row=3, column=0, pady=10, sticky='ew')

        # Stop Capture Button (disabled initially)
        self.stop_button = tk.Button(root, text="Stop Capture", state=tk.DISABLED, bg="#f44336", fg="#ffffff", font=custom_font)
        self.stop_button.grid(row=3, column=1, pady=10, sticky='ew')

        # Status Label
        self.status_label = tk.Label(root, text="Status: Ready", bg="#2e2e2e", fg="#ffffff", font=custom_font)
        self.status_label.grid(row=4, column=0, pady=10, sticky='ew')

        # Display for real-time captured packets
        self.packet_display = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg="#ffffff", font=custom_font)
        self.packet_display.grid(row=5, column=0, pady=10, sticky='nsew')

        # Analytics Button
        self.analytics_button = tk.Button(root, text="View Analytics", bg="#2196F3", fg="#ffffff", font=custom_font, command=self.open_analytics)
        self.analytics_button.grid(row=6, column=0, pady=10, sticky='ew')

        # Ensure the widgets resize properly
        self.start_button.grid_propagate(False)
        self.stop_button.grid_propagate(False)
        self.packet_display.grid_propagate(False)

    def update_packet_display(self, packet_summary):
        self.packet_display.config(state=tk.NORMAL)
        self.packet_display.insert(tk.END, packet_summary + '\n')
        self.packet_display.config(state=tk.DISABLED)

    def update_status(self, status_message):
        self.status_label.config(text=status_message)

    def open_analytics(self):
        """Open a new window for analytics."""
        analytics_window = Toplevel(self.root)
        analytics_window.title("Analytics")
        analytics_window.geometry("600x400")
        analytics_window.configure(bg="#2e2e2e")

        # Instructions label
        instructions_label = tk.Label(analytics_window, text="Choose an analysis to perform:", bg="#2e2e2e", fg="#ffffff")
        instructions_label.pack(pady=10)

        # Protocol Distribution Button
        protocol_button = tk.Button(analytics_window, text="Protocol Distribution", command=self.show_protocol_distribution)
        protocol_button.pack(pady=5)

        # Packet Size Distribution Button
        packet_size_button = tk.Button(analytics_window, text="Packet Size Distribution", command=self.show_packet_size_distribution)
        packet_size_button.pack(pady=5)

        # Packet Frequency Over Time Button
        packet_frequency_button = tk.Button(analytics_window, text="Packet Frequency Over Time", command=self.show_packet_frequency_over_time)
        packet_frequency_button.pack(pady=5)

        # Top IP Addresses Button
        top_ip_button = tk.Button(analytics_window, text="Top IP Addresses", command=self.show_top_ip_addresses)
        top_ip_button.pack(pady=5)

    def show_protocol_distribution(self):
        """Call the visualization function for protocol distribution."""
        plot_protocol_distribution()

    def show_packet_size_distribution(self):
        """Call the visualization function for packet size distribution."""
        plot_packet_size_distribution()

    def show_packet_frequency_over_time(self):
        """Call the visualization function for packet frequency over time."""
        plot_packet_frequency_over_time()

    def show_top_ip_addresses(self):
        """Call the visualization function for top IP addresses."""
        plot_top_ip_addresses()