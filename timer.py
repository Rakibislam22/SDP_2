import customtkinter as ctk
import threading
import time
import pygame
import math

class TimerTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.running = False
        self.time_left = 0
        self.total_time = 0
        self.timer_thread = None

        # Sound init
        pygame.mixer.init()
        self.beep_file = "beep.wav"  # Replace with your .wav file path

        # Input frame
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(pady=10)

        self.hours_entry = ctk.CTkEntry(self.entry_frame, width=60, placeholder_text="HH")
        self.hours_entry.grid(row=0, column=0, padx=5)

        self.minutes_entry = ctk.CTkEntry(self.entry_frame, width=60, placeholder_text="MM")
        self.minutes_entry.grid(row=0, column=1, padx=5)

        self.seconds_entry = ctk.CTkEntry(self.entry_frame, width=60, placeholder_text="SS")
        self.seconds_entry.grid(row=0, column=2, padx=5)

        # Preset Buttons
        self.preset_frame = ctk.CTkFrame(self)
        self.preset_frame.pack(pady=5)

        ctk.CTkButton(self.preset_frame, text="5 min", command=lambda: self.set_preset(5)).pack(side="left", padx=5)
        ctk.CTkButton(self.preset_frame, text="10 min", command=lambda: self.set_preset(10)).pack(side="left", padx=5)
        ctk.CTkButton(self.preset_frame, text="15 min", command=lambda: self.set_preset(15)).pack(side="left", padx=5)

        # Circular progress
        bg_color = self._apply_appearance_mode(self.cget("fg_color"))
        self.canvas = ctk.CTkCanvas(self, width=200, height=200, bg=bg_color, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.arc = None

        # Time Display
        self.time_label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 36))
        self.time_label.pack(pady=10)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ctk.CTkButton(self.button_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_timer, state="disabled")
        self.reset_button.grid(row=0, column=2, padx=5)

    def set_preset(self, minutes):
        self.hours_entry.delete(0, 'end')
        self.minutes_entry.delete(0, 'end')
        self.seconds_entry.delete(0, 'end')
        self.hours_entry.insert(0, "00")
        self.minutes_entry.insert(0, str(minutes).zfill(2))
        self.seconds_entry.insert(0, "00")

    def start_timer(self):
        if not self.running:
            try:
                hours = int(self.hours_entry.get() or 0)
                minutes = int(self.minutes_entry.get() or 0)
                seconds = int(self.seconds_entry.get() or 0)
                self.time_left = hours * 3600 + minutes * 60 + seconds
                self.total_time = self.time_left
                if self.time_left <= 0:
                    self.time_label.configure(text="Invalid Time")
                    return
            except ValueError:
                self.time_label.configure(text="Invalid Input")
                return

            self.running = True
            self.update_buttons(start=False, pause=True, reset=True)
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()
            self.update_progress()


            

    def run_timer(self):
        while self.time_left > 0 and self.running:
            mins, secs = divmod(self.time_left, 60)
            hrs, mins = divmod(mins, 60)
            time_str = f"{hrs:02}:{mins:02}:{secs:02}"
            self.time_label.configure(text=time_str)
            time.sleep(1)
            self.time_left -= 1

        if self.time_left <= 0 and self.running:
            self.running = False
            self.time_label.configure(text="Time's Up!")
            self.update_buttons(start=True, pause=False, reset=True)
            self.play_beep()

    def update_progress(self):
        if not self.running:
            return
        self.canvas.delete("arc")
        if self.total_time == 0:
            return
        angle = (self.time_left / self.total_time) * 360
        self.canvas.create_oval(20, 20, 180, 180, outline="#444", width=6)
        self.canvas.create_arc(20, 20, 180, 180, start=90, extent=-angle, style="arc", outline="#00ff88", width=8, tag="arc")
        self.after(500, self.update_progress)

    def pause_timer(self):
        self.running = False
        self.update_buttons(start=True, pause=False, reset=True)

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.total_time = 0
        self.time_label.configure(text="00:00:00")
        self.canvas.delete("arc")
        self.update_buttons(start=True, pause=False, reset=False)

    def update_buttons(self, start, pause, reset):
        self.start_button.configure(state="normal" if start else "disabled")
        self.pause_button.configure(state="normal" if pause else "disabled")
        self.reset_button.configure(state="normal" if reset else "disabled")

    def play_beep(self):
        try:
            pygame.mixer.Sound(self.beep_file).play()
        except:
            print("Beep sound not found or failed to play.")
