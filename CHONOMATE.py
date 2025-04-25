import customtkinter
import time
from datetime import datetime

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
            self.after(1000, self.decrement_countdown)  # Schedule next decrement in 1 second

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
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0), weight=1)

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
        self.time_frame.pack(pady=(20, 0))

        self.time_label = customtkinter.CTkLabel(self.time_frame, font=customtkinter.CTkFont("Helvetica", 60), text="--:--")
        self.time_label.grid(row=0, column=0)

        self.pam_label = customtkinter.CTkLabel(self.time_frame, font=customtkinter.CTkFont("Helvetica", 25), text="--")
        self.pam_label.grid(row=0, column=1, padx=(10, 0))

        self.date_label = customtkinter.CTkLabel(self.container, font=customtkinter.CTkFont("Helvetica", 20, "bold"), text="Loading...")
        self.date_label.pack(pady=(10, 0))

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"), values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog", command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")

        self.update_time()

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
