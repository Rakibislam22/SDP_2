import customtkinter
import os
import pygame

class SoundPopup(customtkinter.CTkFrame):
    def __init__(self, master, sound_selected_callback=None, close_callback=None, **kwargs):
        super().__init__(master, width=300, height=300, fg_color="transparent", border_width=2,
                         border_color="red", corner_radius=10, **kwargs)
        self.pack_propagate(False)
        self.close_callback = close_callback
        self.sound_selected_callback = sound_selected_callback
        self._visible = False
        self.selected_sound = customtkinter.StringVar()
        self.playing = False

        # Init pygame mixer
        pygame.mixer.init()

        # Frame
        self.tempf = customtkinter.CTkFrame(self, fg_color="black")
        self.tempf.pack(fill="both", expand=True)

        # Title
        title = customtkinter.CTkLabel(
            self.tempf,
            text="Sound List",
            text_color="white",
            font=customtkinter.CTkFont("Courier New", 18, weight="bold")
        )
        title.pack(pady=10)

        # Sound list frame
        self.sound_frame = customtkinter.CTkFrame(self.tempf, fg_color="transparent")
        self.sound_frame.pack(fill="both", expand=True, padx=10)

        # Load sounds from ./sound/
        self.sounds = []
        self.buttons = []

        sound_folder = "sound"
        if os.path.exists(sound_folder):
            for file in os.listdir(sound_folder):
                if file.endswith(".mp3"):
                    sound_path = os.path.join(sound_folder, file)
                    self._add_sound_option(file, sound_path)

    def _add_sound_option(self, file_name, full_path):
        row = customtkinter.CTkFrame(self.sound_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)

        radio = customtkinter.CTkRadioButton(
            row, text=file_name, variable=self.selected_sound,
            value=full_path, text_color="white",
            command=self._on_select
        )
        radio.pack(side="left", padx=(5, 10), pady=2)

        btn = customtkinter.CTkButton(
            row, text="Play", width=40, height=25, command=lambda: self._toggle_play(full_path, btn)
        )
        btn.pack(side="right", padx=5)

        self.sounds.append((file_name, full_path))
        self.buttons.append(btn)

    def _toggle_play(self, path, button):
        if not self.playing:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.playing = True
            button.configure(text="Pause")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.playing = False
                button.configure(text="Play")
            else:
                pygame.mixer.music.unpause()
                self.playing = True
                button.configure(text="Pause")

    def _on_select(self):
        if self.sound_selected_callback:
            self.sound_selected_callback(self.selected_sound.get())

    def toggle(self):
        if self._visible:
            self.hide()
        else:
            self.show()

    def show(self):
        if not self._visible:
            self.place(x=800, y=530, anchor="center")
            self.lift()
            self.master.bind("<Button-1>", self._check_click_outside)
            self.master.bind("<Escape>", self._check_click_outside)
            self._visible = True

    def hide(self):
        if self._visible:
            self.place_forget()
            self.master.unbind("<Button-1>")
            self.master.unbind("<Escape>")
            pygame.mixer.music.stop()
            self._visible = False

    def _check_click_outside(self, event):
        x1 = self.winfo_rootx()
        y1 = self.winfo_rooty()
        x2 = x1 + self.winfo_width()
        y2 = y1 + self.winfo_height()

        if hasattr(event, "keysym") and event.keysym == "Escape":
            self.hide()
            if self.close_callback:
                self.close_callback()
        elif not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
            self.hide()
            if self.close_callback:
                self.close_callback()
