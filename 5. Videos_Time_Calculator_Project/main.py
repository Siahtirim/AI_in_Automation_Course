import cv2
import os
import customtkinter as ctk
from tkinter import filedialog
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VideoDurationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MP4 Duration Calculator")
        self.geometry("600x450")
        self.resizable(False, False)

        self.path = ""

        # ===== Title =====
        self.title_label = ctk.CTkLabel(
            self,
            text="🎬 MP4 Duration & Size Calculator",
            font=("Arial", 26, "bold")
        )
        self.title_label.pack(pady=20)

        # ===== Select Folder Button =====
        self.select_button = ctk.CTkButton(
            self,
            text="Select Folder",
            width=200,
            height=40,
            command=self.select_folder
        )
        self.select_button.pack(pady=10)

        # ===== Selected Path =====
        self.path_label = ctk.CTkLabel(
            self,
            text="No folder selected",
            wraplength=500
        )
        self.path_label.pack(pady=5)

        # ===== Start Button =====
        self.start_button = ctk.CTkButton(
            self,
            text="Start Calculation",
            width=200,
            height=40,
            fg_color="green",
            hover_color="#1f6f43",
            command=self.start_thread
        )
        self.start_button.pack(pady=15)

        # ===== Progress Bar =====
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)

        # ===== Results =====
        self.result_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 16)
        )
        self.result_label.pack(pady=20)

    def select_folder(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.path_label.configure(text=self.path)

    def start_thread(self):
        thread = threading.Thread(target=self.calculate_duration)
        thread.start()

    def calculate_duration(self):
        if not self.path:
            self.result_label.configure(text="⚠ Please select a folder first!")
            return

        mp4_files = []

        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".mp4"):
                    mp4_files.append(os.path.join(root, file))

        total_files = len(mp4_files)
        self.result_label.configure(text=f"Found {total_files} videos")

        total_hours = 0.0

        for index, file in enumerate(mp4_files):
            cap = cv2.VideoCapture(file)
            duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
            hours = float(duration / 3600.0)
            total_hours += hours
            cap.release()

            progress_value = (index + 1) / total_files if total_files > 0 else 0
            self.progress.set(progress_value)

        self.result_label.configure(
            text=f"🎉 Total Time: {round(total_hours,2)} hours"
        )


if __name__ == "__main__":
    app = VideoDurationApp()
    app.mainloop()