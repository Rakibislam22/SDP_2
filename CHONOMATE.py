import customtkinter
import time
import requests
from datetime import datetime, timedelta
from CTkScrollableDropdown import CTkScrollableDropdown
from pathlib import Path
from playsound import playsound
from alif_calculator import MultiUtilityApp
from music import MusicPlayer
from PIL import Image,ImageTk
from io import BytesIO
import threading
import os
from dotenv import load_dotenv
load_dotenv()


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class WelcomePage(customtkinter.CTkFrame):
    def __init__(self, master, on_finish_callback):
        super().__init__(master)
        self.master = master
        self.on_finish_callback = on_finish_callback
        self.configure(fg_color="transparent")
        
        self.text = "Welcome to ChronoMate.."
        self.label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont("Courier New", 35, "bold"))
        self.label.pack(pady=80)

        


        self.dev_label = customtkinter.CTkLabel(self, text="Developed by Team ChronoMate", font=customtkinter.CTkFont("Helvetica", 20), text_color="gray")
        self.dev_label.pack(pady=(50, 40))

        self.skip_button = customtkinter.CTkButton(self, text="Click for Skip or Wait..5", command=self.skip, fg_color="#333", hover_color="#555")
        self.skip_button.pack(pady=(70))
        
        self.progressbar_1 = customtkinter.CTkProgressBar(self)
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(0.0)  # Start empty
        self.progressbar_1.pack(pady=(70, 10), padx=20, fill="x")

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
        self.geometry("1100x900")
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

    def animate_slide_in(self):
        self.side_panel.lift()  # Bring to front
        width = self.side_panel.winfo_width()
        start_x = self.winfo_width()
        end_x = self.winfo_width() - width - 10  # Final position

        def slide():
            nonlocal start_x
            if start_x > end_x:
                start_x -= 5
                self.side_panel.place(x=start_x, y=180)
                self.after(10, slide)
            else:
                self.side_panel.place(x=end_x, y=180)

        slide()


    def animate_slide_out(self):
        width = self.side_panel.winfo_width()
        start_x = self.side_panel.winfo_x()
        end_x = self.winfo_width()

        def slide():
            nonlocal start_x
            if start_x < end_x:
                start_x += 5
                self.side_panel.place(x=start_x, y=180)
                self.after(10, slide)
            else:
                self.side_panel.place_forget()

        slide()


    def load_main_ui(self):
        self.welcome.destroy()

        self.grid_columnconfigure(1, weight=1) 
        #self.grid_columnconfigure((2), weight=0)
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure((1), weight=2)
        self.grid_rowconfigure(2, weight=0, minsize=32)
        self.grid_columnconfigure(2, weight=0, minsize=5)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Clock Mode", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self.sidebar_frame, text="24 Hours", font=customtkinter.CTkFont(size=15, weight="bold"), command=self.update_time, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=3, column=0, padx=20, pady=10)

        self.top_bar_frame = customtkinter.CTkFrame(self)
        self.top_bar_frame.grid(row=0, column=1, columnspan=2, padx=5, sticky="news")

        self.center_wrapper = customtkinter.CTkFrame(self.top_bar_frame, fg_color="transparent")
        self.center_wrapper.pack()

        self.clock_frame = customtkinter.CTkFrame(self.center_wrapper, fg_color="transparent")
        self.clock_frame.grid(row=0, column=0, padx=50, sticky="e")

        self.weather_frame = customtkinter.CTkFrame(self.center_wrapper, fg_color="transparent")
        self.weather_frame.grid(row=0, column=1, padx=50, sticky="w")


        self.time_label = customtkinter.CTkLabel(
            self.top_bar_frame,
            font=customtkinter.CTkFont("Segoe UI", 60, weight="bold"),
            text="--:--"
        )
        self.time_label.place(x=230, y=35)

        self.pam_label = customtkinter.CTkLabel(
            self.top_bar_frame,
            font=customtkinter.CTkFont("Helvetica", 25),
            text="--",
        )
        self.pam_label.place(x=400, y=65)

        self.date_label = customtkinter.CTkLabel(self.top_bar_frame, font=customtkinter.CTkFont("Helvetica", 22, "bold"), text="Loading...")
        self.date_label.place(x=250, y=125)

        self.update_time()

        

        # Weather Data Variables
        self.city_var = customtkinter.StringVar(value="📍 Loading...")
        self.temp_var = customtkinter.StringVar(value="--° C")
        self.desc_var = customtkinter.StringVar(value="--")
        self.humidity_var = customtkinter.StringVar(value="Humidity: --%")

        # Weather Frame Grid Configuration
        self.weather_frame.grid_columnconfigure(0, weight=1)
        self.weather_frame.grid_columnconfigure(1, weight=1)

        # City Name (centered)
        self.city_label = customtkinter.CTkLabel(
            self.weather_frame, 
            textvariable=self.city_var, 
            font=customtkinter.CTkFont(size=20)
        )
        self.city_label.grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="n")

        # Weather Icon (left) + Temperature (right)
        self.icon_label = customtkinter.CTkLabel(self.weather_frame, text="")
        self.icon_label.grid(row=1, column=0, padx=(10, 5), sticky="e")

        self.temp_label = customtkinter.CTkLabel(
            self.weather_frame, 
            textvariable=self.temp_var, 
            font=customtkinter.CTkFont(size=38, weight="bold")
        )
        self.temp_label.grid(row=1, column=1, padx=(5, 10), sticky="w")

        # Description (centered)
        self.desc_label = customtkinter.CTkLabel(
            self.weather_frame, 
            textvariable=self.desc_var, 
            font=customtkinter.CTkFont(size=15)
        )
        self.desc_label.grid(row=2, column=0, columnspan=2, pady=(5, 0))

        # Humidity (centered)
        self.humidity_label = customtkinter.CTkLabel(
            self.weather_frame, 
            textvariable=self.humidity_var, 
            font=customtkinter.CTkFont(size=15)
        )
        self.humidity_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        #self.load_weather_data("Dhaka")
        # ✅ Only now call auto_update_weather
        self.auto_update_weather()

        self.tab_n = ["Alarm", "World Clock", "Weather", "Stopwatch", "Timer"]

        # Load images
        self.drive = Path(__file__).resolve().parent
        img_paths = ["alarm.png", "wc.png", "wea.png", "stop.png", "timer.png"]
        self.icons = [
            customtkinter.CTkImage(light_image=Image.open(self.drive / "image" / path), size=(40, 40))
            for path in img_paths
        ]

        # Create tabview
        self.tabview1 = customtkinter.CTkTabview(self, width=500, height=650)
        self.tabview1.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.arrow_button = customtkinter.CTkButton(self, text="<<", width=40, command=self.toggle_side_panel)
        #self.arrow_button.grid(row=0, column=1, pady=(10, 0))
        self.arrow_button.place(x=self.winfo_width()-55, y=self.winfo_height()-790) 

        # Side panel (initially hidden)
        self.side_panel = customtkinter.CTkFrame(
            self,
            width=300,
            corner_radius=10,
            #fg_color="transparent",  # or match parent with self.main_frame.cget("fg_color")
            border_width=2,
            border_color="#53947c"  # Light gray border for visibility in light mode
        )
        #self.side_panel.grid(row=1, column=2, padx=(10, 10), pady=(20, 0), sticky="nsew")
        #self.side_panel = customtkinter.CTkFrame(self, width=200, height=650)
        self.side_panel.place(x=self.winfo_width(), y=self.winfo_height()-800)
        #self.side_panel.grid_remove()  # Hide it initially
        
        #self.side_panel_label = customtkinter.CTkLabel(self.side_panel, text="Side Panel", font=("Helvetica", 20))
        #self.side_panel_label.pack(pady=20)

        img_path = Path(__file__).resolve().parent / "image" / "cal.png"
        self.image = customtkinter.CTkImage(light_image=Image.open(img_path), size=(60, 60))

        img_path2 = Path(__file__).resolve().parent / "image" / "music.png"
        self.image2 = customtkinter.CTkImage(light_image=Image.open(img_path2), size=(60, 60))

        # Button to launch lonch_cal_btn function
        self.image_button = customtkinter.CTkButton(
        self.side_panel,
        image=self.image,
        text="",
        command=self.lonch_cal_btn,
        width=30,
        height=40,
        fg_color="transparent",
        hover_color="#888fba"
        )
        self.image_button.pack(padx=5,pady=5)

        self.image_button2 = customtkinter.CTkButton(
        self.side_panel,
        image=self.image2,
        text="",
        command=self.lonch_music_btn,
        width=30,
        height=40,
        fg_color="transparent",
        hover_color="#888fba"
        )
        self.image_button2.pack(padx=5,pady=5)

        self.side_panel_open = False
        global b 
        b = False


        # Add tabs
        for tab in self.tab_n:
            self.tabview1.add(tab)

        self.tabview1.set("Alarm")  # Default active

        # Setup AlarmPage (repeat for other pages similarly)
        alarm_tab = self.tabview1.tab("Alarm")
        alarm_tab.grid_rowconfigure(0, weight=1)
        alarm_tab.grid_rowconfigure(2, weight=1)
        alarm_tab.grid_columnconfigure(0, weight=1)
        alarm_tab.grid_columnconfigure(2, weight=1)
        self.alarm_page = AlarmPage(alarm_tab, on_finish_callback=self.on_alarm_triggered)
        self.alarm_page.grid(row=0, column=1)

        # Access tab buttons
        self.tab_buttons = self.tabview1._segmented_button._buttons_dict

        # Initial setup of buttons
        for i, (name, btn) in enumerate(self.tab_buttons.items()):
            btn.configure(text="", image=self.icons[i], bg_color="transparent", font=("Helvetica", 14), border_width=2, border_spacing=4)

        # Show label only for the first tab
        for i, (name, btn) in enumerate(self.tab_buttons.items()):
            if i == 0:
                btn.configure(text=self.tab_n[i])
            else:
                btn.configure(text="")

        # Add command to each button
        for i, btn in enumerate(self.tab_buttons.values()):
            btn.configure(command=lambda tab_index=i: self.update_tabs(tab_index))
        

        self.appearance_mode_optionemenu.set("Dark")
        self.mode=customtkinter.get_appearance_mode()
    

    def load_weather_data(self, city="Dhaka"):
        API_KEY = os.getenv("G_API_KEY")  # Ensure this environment variable is set
        url = f"http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={city}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.city_var.set(f"📍 {data['name']}")
                self.temp_var.set(f"{round(data['main']['temp'] - 273.15, 1)}° C")
                self.desc_var.set(data["weather"][0]["description"].title())
                self.humidity_var.set(f"Humidity: {data['main']['humidity']}%")

                # Correct way: use CTkImage
                icon_code = data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                img_data = requests.get(icon_url).content
                img = Image.open(BytesIO(img_data)).resize((50, 50))  # make it more visible

                ctk_img = customtkinter.CTkImage(light_image=img, dark_image=img, size=(50, 50))
                self.icon_label.configure(image=ctk_img, text="")  # text="" removes unwanted label text
                self.icon_label.image = ctk_img  # Keep reference to prevent garbage collection

            else:
                self.city_var.set("❌ Load error")
                self.temp_var.set("--° C")

        except Exception as e:
            self.city_var.set("❌ Network error")
            print(f"[Weather Error] {e}")


    def auto_update_weather(self):
        self.load_weather_data("Dhaka")  # or dynamic city later
        self.after(600000, self.auto_update_weather)  # every 10 minutes



    def lonch_cal_btn(self):
        global a
        global b
        if hasattr(self, 'top2') and self.top2.winfo_exists():
            self.top2.destroy()
        if hasattr(self, 'top') and self.top.winfo_exists():
            self.top.destroy()
        self.toggle_side_panel()

        mode = (customtkinter.get_appearance_mode()).lower()
        self.top = customtkinter.CTkFrame(self)
        #top.title("Calculator")
        #top.geometry("400x600")  # Optional: Set size
        self.top.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        back = customtkinter.CTkButton(self.top, text="X",fg_color="red",corner_radius=15, width=4, height=12, command=lambda:self.top.destroy())
        back.pack(anchor="e",padx=20,pady=20)

        a = MultiUtilityApp(self.top)
        a.change_mode(mode)

    def lonch_music_btn(self):
        
        if hasattr(self, 'top') and self.top.winfo_exists():
            self.top.destroy()
        if hasattr(self, 'top2') and self.top2.winfo_exists():
            self.top2.destroy()
        self.toggle_side_panel()

        self.top2 = customtkinter.CTkFrame(self,width=400,height=500)
        #top.title("Calculator")
        #top.geometry("400x600")  # Optional: Set size
        self.top2.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        back = customtkinter.CTkButton(self.top2, text="X",fg_color="red",corner_radius=15, width=4, height=12, command=lambda:self.top2.destroy())
        back.pack(anchor="e",padx=20,pady=20)

        a = MusicPlayer(self.top2)


        
        

    # def toggle_side_panel(self):
    #     if self.side_panel_open:
    #         self.side_panel.grid_remove()
    #         self.arrow_button.configure(text="<<")  # Pointing right
    #     else:
    #         self.side_panel.grid()
    #         self.arrow_button.configure(text=">>")  # Pointing left⬅⇾
    #     self.side_panel_open = not self.side_panel_open

    def toggle_side_panel(self):
        if self.side_panel_open:
            self.animate_slide_out()
            self.arrow_button.configure(text="<<")
        else:
            self.animate_slide_in()
            self.arrow_button.configure(text=">>")

        self.side_panel_open = not self.side_panel_open


    def update_tabs(self, s_tab):
        self.tabview1.set(self.tab_n[s_tab])

        for i, (name, btn) in enumerate(self.tab_buttons.items()):
            if i == s_tab:
                btn.configure(text=self.tab_n[i], image=self.icons[i])
            else:
                btn.configure(text="", image=self.icons[i])

        


    def on_alarm_triggered(self):
            print("Alarm Triggered! You can switch to the home screen or perform other actions.")
            # Add any other functionality here, such as switching frames, showing notifications, etc.

    def update_time(self):
        if self.switch_var.get() == "on":
            self.current_time = time.strftime('%H:%M')
            self.time_label.configure(text=self.current_time)
            self.pam_label.configure(text="")
        else:
            self.current_time = time.strftime('%I:%M')
            self.m = time.strftime('%p')
            self.time_label.configure(text=self.current_time)
            self.pam_label.configure(text=self.m)

        self.current_date = datetime.now().strftime('%a, %d %B')
        self.date_label.configure(text=self.current_date)

        self.after(1000, self.update_time)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        global a

        if hasattr(self, 'top') and self.top.winfo_exists() :
            m = (new_appearance_mode).lower()
            a.change_mode(m)
            self.arrow_button.place(x=self.winfo_width()-55, y=self.winfo_height()-720)
            self.side_panel.place(x=self.winfo_width(), y=self.winfo_height()-800)
        else: 
            pass
        customtkinter.set_appearance_mode(new_appearance_mode)

        
         
        
        

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        if self.side_panel_open:
            #self.side_panel.grid()
            pass
        else:
            pass
            #self.side_panel.grid_remove()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


class AlarmPage(customtkinter.CTkFrame):
    def __init__(self, master, on_finish_callback):
        super().__init__(master)
        self.master = master
        self.on_finish_callback = on_finish_callback

        self.configure(fg_color="transparent")

        self.alarm_time_label = customtkinter.CTkLabel(self, text="Hours", font=customtkinter.CTkFont("Arial", 18))
        self.alarm_time_label.grid(row=0,column=0)
        self.alarm_time_label = customtkinter.CTkLabel(self, text="Minutes", font=customtkinter.CTkFont("Arial", 18))
        self.alarm_time_label.grid(row=0,column=1)
        self.alarm_time_label = customtkinter.CTkLabel(self, text="Seconds", font=customtkinter.CTkFont("Arial", 18))
        self.alarm_time_label.grid(row=0,column=2)

        #self.scrollable_frame1 = customtkinter.CTkScrollableFrame(self)
        #self.scrollable_frame1.grid(row=1, column=0, padx=5,pady=10)

        hour= [f"{i:02}" for i in range(1, 13)]
        minute = [f"{i:02}" for i in range(60)]
        second = [f"{i:02}" for i in range(60)]

        self.hour_cb = customtkinter.CTkComboBox(self, values=hour,justify='center')
        self.minute_cb = customtkinter.CTkComboBox(self, values=minute,justify='center')
        self.second_cb = customtkinter.CTkComboBox(self, values=second,justify='center')
        self.period_cb = customtkinter.CTkComboBox(self, values=["AM", "PM"],justify='center',)

        CTkScrollableDropdown(self.hour_cb, values=hour)
        CTkScrollableDropdown(self.minute_cb, values=minute)
        CTkScrollableDropdown(self.second_cb, values=second)

        self.hour_cb.grid(row=1, column=0, padx=5, pady=2)
        self.minute_cb.grid(row=1, column=1, padx=5, pady=2)
        self.second_cb.grid(row=1, column=2, padx=5, pady=2)
        self.period_cb.grid(row=1, column=3, padx=5, pady=2)

        self.activate_switch = customtkinter.CTkSwitch(self, text="Activate", command=self.set_alarm)
        self.activate_switch.grid(row=2, column=1, pady=10)

        self.sound_label = customtkinter.CTkLabel(self, text="Choose Alarm Sound", font=customtkinter.CTkFont("Arial", 18))
        self.sound_label.grid(row=3, column=1, pady=(20, 5))

        self.choose_sound_button = customtkinter.CTkButton(self, text="Choose Sound", command=self.choose_sound)
        self.choose_sound_button.grid(row=4, column=1, pady=10)

        self.selected_sound = None
        self.alarm_time = None
        self.alarm_active = False  # NEW: Flag to know alarm is ringing

        # Snooze and Stop buttons
        self.snooze_button = customtkinter.CTkButton(self, text="Snooze", command=self.snooze_alarm, state="disabled")
        self.stop_button = customtkinter.CTkButton(self, text="Stop", command=self.stop_alarm, state="disabled")
        self.snooze_button.grid(row=5, column=0, pady=20)
        self.stop_button.grid(row=5, column=2, pady=20)

    def set_alarm(self):
        hour = int(self.hour_cb.get())
        minute = int(self.minute_cb.get())
        second = int(self.second_cb.get())
        period = self.period_cb.get()

        if period == "PM" and hour != 12:
            hour += 12
        if period == "AM" and hour == 12:
            hour = 0

        self.alarm_time = datetime.now().replace(hour=hour, minute=minute, second=second, microsecond=0).time()
        print(f"Alarm set for: {self.alarm_time}")
        self.alarm_active = True
        self.check_alarm()

    def choose_sound(self):
        from tkinter.filedialog import askopenfilename
        file_path = askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.selected_sound = file_path
            print(f"Selected sound: {self.selected_sound}")

    def check_alarm(self):
        if not self.alarm_active:
            return

        current_time = datetime.now().time()

        if current_time >= self.alarm_time:
            print("Time to trigger the alarm!")
            self.trigger_alarm()
        else:
            self.after(1000, self.check_alarm)

    def trigger_alarm(self):
        if self.selected_sound:
            print("Playing alarm sound...")
            threading.Thread(target=playsound, args=(self.selected_sound,), daemon=True).start()
        else:
            print("No sound selected.")

        # Enable snooze and stop buttons
        self.snooze_button.configure(state="normal")
        self.stop_button.configure(state="normal")

    def snooze_alarm(self):
        print("Snoozing alarm for 5 minutes...")
        snooze_time = (datetime.now() + timedelta(minutes=5)).time()
        self.alarm_time = snooze_time
        self.alarm_active = True
        self.snooze_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.check_alarm()

    def stop_alarm(self):
        print("Alarm stopped.")
        self.alarm_active = False
        self.snooze_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.on_finish_callback()


if __name__ == "__main__":
    app = App()
    app.mainloop()


#it's work properly!!
