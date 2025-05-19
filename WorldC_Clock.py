import customtkinter as ctk
from datetime import datetime
import pytz

class TimezoneConverter(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.label_title = ctk.CTkLabel(self, text="Timezone", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=20)

        # Entry for continent
        self.entry_continent = ctk.CTkEntry(self, placeholder_text="Enter Continent (e.g. Asia)",width=250)
        self.entry_continent.pack(pady=5)

        # Entry for region/capital
        self.entry_region = ctk.CTkEntry(self, placeholder_text="Enter Region or Capital (e.g. Dhaka)",width=250)
        self.entry_region.pack(pady=5)

        # Button to fetch time
        self.btn_get_time = ctk.CTkButton(self, text="Get Time", command=self.display_time)
        self.btn_get_time.pack(pady=10)

        # Output label
        self.label_output = ctk.CTkLabel(self, text="", font=("Arial", 24,"bold"))
        self.label_output.pack(pady=10)

    def get_time_in_timezone(self, timezone_str):
        try:
            timezone = pytz.timezone(timezone_str)
            time_now = datetime.now(timezone)
            return time_now.strftime("%a, %d %B %Y , %H:%M ")
        except Exception as e:
            return f"Invalid Timezone: {timezone_str}"

    def display_time(self):
        continent = self.entry_continent.get().capitalize()
        region = self.entry_region.get().capitalize()
        timezone_str = f"{continent}/{region}"
        time_str = self.get_time_in_timezone(timezone_str)
        self.label_output.configure(text=f"{region}\n\n {time_str}")

