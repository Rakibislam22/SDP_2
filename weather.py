import customtkinter as ctk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
import threading
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("W_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.city_entry = ctk.CTkEntry(self, placeholder_text="Enter city", width=200)
        self.city_entry.pack(pady=10)

        self.search_btn = ctk.CTkButton(self, text="Search", command=self.start_weather_thread)
        self.search_btn.pack(pady=5)

        self.location_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.location_label.pack(pady=2)

        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=2)

        self.temp_label = ctk.CTkLabel(self, text="", font=("Arial", 42, "bold"))
        self.temp_label.pack(pady=0)

        self.desc_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.desc_label.pack(pady=2)

        self.humidity_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.humidity_label.pack(pady=2)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="red")
        self.result_label.pack(pady=5)

    def start_weather_thread(self):
        threading.Thread(target=self.get_weather, daemon=True).start()

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.result_label.configure(text="❗ Enter a city name")
            return

        try:
            url = f"{BASE_URL}?appid={API_KEY}&q={city}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                location = data["name"]
                desc = data["weather"][0]["description"].title()
                icon_code = data["weather"][0]["icon"]
                temp = round(data["main"]["temp"] - 273.15, 1)
                humidity = data["main"]["humidity"]

                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
                img_data = requests.get(icon_url).content
                img = Image.open(BytesIO(img_data))
                img = img.resize((90, 90), Image.LANCZOS)
                weather_icon = ImageTk.PhotoImage(img)

                # Update UI on main thread using `after`
                self.after(0, self.update_ui, location, temp, desc, humidity, weather_icon)
            else:
                error_msg = response.json().get("message", "Unknown error.")
                self.after(0, lambda: self.result_label.configure(text="❗ " + error_msg))
        except Exception as e:
            self.after(0, lambda: self.result_label.configure(text=f"❗ Error: {e}"))

    def update_ui(self, location, temp, desc, humidity, weather_icon):
        self.location_label.configure(text=f"📍 {location}")
        self.temp_label.configure(text=f"{temp}°", font=("Arial", 44, "bold"))
        self.desc_label.configure(text=desc)
        self.humidity_label.configure(text=f"Humidity: {humidity}%")
        self.icon_label.configure(image=weather_icon)
        self.icon_label.image = weather_icon
        self.result_label.configure(text="")
