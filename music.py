import customtkinter as ctk
import tkinter.filedialog as fd
import pygame
from pathlib import Path
from PIL import Image
from customtkinter import CTkImage
from mutagen.mp3 import MP3
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        #self.root.title("Music Player")
        #self.center_window(400,500)
        #self.root.resizable(False, False)
        self.playlist = []
        self.current_index = 0
        img = Path(__file__).resolve().parent / "image" / "sound.png"
        self.cover_image = CTkImage(
            
            light_image=Image.open(img).resize((300, 300), Image.Resampling.LANCZOS),
            dark_image=Image.open(img).resize((300, 300), Image.Resampling.LANCZOS),
            size=(300, 300))
        self.main_frame = ctk.CTkFrame(self.root, width=420, height=560)
        self.main_frame.pack()
        self.main_frame.pack_propagate(False)


        # === Initialize pygame ===
        pygame.mixer.init()

        # === State variables ===
        self.current_song_length = 0
        self.is_seeking = False
        self.playback_offset = 0
        self.current_volume = 0.5
        self.is_muted = False
        self.current_song_index = -1
        self.is_paused = False
        self.playlist_window = None
        self.repeat_playlist = True

        # === UI Components ===
        self.create_widgets()
        self.update_progress()

    def center_window(self, width=400, height=500):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.song_title = ctk.CTkLabel(self.main_frame, text="Song Title", font=("Arial", 18, "bold"))
        self.song_title.pack(pady=(10, 5))

        cover_frame = ctk.CTkFrame(self.main_frame, width=300, height=230)
        cover_frame.pack(pady=5)
        cover_frame.pack_propagate(False)
        self.cover_label = ctk.CTkLabel(cover_frame, image=self.cover_image, text="")
        self.cover_label.pack(expand=True)

        time_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.current_time_label = ctk.CTkLabel(time_frame, text="0:00")
        self.current_time_label.pack(side="left")

        self.total_time_label = ctk.CTkLabel(time_frame, text="0:00")
        self.total_time_label.pack(side="right")

        self.seek_slider = ctk.CTkSlider(self.main_frame, from_=0, to=100, number_of_steps=100)
        self.seek_slider.pack(fill="x", padx=20, pady=10)
        self.seek_slider.set(0)
        self.seek_slider.configure(command=self.on_slider_change)
        self.seek_slider.bind("<ButtonRelease-1>", self.on_slider_release)

        controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        controls_frame.pack(pady=(10, 0))

        self.back_btn = ctk.CTkButton(controls_frame, text="⏮️", width=40)
        self.back_btn.pack(side="left", padx=5)
        self.back_btn.bind("<Button-1>", self.skip_backward)
        self.back_btn.bind("<Double-Button-1>", self.play_previous_song)

        ctk.CTkButton(controls_frame, text="⏯️", width=40, command=self.play_pause).pack(side="left", padx=5)

        self.next_btn = ctk.CTkButton(controls_frame, text="⏭️", width=40)
        self.next_btn.pack(side="left", padx=5)
        self.next_btn.bind("<Button-1>", self.skip_forward)
        self.next_btn.bind("<Double-Button-1>", self.play_next_song)

        tool_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=(20, 10))

        self.sound_btn = ctk.CTkButton(tool_frame, text="🔈", width=20, command=self.toggle_sound)
        self.sound_btn.grid(row=0, column=0, padx=(5, 2))

        self.volume_slider = ctk.CTkSlider(tool_frame, from_=0, to=1, number_of_steps=100, width=80)
        self.volume_slider.grid(row=0, column=1, padx=(2, 10))
        self.volume_slider.set(self.current_volume)
        self.volume_slider.configure(command=self.on_volume_change)

        ctk.CTkButton(tool_frame, text=" ", fg_color="transparent", width=20, state="disabled").grid(row=0, column=2, padx=15)
        self.open_btn = ctk.CTkButton(tool_frame, text="📂", width=40, command=lambda: self.open_file(auto_play=True))
        self.open_btn.grid(row=0, column=3, padx=(10, 5))

        self.playlist_btn = ctk.CTkButton(tool_frame, text="📜", width=40, command=self.show_playlist_window)
        self.playlist_btn.grid(row=0, column=4, padx=(10, 5))

        tool_frame.grid_columnconfigure((0, 1, 3, 4), weight=0)
        tool_frame.grid_columnconfigure(2, weight=1)

        self.name_right = ctk.CTkLabel(self.main_frame, text="©Ismail hossain   ", font=("Arial", 10, "bold"))
        self.name_right.place(relx = 1.0, rely = 1.0, anchor ='se')


    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"

    def update_progress(self):
        if not self.is_seeking and pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() // 1000
            actual_time = int(self.playback_offset + pos)
            if actual_time <= self.current_song_length:
                self.seek_slider.set(actual_time)
                self.current_time_label.configure(text=self.format_time(actual_time))
            if actual_time >= self.current_song_length:
                if not self.is_paused:
                    self.play_next_song()
        self.root.after(500, self.update_progress)

    def on_slider_change(self, value):
        self.is_seeking = True
        self.current_time_label.configure(text=self.format_time(value))

    def on_slider_release(self, event=None):
        self.is_seeking = False
        seek_time = self.seek_slider.get()
        pygame.mixer.music.play(start=seek_time)
        self.playback_offset = seek_time

    def on_volume_change(self, val):
        self.current_volume = float(val)
        if self.current_volume == 0:
            self.is_muted = True
            self.sound_btn.configure(text="🔇")
        else:
            self.is_muted = False
            self.sound_btn.configure(text="🔊")
        pygame.mixer.music.set_volume(self.current_volume)

    def toggle_sound(self):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.current_volume)
            self.volume_slider.set(self.current_volume)
            self.sound_btn.configure(text="🔊")
            self.is_muted = False
        else:
            pygame.mixer.music.set_volume(0)
            self.volume_slider.set(0)
            self.sound_btn.configure(text="🔇")
            self.is_muted = True

    def play_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
        else:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def play_song(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.song_title.configure(text=os.path.basename(file_path))

        audio = MP3(file_path)
        self.current_song_length = int(audio.info.length)
        self.total_time_label.configure(text=self.format_time(self.current_song_length))

        self.playback_offset = 0
        self.seek_slider.configure(to=self.current_song_length)
        self.seek_slider.set(0)
        self.is_paused = False

    def skip_backward(self, event=None):
        current_pos = pygame.mixer.music.get_pos() // 1000
        new_pos = self.playback_offset + current_pos - 10
        pygame.mixer.music.play(start=new_pos)
        self.playback_offset = new_pos

    def skip_forward(self, event=None):
        current_pos = pygame.mixer.music.get_pos() // 1000
        new_pos = self.playback_offset + current_pos + 10
        if new_pos < self.current_song_length:
            pygame.mixer.music.play(start=new_pos)
            self.playback_offset = new_pos
        else:
            self.play_next_song()

    def play_previous_song(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.play_song(self.playlist[self.current_index])

    def play_next_song(self, event=None):
        if self.playlist:
            self.current_index += 1
            if self.current_index >= len(self.playlist):
                if self.repeat_playlist:
                    self.current_index = 0
                else:
                    return
            self.play_song(self.playlist[self.current_index])

    def open_file(self, auto_play=True):
        files = fd.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        if files:
            self.playlist.extend(files)
            if auto_play:
                self.current_index = len(self.playlist) - len(files)  # Start from the first newly added song
                self.play_song(self.playlist[self.current_index])
            self.refresh_playlist()

    def remove_selected_song(self):
        if self.scroll_frame.winfo_children():
            selected_index = len(self.scroll_frame.winfo_children()) - 1
            if 0 <= selected_index < len(self.playlist):
                self.playlist.pop(selected_index)
                if selected_index == self.current_index:
                    pygame.mixer.music.stop()
                if self.current_index >= len(self.playlist):
                    self.current_index = 0
                self.refresh_playlist()

    def refresh_playlist(self):
        if not hasattr(self, 'scroll_frame') or not self.scroll_frame.winfo_exists():
            return  # Avoid updating non-existent scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        for idx, song in enumerate(self.playlist):
            title = os.path.basename(song)
            btn = ctk.CTkButton(self.scroll_frame, text=title, width=250,
                                command=lambda i=idx: self.play_song(self.playlist[i]))
            btn.pack(pady=2)

    def show_playlist_window(self):
        if self.playlist_window and self.playlist_window.winfo_exists():
            self.playlist_window.destroy()
            self.playlist_window = None
            return

        self.playlist_window = ctk.CTkToplevel(self.root)
        self.playlist_window.title("Playlist")
        self.playlist_window.geometry("300x500")

        self.playlist_window.transient(self.root)
        self.playlist_window.attributes('-topmost', True)

        self.open_playlist_right_position()

        scroll_frame = ctk.CTkScrollableFrame(self.playlist_window, label_text="Playlist")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.scroll_frame = scroll_frame
        self.refresh_playlist()

        btn_frame = ctk.CTkFrame(self.playlist_window)
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="➕ Add", command=lambda: self.open_file(auto_play=False)).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="❌ Remove", command=self.remove_selected_song).pack(side="left", padx=5)



    def open_playlist_right_position(self):
        # Position the playlist window just to the right of the main window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        playlist_x = root_x + root_width + 10
        playlist_y = root_y
        self.playlist_window.geometry(f"+{playlist_x}+{playlist_y}")


if __name__ == "__main__":
    #ctk.set_appearance_mode("dark")
    #ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MusicPlayer(root)
    #root.mainloop()