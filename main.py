import tkinter as tk
from dashboard.app import TrafficAnalyzerApp  # Import the application logic

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")  # Set an initial size for the window
    app = TrafficAnalyzerApp(root)  # Initialize the application
    root.mainloop()  # Start the main event loop
