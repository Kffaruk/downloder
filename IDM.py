import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import yt_dlp

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced YouTube Video Downloader")
        self.root.geometry("600x300")

        # Variables
        self.url = tk.StringVar()
        self.output_path = tk.StringVar(value=os.getcwd())

        # Widgets
        self.build_widgets()

    def build_widgets(self):
        tk.Label(self.root, text="YouTube Video URL:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.url, width=70).pack(pady=5)

        tk.Label(self.root, text="Save to Folder:").pack(pady=5)
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=5)
        tk.Entry(path_frame, textvariable=self.output_path, width=50).pack(side=tk.LEFT)
        tk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Download HD Video", command=self.start_download_thread).pack(pady=20)

        self.progress_label = tk.Label(self.root, text="Progress: Waiting...", fg="blue")
        self.progress_label.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path.set(folder_selected)

    def start_download_thread(self):
        thread = threading.Thread(target=self.download_video)
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '')
            eta = d.get('eta', '')
            self.progress_label.config(text=f"Downloading... {percent} at {speed}, ETA: {eta}s")
        elif d['status'] == 'finished':
            self.progress_label.config(text="Download complete! Merging...")

    def download_video(self):
        url = self.url.get()
        output_dir = self.output_path.get()

        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
            return

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s_%(id)s.%(ext)s'),
            'format': 'bv*[ext=mp4]+ba[ext=m4a]/best',
            'merge_output_format': 'mp4',
            'ffmpeg_location': r"G:/Software/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin",
            'progress_hooks': [self.progress_hook],
            'nooverwrites': True,  # আগের ফাইল থাকলে ওভাররাইট করবে না, স্কিপ করবে
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Video downloaded and merged successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed:\n{str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
