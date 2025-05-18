from customtkinter import *
from currency_converter import *
from tkinter import *
from PIL import Image
from CTkScrollableDropdown import CTkScrollableDropdown

set_appearance_mode("system")
set_default_color_theme('dark-blue')
c=CurrencyConverter()


n=1
frm=""
mode="dark"

def change_mode():
    global mode
    if mode == "dark":
        mode_change_btn.configure(text="D",
                                  text_color="white",
                                  fg_color="black",
                                  hover_color="gray")
        set_appearance_mode("light")
        to_lable.configure(fg_color="transparent")
        exchange_btn.configure(fg_color="transparent",
                               hover_color="#f2f2f2",
                               image=exc_btn_img_black)
        mode ="light"
    elif mode == "light":
        mode_change_btn.configure(text="L",
                                  text_color="black",
                                  fg_color="white",
                                  hover_color="gray")
        set_appearance_mode("dark")
        to_lable.configure(fg_color="#3A3B3C")
        exchange_btn.configure(fg_color="transparent",
                               hover_color="#1a1a1a",
                               image=exc_btn_img_white)
        mode ="dark"
    

def exc_btn():
    form=from_convart_box.get()
    too=to_convart_box.get()
    from_convart_box.set(too)
    to_convart_box.set(form)

def convaercurrency():
    global n, frm
    try:
        n=int(from_lable.get())
    except:
        n=0
    frm = from_convart_box.get()
    to = to_convart_box.get()
    try:
        ans=c.convert(n,frm,to)
        ans= round(ans,2)
        to_lable.configure(text=str(ans))
    except:
        if frm =='BDT' or to == 'BDT':
            if to == 'BDT' and frm != 'BDT':
                bdt = c.convert(n,frm)
                bdt = bdt*131.84                                          #change with the current valu EUR to BDT
                bdt= round(bdt,2)
                to_lable.configure(text=str(bdt))
            elif frm == 'BDT' and to != 'BDT':
                bdt = c.convert(n,'USD',to)
                bdt = bdt/121.47                                          #change with the current valu USD to BDT
                bdt= round(bdt,2)
                to_lable.configure(text=str(bdt))
            else:
                to_lable.configure(text=n)
        else:
            # to_lable.configure(text=ans)
            pass
            


windo=CTk()
windo.title("Currency Converter")
windo.geometry("500x650")
# windo.resizable(height=False,width=False)

# frame1 = CTkFrame(windo, height=1, width=500)
# frame1.pack()

frame = CTkFrame(windo)
frame.pack(expand=True, fill="both", side="top")

exc_btn_img_black = CTkImage(light_image=Image.open('image/logo black.png'),
                       dark_image=Image.open('image/logo black.png'),
                       size=(33,33))
exc_btn_img_white = CTkImage(light_image=Image.open('image/logo white.png'),
                       dark_image=Image.open('image/logo white.png'),
                       size=(33,33))

mode_change_btn=CTkButton(frame,
                          text="L",
                          text_color="black",
                          fg_color="white",
                          hover_color="gray",
                          command=change_mode,
                          width=30,
                          height=30,
                          font=("Helvetica",12,"bold"))
mode_change_btn.place(x=385,y=10)

titel_leble=CTkLabel(frame,
                     text="Currency Converter",
                     font=("Helvetica",22,"bold"))
titel_leble.pack(pady=10)

from_leble=CTkLabel(frame,
                     text="FROM",
                     font=("Helvetica",16,"bold"))
from_leble.place(x=45,y=55)

to_leble=CTkLabel(frame,
                     text="TO",
                     font=("Helvetica",16,"bold"))
to_leble.place(x=255,y=55)

exchange_btn=CTkButton(frame,
                       width=20,
                       height=20,
                       border_spacing=0,
                       border_width=0,
                       corner_radius=5,
                       text="",
                       hover_color="#1a1a1a",
                       bg_color="transparent",
                       fg_color="transparent",
                       image=exc_btn_img_white,
                       command=exc_btn)
exchange_btn.place(x=192,y=81)

cuntry = [
    "BDT", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", 
    "ISK", "NOK", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", 
    "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"
]

from_convart_box= CTkComboBox(frame,
                              values=cuntry,
                              justify='center',
                              font=("Helvetica",14,"bold"),
                              state="readonly")
from_convart_box.set("USD")
from_convart_box.place(x=40,y=85)
from_box_deopdown = CTkScrollableDropdown(from_convart_box, values=cuntry)

to_convart_box=CTkComboBox(frame,
                           values=cuntry,
                           justify='center',
                           font=("Helvetica",14,"bold"),
                           state="readonly")
to_convart_box.set("BDT")
to_convart_box.place(x=250,y=85)
to_box_deopdown = CTkScrollableDropdown(to_convart_box, values=cuntry)

from_lable=CTkEntry(frame,
                    font=("Helvetica",14, "bold"),
                    placeholder_text="Enter Amount",
                    justify='center')
from_lable.place(x=40,y=130)

to_lable=CTkLabel(frame,
                  text="0",
                  justify="center",
                  width=140,
                  height=28,
                  corner_radius=7,
                  fg_color="#3A3B3C",
                  bg_color="transparent",
                  font=("Helvetica",14, "bold"),)
to_lable.place(x=250,y=130)

convart_btn=CTkButton(frame,
                      text="Convert",
                      font=("Helvetica",14, "bold"),
                      command=convaercurrency)
convart_btn.place(x=150,y=180)

copyright_frame = CTkFrame(windo, height=10,fg_color="red")
copyright_frame.pack(fill="x",side="top")

copyrights = CTkLabel(copyright_frame, text="© alifjobaer12", font=("Calibri", 12), corner_radius=0, width=1, height=1, fg_color="transparent", bg_color="transparent", text_color="#9e9e9e", )
copyrights.place(x=425, y=5, anchor="e") 


windo.mainloop()