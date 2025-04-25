import customtkinter
import time
from datetime import datetime
from playsound import playsound

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class WelcomePage(customtkinter.CTkFrame):
    def __init__(self, master, on_finish_callback):
        super().__init__(master)
        self.master = master
        self.on_finish_callback = on_finish_callback
        self.configure(fg_color="transparent")
        
        self.text = "Welcome to ChronoMate.."
        self.label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont("Courier New", 35, "bold"))
        self.label.pack(pady=50)

        


        self.dev_label = customtkinter.CTkLabel(self, text="Developed by Team ChronoMate", font=customtkinter.CTkFont("Helvetica", 20), text_color="gray")
        self.dev_label.pack(pady=(10, 40))

        self.skip_button = customtkinter.CTkButton(self, text="Click for Skip or Wait..5", command=self.skip, fg_color="#333", hover_color="#555")
        self.skip_button.pack(pady=(50))
        
        self.progressbar_1 = customtkinter.CTkProgressBar(self)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(0.0)  # Start empty
        self.progressbar_1.pack(pady=(10, 10), padx=20, fill="x")

        self.char_index = 0
        self.animate_text()

        # Schedule countdown and skip button update after 5 seconds
        self.after(1000, self.start_countdown)  # Start countdown 1 second after initialization
        self.after(5000, self.skip)  # Automatically skip after 5 seconds
        


    def start_countdown(self):
        # Countdown from 5 to 1 with a pause of 1 second each
        self.countdown_value = 5
        self.update_button_text(self.countdown_value)  # Initialize the button text
        self.decrement_countdown()

    def decrement_countdown(self):
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.update_button_text(self.countdown_value)
            self.progressbar_1.set((5 - self.countdown_value) / 4)  # Fill from 0.0 to 1.0
            self.after(1000, self.decrement_countdown)

    def update_button_text(self, i):
        # Update the button text
        self.skip_button.configure(text=f"Click for Skip or Wait..{i}")
               
        

    def animate_text(self):
        if self.char_index <= len(self.text):
            self.label.configure(text=self.text[:self.char_index])
            self.char_index += 1
            self.after(90, self.animate_text)

    def skip(self):
        self.pack_forget()
        self.on_finish_callback()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ChronoMate")
        self.geometry("1100x580")
        self.show_welcome()
        

        Water_mark = customtkinter.CTkLabel(self, text="© rakibislam22", font=("Calibri", 15), corner_radius=0, width=1, height=1, fg_color="transparent", bg_color="transparent", text_color="#9e9e9e", )
        Water_mark.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        

    def show_welcome(self):
        self.welcome = WelcomePage(self, self.start_main_app)
        self.welcome.pack(fill="both", expand=True)

    def start_main_app(self):
        self.welcome.destroy()
        self.load_main_ui()
        self.update_time()

    #def show_welcome(self):
    #    self.welcome_frame = WelcomePage(self, self.load_main_ui)

    def load_main_ui(self):
        self.welcome.destroy()

        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=2)
        self.grid_rowconfigure(2, weight=0, minsize=26)
        self.grid_columnconfigure(2, weight=0, minsize=13)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Clock Mode", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self.sidebar_frame, text="24 Hours", font=customtkinter.CTkFont(size=15, weight="bold"), command=self.update_time, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.container = customtkinter.CTkFrame(self, width=150, height=60)
        self.container.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.time_frame = customtkinter.CTkFrame(self.container, fg_color="transparent", width=150, height=60)
        self.time_frame.pack(pady=(10, 0))

        self.time_label = customtkinter.CTkLabel(self.time_frame, font=customtkinter.CTkFont("Helvetica", 60), text="--:--")
        self.time_label.grid(row=0, column=0)

        self.pam_label = customtkinter.CTkLabel(self.time_frame, font=customtkinter.CTkFont("Helvetica", 25), text="--")
        self.pam_label.grid(row=0, column=1, padx=(10, 0))

        self.date_label = customtkinter.CTkLabel(self.container, font=customtkinter.CTkFont("Helvetica", 20, "bold"), text="Loading...")
        self.date_label.pack(pady=(8, 0))

        self.tabview1 = customtkinter.CTkTabview(self, width=250)
        self.tabview1.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # Adding tabs
        self.tabview1.add("Alarm")
        self.tabview1.add("World Clock")
        self.tabview1.add("Stopwatch")
        self.tabview1.add("Timer")
        
        # Access the "Alarm" tab and configure it for center alignment
        alarm_tab = self.tabview1.tab("Alarm")
        alarm_tab.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
        alarm_tab.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand

        # The AlarmPage should be placed inside the "Alarm" tab's content area
        self.alarm_page = AlarmPage(alarm_tab, on_finish_callback=self.on_alarm_triggered)

        self.tabview1.set("Alarm")  # Set the "Alarm" tab as active
        
        # Now center the AlarmPage inside the tab
        self.alarm_page.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        

        #self.tabview = customtkinter.CTkTabview(self, width=250)
        #self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.tabview.add("CTkTabview")
        #self.tabview.add("Tab 2")
        #self.tabview.add("Tab 3")
        #self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
        #self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        #self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"])
        #self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        #self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"), values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog", command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        #self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        #self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        #self.optionmenu_1.set("CTkOptionmenu")
        #elf.combobox_1.set("CTkComboBox")

        self.update_time()


    def on_alarm_triggered(self):
            print("Alarm Triggered! You can switch to the home screen or perform other actions.")
            # Add any other functionality here, such as switching frames, showing notifications, etc.

    def update_time(self):
        if self.switch_var.get() == "on":
            self.current_time = time.strftime('%H:%M')
            self.time_label.configure(text=self.current_time)
            self.pam_label.grid_remove()
        else:
            self.current_time = time.strftime('%I:%M')
            self.m = time.strftime('%p')
            self.time_label.configure(text=self.current_time)
            self.pam_label.configure(text=self.m)
            self.pam_label.grid()

        self.current_date = datetime.now().strftime('%a, %d %B')
        self.date_label.configure(text=self.current_date)

        self.after(1000, self.update_time)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


class AlarmPage(customtkinter.CTkFrame):
    def __init__(self, master, on_finish_callback):
        super().__init__(master)
        self.master = master
        self.on_finish_callback = on_finish_callback
        
        self.configure(fg_color="transparent")
        
        
        # Label to show alarm time
        self.alarm_time_label = customtkinter.CTkLabel(self, text="Set Alarm Time", font=customtkinter.CTkFont("Arial", 18))
        self.alarm_time_label.pack(pady=20)
        
        # Time entry for setting the alarm
        self.alarm_time_entry = customtkinter.CTkEntry(self, placeholder_text="Enter time (HH:MM:SS)")
        self.alarm_time_entry.pack(pady=10)
        
        # Button to set alarm
        self.set_alarm_button = customtkinter.CTkButton(self, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)
        
        # Label for selecting custom sound
        self.sound_label = customtkinter.CTkLabel(self, text="Choose Alarm Sound", font=customtkinter.CTkFont("Arial", 18))
        self.sound_label.pack(pady=20)

        # Button to open file dialog to choose sound
        self.choose_sound_button = customtkinter.CTkButton(self, text="Choose Sound", command=self.choose_sound)
        self.choose_sound_button.pack(pady=10)

        self.selected_sound = None  # Holds the path to the selected sound file
        
        self.alarm_time = None  # Will hold the set alarm time

    def set_alarm(self):
        # Get the alarm time entered by the user
        alarm_time_str = self.alarm_time_entry.get()
        self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M:%S").time()

        # Print the set alarm time (just for checking)
        print(f"Alarm set for: {self.alarm_time}")

        # Check if alarm time has passed, and if it does, trigger the alarm
        self.check_alarm()

    def choose_sound(self):
        # Open file dialog to let user select a sound
        from tkinter.filedialog import askopenfilename
        file_path = askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.selected_sound = file_path
            print(f"Selected sound: {self.selected_sound}")
            
    def check_alarm(self):
        # Continuously check if the current time matches the alarm time
        current_time = datetime.now().time()
        
        if current_time >= self.alarm_time:
            print("Time to trigger the alarm!")
            self.trigger_alarm()
        else:
            # Re-check in 1 second
            self.after(1000, self.check_alarm)

    def trigger_alarm(self):
        if self.selected_sound:
            # Play the selected sound (if one is chosen)
            print("Playing alarm sound...")
            playsound(self.selected_sound)  # For simpler sounds
            # Alternatively, use pygame for advanced controls:
            # pygame.mixer.init()
            # pygame.mixer.music.load(self.selected_sound)
            # pygame.mixer.music.play()
        else:
            print("No sound selected.")
        
        # Call the callback function (e.g., to switch screens, show message, etc.)
        self.on_finish_callback()  # This calls the function from the main file (on_alarm_triggered)


if __name__ == "__main__":
    app = App()
    app.mainloop()
