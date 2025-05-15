import os
import time
import ctypes
import threading
import customtkinter as ctk
from tkinter import filedialog

# ---------------- VLC PATH FIX ----------------

# Absolute path to 'vlc' folder containing 'libvlc.dll,plugin'
vlc_path = os.path.abspath("vlc")

# Manually load libvlc.dll
libvlc_path = os.path.join(vlc_path, "libvlc.dll")
if not os.path.exists(libvlc_path):
    raise FileNotFoundError("libvlc.dll not found in 'vlc' folder.")
ctypes.CDLL(libvlc_path)

# Add VLC path to system environment for plugin loading
plugin_path = os.path.join(vlc_path, "plugins")

os.environ["VLC_PLUGIN_PATH"] = plugin_path
os.environ["PATH"] = vlc_path + os.pathsep + os.environ["PATH"]

# Now import VLC safely
import vlc


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomTkinter Video Player")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # VLC instance using plugin path
        plugin_path = os.path.join(vlc_path, "plugins")
        self.vlc_instance = vlc.Instance(
            '--no-xlib',
            '--no-video-title-show',
            '--avcodec-hw=none',
            '--aout=directsound'
        )

        self.media_player = self.vlc_instance.media_player_new()

        # ------------------ UI ------------------
        self.main_frame = ctk.CTkFrame(self.root, width=400, height=500)
        self.main_frame.pack()
        self.main_frame.pack_propagate(False)

        self.video_panel = ctk.CTkLabel(self.main_frame, text="")
        self.video_panel.pack(expand=True, fill="both")

        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.create_widgets()

        self.update_thread = None
        self.stop_update = False

    def create_widgets(self):
        self.movie_title = ctk.CTkLabel(self.bottom_frame, text="Movie Title", font=("Arial", 18, "bold"))
        self.movie_title.pack(pady=(5, 5))

        time_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=(0, 5))

        self.current_time_label = ctk.CTkLabel(time_frame, text="0:00")
        self.current_time_label.pack(side="left")

        self.total_time_label = ctk.CTkLabel(time_frame, text="0:00")
        self.total_time_label.pack(side="right")

        self.seek_slider = ctk.CTkSlider(self.bottom_frame, from_=0, to=100, number_of_steps=100)
        self.seek_slider.pack(fill="x", padx=20, pady=5)
        self.seek_slider.set(0)
        self.seek_slider.bind("<ButtonRelease-1>", self.seek_video)

        controls_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        controls_frame.pack(pady=5)

        self.back_btn = ctk.CTkButton(controls_frame, text="⏮️", width=40, command=self.skip_backward)
        self.back_btn.pack(side="left", padx=5)

        self.play_btn = ctk.CTkButton(controls_frame, text="⏯️", width=40, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=5)

        self.next_btn = ctk.CTkButton(controls_frame, text="⏭️", width=40, command=self.skip_forward)
        self.next_btn.pack(side="left", padx=5)

        tool_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=(5, 5))

        self.sound_btn = ctk.CTkButton(tool_frame, text="🔈", width=20, command=self.toggle_mute)
        self.sound_btn.grid(row=0, column=0, padx=(5, 2))

        self.volume_slider = ctk.CTkSlider(tool_frame, from_=0, to=100, number_of_steps=100, width=80,
                                           command=self.set_volume)
        self.volume_slider.grid(row=0, column=1, padx=(2, 10))
        self.volume_slider.set(100)

        ctk.CTkButton(tool_frame, text=" ", fg_color="transparent", width=20, state="disabled").grid(
            row=0, column=2, padx=15)

        self.open_btn = ctk.CTkButton(tool_frame, text="📂", width=40, command=self.open_file)
        self.open_btn.grid(row=0, column=3, padx=(10, 5))

        tool_frame.grid_columnconfigure((0, 1, 3), weight=0)
        tool_frame.grid_columnconfigure(2, weight=1)

        self.name_right = ctk.CTkLabel(self.bottom_frame, text="©Ismail Hossain", font=("Arial", 10, "bold"))
        self.name_right.pack(anchor="se", padx=10, pady=(0, 5))

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.stop_update = True
            self.media = self.vlc_instance.media_new(file_path)
            self.media_player.set_media(self.media)

            handle = self.video_panel.winfo_id()
            if os.name == 'nt':
                self.media_player.set_hwnd(handle)
            else:
                self.media_player.set_xwindow(handle)

            self.media_player.play()
            self.movie_title.configure(text=os.path.basename(file_path))
            time.sleep(0.5)

            self.stop_update = False
            threading.Thread(target=self.update_slider_loop, daemon=True).start()

    def toggle_play(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    def set_volume(self, vol):
        self.media_player.audio_set_volume(int(vol))
        if vol == 0:
            self.sound_btn.configure(text="🔇")
        else:
            self.sound_btn.configure(text="🔈")

    def toggle_mute(self):
        is_muted = self.media_player.audio_get_mute()
        self.media_player.audio_set_mute(not is_muted)
        if is_muted:
            self.sound_btn.configure(text="🔈")
        else:
            self.sound_btn.configure(text="🔇")

    def seek_video(self, event=None):
        percent = self.seek_slider.get() / 100.0
        length = self.media_player.get_length()
        self.media_player.set_time(int(length * percent))

    def skip_forward(self):
        current = self.media_player.get_time()
        self.media_player.set_time(current + 10000)

    def skip_backward(self):
        current = self.media_player.get_time()
        self.media_player.set_time(max(0, current - 10000))

    def update_slider_loop(self):
        while not self.stop_update:
            time.sleep(1)
            if self.media_player and self.media_player.get_length() > 0:
                curr = self.media_player.get_time()
                total = self.media_player.get_length()
                self.seek_slider.set((curr / total) * 100)
                self.current_time_label.configure(text=self.format_time(curr // 1000))
                self.total_time_label.configure(text=self.format_time(total // 1000))

    def format_time(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02}"


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = VideoPlayerApp(root)
    root.mainloop()
