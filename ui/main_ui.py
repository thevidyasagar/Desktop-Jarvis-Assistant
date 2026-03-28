import tkinter as tk
from tkinter import ttk


class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.geometry("420x280")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")  # dark blue

        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="JARVIS",
            font=("Segoe UI", 28, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title.pack(pady=20)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Status: Idle",
            font=("Segoe UI", 12),
            fg="#e5e7eb",
            bg="#0f172a"
        )
        self.status_label.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=20)

        start_btn = ttk.Button(
            btn_frame,
            text="Start Listening",
            command=self.start_listening
        )
        start_btn.grid(row=0, column=0, padx=10)

        stop_btn = ttk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_listening
        )
        stop_btn.grid(row=0, column=1, padx=10)

    def start_listening(self):
        self.status_label.config(text="Status: Listening...")

    def stop_listening(self):
        self.status_label.config(text="Status: Idle")

    def run(self):
        self.root.mainloop()


def start_ui():
    app = JarvisUI()
    app.run()
