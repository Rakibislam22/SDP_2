import customtkinter as ctk
import time
import threading

class StopwatchFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.running = False
        self.paused = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_count = 1
        self.last_lap_time = 0

        # Stopwatch display
        self.time_var = ctk.StringVar(value="00:00:00.00")
        self.time_label = ctk.CTkLabel(self, textvariable=self.time_var, font=("Segoe UI", 48, "bold"))
        self.time_label.pack(pady=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self,fg_color="transparent")
        btn_frame.pack(pady=10)

        self.main_button = ctk.CTkButton(btn_frame, text="Start", command=self.toggle_start_stop)
        self.main_button.grid(row=0, column=0, padx=10)

        self.secondary_button = ctk.CTkButton(btn_frame, text="Lap", command=self.lap_or_reset, state="disabled")
        self.secondary_button.grid(row=0, column=1, padx=10)

        # Styled lap list container
        lap_container = ctk.CTkFrame(self, corner_radius=10)
        lap_container.pack(pady=10, padx=20, fill="both", expand=False)

        self.lap_box = ctk.CTkTextbox(lap_container, height=180, width=420)
        self.lap_box.pack(padx=10, pady=10, fill="both")
        self.lap_box.configure(
            state="disabled",
            font=("Segoe UI", 18),
            wrap="none",
        )

    def toggle_start_stop(self):
        if not self.running and not self.paused:
            # Start
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.main_button.configure(text="Stop")
            self.secondary_button.configure(state="normal", text="Lap")
            threading.Thread(target=self.update_timer, daemon=True).start()

        elif self.running:
            # Stop
            self.running = False
            self.paused = True
            self.elapsed_time = time.time() - self.start_time
            self.main_button.configure(text="Resume")
            self.secondary_button.configure(text="Reset")

        elif self.paused:
            # Resume
            self.running = True
            self.paused = False
            self.start_time = time.time() - self.elapsed_time
            self.main_button.configure(text="Stop")
            self.secondary_button.configure(text="Lap")
            threading.Thread(target=self.update_timer, daemon=True).start()

    def lap_or_reset(self):
        if self.running:
            # Lap
            elapsed = time.time() - self.start_time
            lap_time = self.format_time(elapsed)

            # Calculate lap difference
            diff_seconds = elapsed - self.last_lap_time
            lap_diff = self.format_time(diff_seconds)
            self.last_lap_time = elapsed

            # Show both lap time and difference
            self.lap_box.configure(state="normal")
            if self.lap_count == 1:
                self.lap_box.insert("end", f"Lap {self.lap_count} : {lap_time}\n\n")
            else:
                self.lap_box.insert("end", f"Lap {self.lap_count} : {lap_time} (+{lap_diff})\n\n")

            self.lap_box.see("end")
            self.lap_box.configure(state="disabled")
            self.lap_count += 1

        elif self.paused:
            # Reset
            self.running = False
            self.paused = False
            self.start_time = 0
            self.elapsed_time = 0
            self.lap_count = 1
            self.last_lap_time = 0  # reset lap tracking
            self.time_var.set("00:00:00.00")
            self.main_button.configure(text="Start")
            self.secondary_button.configure(text="Lap", state="disabled")
            self.lap_box.configure(state="normal")
            self.lap_box.delete("1.0", "end")
            self.lap_box.configure(state="disabled")

    def update_timer(self):
        while self.running:
            self.elapsed_time = time.time() - self.start_time
            self.time_var.set(self.format_time(self.elapsed_time))
            time.sleep(0.01)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        millis = int((seconds % 1) * 100)
        return f"{int(hours):02}:{int(mins):02}:{int(secs):02}.{millis:02}"
