import customtkinter
import os
import pygame

class SoundPopup(customtkinter.CTkFrame):
    def __init__(self, master, sound_selected_callback=None, close_callback=None, **kwargs):
        super().__init__(master, width=250, height=280, fg_color="transparent", border_width=2,
                         border_color="red", corner_radius=15, **kwargs)
        self.pack_propagate(False)
        self.close_callback = close_callback
        self.sound_selected_callback = sound_selected_callback
        self._visible = False
        self.selected_sound = customtkinter.StringVar()
        self.playing = False

        # Init pygame mixer
        pygame.mixer.init()

        self.current_button = None  # Track which button is playing

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
        self.sound_frame = customtkinter.CTkScrollableFrame(self.tempf, fg_color="transparent")
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

        # Set first radio as selected by default
        if self.sounds:
            self.selected_sound.set(self.sounds[0][1])
            if self.sound_selected_callback:
                self.sound_selected_callback(self.sounds[0][1])
        
        

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
            row, text="▶", width=30, height=20, command=lambda: self._toggle_play(full_path, btn)
        )
        btn.pack(side="right", padx=5)

        self.sounds.append((file_name, full_path))
        self.buttons.append(btn)

    def _toggle_play(self, path, button):
        if not self.playing or self.current_button != button:
            pygame.mixer.music.stop()
            for btn in self.buttons:
                btn.configure(text="▶")

            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.playing = True
            self.current_button = button
            button.configure(text="⏹")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.playing = False
                button.configure(text="▶")
            else:
                pygame.mixer.music.unpause()
                self.playing = True
                button.configure(text="⏹")

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
            self.place(x=822, y=548, anchor="center")
            self.lift()
            self.master.bind("<Button-1>", self._check_click_outside)
            self.master.bind("<Escape>", self._check_click_outside)
            self._visible = True

    def hide(self):
        if self._visible:
            self.place_forget()
            self.master.unbind("<Button-1>")
            self.master.unbind("<Escape>")

            # Stop any playing sound
            pygame.mixer.music.stop()
            self.playing = False

            # Reset all buttons to ▶
            for btn in self.buttons:
                btn.configure(text="▶")

            self.current_button = None  # Optional: reset reference to last button
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
