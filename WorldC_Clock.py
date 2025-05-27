import customtkinter as ctk
from datetime import datetime
from CTkScrollableDropdown import CTkScrollableDropdown
import pytz

class TimezoneConverter(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Main container frame with fixed size
        self.main_frame = ctk.CTkFrame(self, width=400, height=400, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=20)
        self.main_frame.pack_propagate(False)  # Prevent shrinking to fit contents

        # Title Label
        self.label_title = ctk.CTkLabel(self.main_frame, text="Timezone", font=("Helvetica", 22, "bold"))
        self.label_title.pack(pady=(0, 30))

        # Entry Frame for input and button
        entry_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        entry_frame.pack(pady=5)

        self.region = pytz.all_timezones

        # Dropdown for regions
        self.entry_region = ctk.CTkLabel(entry_frame,text="Select Timezone :",font=ctk.CTkFont("Helvetica", 16))
        self.entry_region.pack(side="left", padx=5)
        self.entry_region = ctk.CTkEntry(entry_frame, width=170)
        self.entry_region.pack(side="left", padx=5)

        CTkScrollableDropdown(self.entry_region, values=self.region, command=lambda e: (self.entry_region.delete(0, 'end'), self.entry_region.insert(0, e)),
                      autocomplete=True)

        # Scrollable dropdown behavior
        CTkScrollableDropdown(self.entry_region, values=self.region)

        # Search Button
        self.btn_get_time = ctk.CTkButton(entry_frame, text="🔍", command=self.display_time, width=50)
        self.btn_get_time.pack(side="left", padx=5)

        # Output Label
        self.label_output = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 20, "bold"))
        self.label_output.pack(pady=(20, 0))

    def get_time_in_timezone(self, timezone_str):
        try:
            timezone = pytz.timezone(timezone_str)
            time_now = datetime.now(timezone)
            return time_now.strftime("%a, %d %B %Y , %H:%M")
        except Exception:
            return f"Invalid Timezone: {timezone_str}"

    def display_time(self):
        region = self.entry_region.get()
        time_str = self.get_time_in_timezone(region)
        self.label_output.configure(
            text=f"\n{region}\n\n{time_str}",
            text_color="red" if "Invalid" in time_str else "green"
        )
