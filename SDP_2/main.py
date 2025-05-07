from customtkinter import *
from currency_converter import *
from tkinter import *
from PIL import Image
from CTkScrollableDropdown import CTkScrollableDropdown
from tab import open_calculator

import google.generativeai as ai
import threading
import time
from chatbot import open_chatbot
from alif_calculator import MultiUtilityApp



set_appearance_mode("dark")
set_default_color_theme("blue")
mode="light"


def lonch_cal_btn():
    global mode, app_calculater
    cal_frame = CTkFrame(main_windo, width=400, height=500 )
    cal_frame.pack(side="top", expand=True, fill="both",)

    # call all constractor & change_mode function
    app_calculater = MultiUtilityApp(cal_frame)
    app_calculater.change_mode(mode)

    back = CTkButton(cal_frame, text="<-", font=("JetBrains Mono", 26, "bold"), width=40, height=40, command=lambda:cal_frame.destroy())
    back.pack(pady=20)

def lonch_chatbot_btn():
    chat_frame = CTkFrame(main_windo,  width=400, height=500 )
    chat_frame.pack(side="top", expand=True, fill="both",)
    open_chatbot(chat_frame)
    back = CTkButton(chat_frame, text="<-", font=("JetBrains Mono", 26, "bold"), width=40, height=40, command=lambda: chat_frame.destroy())
    back.pack(pady=20)

def change():
    global mode, app_calculater
    if mode == "dark":
        set_appearance_mode("dark")
        mode = "light"

        try:
            # call all constractor & change_mode function

            app_calculater.change_mode(mode)
        except:
            pass
        mode_change_btn.configure(text="🔆",
                                    text_color="black",
                                    fg_color="white",
                                    hover_color="gray")
    elif mode == "light":
        set_appearance_mode("light")
        mode = "dark"

        try:
            # call all constractor & change_mode function

            app_calculater.change_mode(mode)
        except:
            pass
        mode_change_btn.configure(text="🌙",
                                    text_color="white",
                                    fg_color="black",
                                    hover_color="gray")
        
    


main_windo = CTk()                                                              
main_windo.geometry("500x750")
main_windo.title("Calculator")

# create all class object
app_calculater = object.__new__(MultiUtilityApp)

btn = CTkButton(main_windo, text="Open Calculator", font=("Helvetica", 14, "bold"), width=150, height=45, command=lonch_cal_btn)
btn.place(x=250, y=70, anchor="center")

chatbot_btn = CTkButton(main_windo, text="Open ChatBot", font=("Helvetica", 14, "bold"), width=150, height=45, command=lonch_chatbot_btn)
chatbot_btn.place(x=250, y=170, anchor="center")

mode_change_btn=CTkButton(main_windo,
                          text="🔆",
                          text_color="black",
                          fg_color="white",
                          bg_color="transparent",
                          hover_color="gray",
                          command=change,
                          width=30,
                          height=30,
                          font=("Segoe UI Emoji" , 15))
mode_change_btn.pack(ipadx=0, ipady=0, anchor="center")




# open_calculator(main_windo)
main_windo.mainloop()

