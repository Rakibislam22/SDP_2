import customtkinter as ctk

class ChronoMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChronoMate")

        # Initialize frames for different modes
        self.stopwatch_frame = ctk.CTkFrame(self.root)
        self.timer_frame = ctk.CTkFrame(self.root)
        self.world_clock_frame = ctk.CTkFrame(self.root)
        self.alarm_frame = ctk.CTkFrame(self.root)

        # Mode options
        self.mode_options = ["Stopwatch", "Timer", "World Clock", "Alarm"]

        # Dropdown menu for selecting modes
        self.mode_var = ctk.StringVar(value=self.mode_options[0])  # Default value is "Stopwatch"
        self.mode_dropdown = ctk.CTkOptionMenu(self.root, variable=self.mode_var, values=self.mode_options, command=self.change_mode)
        self.mode_dropdown.grid(row=0, column=0, padx=10, pady=10)

        # Initially show the stopwatch
        self.show_stopwatch()

    def change_mode(self, selected_mode):
        if selected_mode == "Stopwatch":
            self.show_stopwatch()
        elif selected_mode == "Timer":
            self.show_timer()
        elif selected_mode == "World Clock":
            self.show_world_clock()
        elif selected_mode == "Alarm":
            self.show_alarm()

    def show_stopwatch(self):
        self.clear_frames()
        # Add your stopwatch widgets here
        stopwatch_label = ctk.CTkLabel(self.stopwatch_frame, text="Stopwatch Mode")
        stopwatch_label.grid(row=0, column=0)
        self.stopwatch_frame.grid(row=1, column=0, padx=10, pady=10)

    def show_timer(self):
        self.clear_frames()
        # Add your timer widgets here
        timer_label = ctk.CTkLabel(self.timer_frame, text="Timer Mode")
        timer_label.grid(row=0, column=0)
        self.timer_frame.grid(row=1, column=0, padx=10, pady=10)

    def show_world_clock(self):
        self.clear_frames()
        # Add your world clock widgets here
        world_clock_label = ctk.CTkLabel(self.world_clock_frame, text="World Clock Mode")
        world_clock_label.grid(row=0, column=0)
        self.world_clock_frame.grid(row=1, column=0, padx=10, pady=10)

    def show_alarm(self):
        self.clear_frames()
        # Add your alarm widgets here
        alarm_label = ctk.CTkLabel(self.alarm_frame, text="Alarm Mode")
        alarm_label.grid(row=0, column=0)
        self.alarm_frame.grid(row=1, column=0, padx=10, pady=10)

    def clear_frames(self):
        # Hide all frames
        self.stopwatch_frame.grid_forget()
        self.timer_frame.grid_forget()
        self.world_clock_frame.grid_forget()
        self.alarm_frame.grid_forget()


if __name__ == "__main__":
    root = ctk.CTk()
    app = ChronoMateApp(root)
    root.mainloop()
