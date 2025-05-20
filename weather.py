import customtkinter as ctk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("W_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Live Weather")
app.geometry("350x450")

def get_weather():
    city = city_entry.get().strip()
    if not city:
        result_label.configure(text="❗ Enter a city name")
        return

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
        img = Image.open(BytesIO(requests.get(icon_url).content))
        img = img.resize((90, 90), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(img)

        location_label.configure(text=f"📍 {location}")
        temp_label.configure(text=f"{temp}°", font=("Arial", 44, "bold"))
        desc_label.configure(text=desc)
        humidity_label.configure(text=f"Humidity: {humidity}%")
        icon_label.configure(image=weather_icon)
        icon_label.image = weather_icon

        result_label.configure(text="")  # Clear errors
    else:
        result_label.configure(text="❗ " + response.json().get("message", "Unknown error."))

# UI Elements
city_entry = ctk.CTkEntry(app, placeholder_text="Enter city", width=200)
city_entry.pack(pady=20)

search_btn = ctk.CTkButton(app, text="Search", command=get_weather)
search_btn.pack(pady=10)

location_label = ctk.CTkLabel(app, text="", font=("Arial", 18))
location_label.pack(pady=5)

icon_label = ctk.CTkLabel(app, text="")
icon_label.pack(pady=5)

temp_label = ctk.CTkLabel(app, text="", font=("Arial", 42, "bold"))
temp_label.pack(pady=0)

desc_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
desc_label.pack(pady=2)

humidity_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
humidity_label.pack(pady=2)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="red")
result_label.pack(pady=10)

app.mainloop()
