import os
import time
import ctypes
import pathlib
import threading
import webbrowser
import urllib.parse
import customtkinter as ctk
from tkinter import filedialog

# ---------------- VLC PATH FIX ----------------

vlc_path = os.path.abspath("vlc")

libvlc_path = os.path.join(vlc_path, "libvlc.dll")
if not os.path.exists(libvlc_path):
    raise FileNotFoundError("libvlc.dll not found in 'vlc' folder.")
ctypes.CDLL(libvlc_path)

plugin_path = os.path.join(vlc_path, "plugins")
os.environ["VLC_PLUGIN_PATH"] = plugin_path
os.environ["PATH"] = vlc_path + os.pathsep + os.environ["PATH"]

import vlc


class VideoPlayerApp:
    def __init__(self, parent):
        self.parent = parent

        self.vlc_instance = vlc.Instance(
            '--no-xlib',
            '--no-video-title-show',
            '--avcodec-hw=none',
            '--aout=directsound'
        )
        self.media_player = self.vlc_instance.media_player_new()

        self.main_frame = ctk.CTkFrame(self.parent, width=650, height=550)
        self.main_frame.pack()
        self.main_frame.pack_propagate(False)

        self.video_panel = ctk.CTkLabel(self.main_frame, text="")
        self.video_panel.pack()
        self.video_panel.pack_propagate(False)

        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=0)

        self.create_widgets()

        self.update_thread = None
        self.stop_update = False

        self.update_thread = None
        self.stop_update = False

    def get_frame(self):
        return self.main_frame

    def create_widgets(self):
        self.movie_title = ctk.CTkLabel(self.bottom_frame, text="Video Title", font=("Arial", 18, "bold"))
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
        
        self.playlist_popup_btn = ctk.CTkButton(tool_frame, text="📄", width=40, command=self.open_playlist_popup)
        self.playlist_popup_btn.grid(row=0, column=4, padx=(5, 5))

        tool_frame.grid_columnconfigure((0, 1, 3), weight=0)
        tool_frame.grid_columnconfigure(2, weight=1)

        def open_ismail_github(event=None):
            webbrowser.open_new("https://github.com/kenshiro147") 

        self.name_right = ctk.CTkLabel(
            self.bottom_frame,
            text="©Ismail Hossain",
            font=("Arial", 10, "bold"),
            cursor="hand2",  # Hand cursor on hover
            text_color="#9e9e9e"  # Optional: consistent style
        )
        self.name_right.pack(anchor="se", padx=10, pady=(0, 5))
        self.name_right.bind("<Button-1>", open_ismail_github)


        
        

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

            attempts = 0
            width, height = 0, 0
            while (width == 0 or height == 0) and attempts < 10:
                time.sleep(0.1)
                width = self.media_player.video_get_width()
                height = self.media_player.video_get_height()
                attempts += 1

            if width > 0 and height > 0:
                self.resize_to_base_ratio(width, height)

            self.stop_update = False
            threading.Thread(target=self.update_slider_loop, daemon=True).start()

            # Save to playlist
            self.add_to_playlist(file_path)

    def play_from_playlist(self, file_path):
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

        attempts = 0
        width, height = 0, 0
        while (width == 0 or height == 0) and attempts < 10:
            time.sleep(0.1)
            width = self.media_player.video_get_width()
            height = self.media_player.video_get_height()
            attempts += 1

        if width > 0 and height > 0:
            self.resize_to_base_ratio(width, height)

        self.stop_update = False
        threading.Thread(target=self.update_slider_loop, daemon=True).start()     

    def resize_to_base_ratio(self, video_width, video_height):
        base_width = 650   # 16:9 bounding box width
        base_height = 400  # 16:9 bounding box height

        video_ratio = video_width / video_height
        base_ratio = base_width / base_height

        if video_ratio > base_ratio:
            # Video is wider than 16:9, fit to width
            new_width = base_width
            new_height = int(base_width / video_ratio)
        else:
            # Video is taller than 16:9 or equal, fit to height
            new_height = base_height
            new_width = int(base_height * video_ratio)

        self.video_panel.configure(width=new_width, height=new_height)
        self.main_frame.configure(width=new_width, height=new_height+200)
    
    def toggle_play(self):
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()

    def set_volume(self, vol):
        self.media_player.audio_set_volume(int(vol))
        self.sound_btn.configure(text="🔈" if vol > 0 else "🔇")

    def toggle_mute(self):
        is_muted = self.media_player.audio_get_mute()
        self.media_player.audio_set_mute(not is_muted)
        self.sound_btn.configure(text="🔈" if is_muted else "🔇")

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
    
    def add_to_playlist(self, file_path):
        playlist_file = "playlist.txt"
        if not os.path.exists(playlist_file):
            open(playlist_file, "w", encoding="utf-8").close()

        with open(playlist_file, "r", encoding="utf-8") as f:
            existing = [line.strip() for line in f.readlines()]

        if file_path not in existing:
            with open(playlist_file, "a", encoding="utf-8") as f:
                f.write(file_path + "\n")


    def load_playlist(self):
        playlist_file = "playlist.txt"
        if os.path.exists(playlist_file):
            with open(playlist_file, "r", encoding="utf-8") as f:
                paths = [line.strip() for line in f.readlines()]
            return paths
        return []

    

    def open_playlist_popup(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Playlist")
        popup.geometry("300x400")
        popup.resizable(False, False)

        # Make it appear on top
        popup.transient(self.parent)       
        popup.attributes('-topmost', True)
        popup.lift()                       

        # Top control buttons
        top_controls = ctk.CTkFrame(popup)
        top_controls.pack(fill="x", padx=10, pady=(10, 0))

        add_btn = ctk.CTkButton(top_controls, text="➕ Add", width=70, command=self.manual_add_to_playlist)
        add_btn.pack(side="left", padx=5)

        remove_btn = ctk.CTkButton(top_controls, text="❌ Remove Selected", width=140, command=self.remove_selected_from_playlist)
        remove_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(top_controls, text="🧹 Clear All", width=70, command=self.clear_playlist)
        clear_btn.pack(side="left", padx=5)

        # Scrollable frame for playlist
        self.playlist_frame = ctk.CTkScrollableFrame(popup, width=330, height=400, label_text="Saved Videos")
        self.playlist_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.refresh_playlist_buttons()

    def play_from_popup(self, file_path, window):
        window.destroy()  # Close popup
        self.play_from_playlist(file_path)

    def refresh_playlist_buttons(self):
        # Clear current buttons
        for widget in self.playlist_frame.winfo_children():
            widget.destroy()

        self.button_refs = []  # Keep references for selection
        self.selected_index = None

        playlist = self.load_playlist()
        for idx, file_path in enumerate(playlist):
            file_name = os.path.basename(file_path)

            def on_click(event, path=file_path, index=idx):
                self.selected_index = index
                self.highlight_selected_button(index)

            btn = ctk.CTkButton(self.playlist_frame, text=file_name, anchor="w", width=280,
                                command=lambda path=file_path: self.play_from_playlist(path))
            btn.bind("<Button-1>", on_click)
            btn.pack(fill="x", padx=5, pady=2)

            self.button_refs.append(btn)

    def highlight_selected_button(self, index):
        for i, btn in enumerate(self.button_refs):
            if i == index:
                btn.configure(fg_color="#1f6aa5")  # Highlight color
            else:
                btn.configure(fg_color="#3a3a3a")  # Default

    def manual_add_to_playlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.add_to_playlist(file_path)
            self.refresh_playlist_buttons()

    def remove_selected_from_playlist(self):
        if self.selected_index is None:
            return

        try:
            playlist = self.load_playlist()
        except Exception as e:
            print("Error loading playlist:", e)
            return

        if 0 <= self.selected_index < len(playlist):
            removed_path = playlist[self.selected_index]

            # Get current playing media path safely
            current_media = self.media_player.get_media()
            current_path = ""
            if current_media:
                try:
                    media_mrl = current_media.get_mrl()
                    if media_mrl.startswith("file:///"):
                        url_path = media_mrl[7:]  # Remove 'file://'
                        url_path = urllib.parse.unquote(url_path)
                        current_path = str(pathlib.Path(url_path).resolve())
                except Exception as e:
                    print("Error getting current media path:", e)

            # Remove the selected video
            del playlist[self.selected_index]

            try:
                with open("playlist.txt", "w", encoding="utf-8") as f:
                    for path in playlist:
                        f.write(path + "\n")
            except Exception as e:
                print("Error writing updated playlist:", e)
                return

            # If the removed video was currently playing
            if  self.media_player.is_playing():
                self.media_player.stop()
                self.movie_title.configure(text="Video Title")
                self.video_panel.configure(image=None)
                self.seek_slider.set(0)
                self.current_time_label.configure(text="0:00")
                self.total_time_label.configure(text="0:00")

                if playlist:
                    if self.selected_index >= len(playlist):
                        self.selected_index = len(playlist) - 1
                    if 0 <= self.selected_index < len(playlist):
                        self.play_from_playlist(playlist[self.selected_index])
                    else:
                        self.selected_index = None
                else:
                    self.selected_index = None
            else:
                # Just update the selected index safely
                if self.selected_index >= len(playlist):
                    self.selected_index = len(playlist) - 1 if playlist else None

            self.refresh_playlist_buttons()


    def clear_playlist(self):
        open("playlist.txt", "w", encoding="utf-8").close()
        self.selected_index = None
        if self.media_player.is_playing():
            self.media_player.stop()
            self.movie_title.configure(text="Video Title")
            self.video_panel.configure(image=None)
            self.seek_slider.set(0)
            self.current_time_label.configure(text="0:00")
            self.total_time_label.configure(text="0:00")
        self.refresh_playlist_buttons()

