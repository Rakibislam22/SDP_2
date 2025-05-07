import math
import re
from customtkinter import *
from currency_converter import *
from tkinter import *
from PIL import Image , ImageTk
from CTkScrollableDropdown import CTkScrollableDropdown


set_appearance_mode("dark")
set_default_color_theme('dark-blue')
c=CurrencyConverter()


font_12 = ("Helvetica",12,"bold")
font_16 = ("Helvetica",16,"bold")
font_14 = ("Helvetica",14,"bold")
font_18 = ("Helvetica",18,"bold")
font_22 = ("Helvetica",22,"bold")
font_24 = ("Helvetica",24,"bold")
font_38 = ("Helvetica",38,"bold")


n=1            # for currency converter
frm=""         # for currency converter
mode="dark"
input_num=""   # for calculator


#  calculator functions start

def valu_input(val):
    input_box.configure(state="normal")
    global input_num
    input_num += str(val)
    input_box.delete(1.0,"end")
    input_box.insert(1.0,input_num)
    input_box.configure(state="disabled")


def calculation():
    global input_num
    try:
        input_num = str(eval(input_num))
        input_box.configure(state="normal")
        input_box.delete(1.0,"end")
        input_box.insert(1.0,input_num)
        input_box.configure(state="disabled")
    except:
        clear()
        input_box.configure(state="normal")
        input_box.insert(1.0,"Error")
        input_box.configure(state="disabled")
        


def percentage():
    global input_num
    try:
        # Match the last number and operator before %
        match = re.search(r'([\d\.]+)([\+\-\*/])([\d\.]+)%$', input_num)
        if match:
            first, operator, percent = match.groups()
            new_expr = f"{first}{operator}({first}*{percent}/100)"
            input_num = re.sub(r'([\d\.]+[\+\-\*/][\d\.]+)%$', new_expr, input_num)
        else:
            # Handle single number % like 50% = 0.5
            match = re.search(r'([\d\.]+)%$', input_num)
            if match:
                num = match.group(1)
                input_num = re.sub(r'([\d\.]+)%$', f"({num}/100)", input_num)

        #input_box.configure(state="normal")
        #input_box.delete(1.0, "end")
        #input_box.insert(1.0, input_num)
        #input_box.configure(state="disabled")
    except:
        clear()
        input_box.configure(state="normal")
        input_box.insert(1.0,"Error")
        input_box.configure(state="disabled")


def square():
    global input_num
    try:
        result = float(input_num) ** 2
        input_num = str(result)
        input_box.configure(state="normal")
        input_box.delete(1.0, "end")
        input_box.insert(1.0, input_num)
        input_box.configure(state="disabled")
    except:
        clear()
        input_box.configure(state="normal")
        input_box.insert(1.0,"Error")
        input_box.configure(state="disabled")


def square_root():
    global input_num
    try:
        result = math.sqrt(float(input_num))
        input_num = str(result)
        input_box.configure(state="normal")
        input_box.delete(1.0, "end")
        input_box.insert(1.0, input_num)
        input_box.configure(state="disabled")
    except:
        clear()
        input_box.configure(state="normal")
        input_box.insert(1.0,"Error")
        input_box.configure(state="disabled")


def clear():
    global input_num
    input_num = ""
    input_box.configure(state="normal")
    input_box.delete(1.0,"end")
    input_box.configure(state="disabled")

def backspace():
    global input_num
    if input_num:  
        input_num = input_num[:-1]  
        input_box.configure(state="normal")
        input_box.delete(1.0, "end")  
        input_box.insert(1.0, input_num)  
        input_box.configure(state="disabled")
    
    
#   calculator functions end



# currency convator functions start

def change_mode():
    global mode
    if mode == "dark":
        mode_change_btn.configure(text="D",
                                  text_color="white",
                                  fg_color="black",
                                  hover_color="gray")
        set_appearance_mode("light")
        calculator_fram.configure(fg_color="white")
        input_box.configure(fg_color="white", text_color="black")

        windo.configure(fg_color="white")
        to_lable.configure(fg_color="white")
        exchange_btn.configure(fg_color="transparent",
                               hover_color="white",
                               image=exc_btn_img_black)
        to_lable_extra.configure(fg_color="#979da2")
        mode ="light"

    elif mode == "light":
        mode_change_btn.configure(text="L",
                                  text_color="black",
                                  fg_color="white",
                                  hover_color="gray")
        set_appearance_mode("dark")
        to_lable.configure(fg_color="#3A3B3C")
        exchange_btn.configure(fg_color="transparent",
                               hover_color="black",
                               image=exc_btn_img_white)
        calculator_fram.configure(fg_color="black")
        input_box.configure(fg_color="black", text_color="white")
        windo.configure(fg_color="black")
        mode ="dark"
    

def exc_btn():
    form=from_convart_box.get()
    too=to_convart_box.get()
    from_convart_box.set(too)
    to_convart_box.set(form)

def convertcurrency():
    global n, frm
    try:
        n=float(from_lable.get())
    except:
        n=0
    frm = from_convart_box.get()
    to = to_convart_box.get()
    try:
        ans=str(c.convert(n,frm,to))
        ans=str(round(ans,2))
        to_lable.configure(text=str(ans))
    except:
        if frm =='BDT' or to == 'BDT':
            if to == 'BDT' and frm != 'BDT':
                bdt = c.convert(n,frm)
                bdt = bdt*131.84                                          #change with the current valu EUR to BDT
                bdt= round(bdt,2)
                to_lable.configure(text=str(bdt))
            elif frm == 'BDT' and to != 'BDT':
                bdt = c.convert(n,'EUR',to)
                bdt = bdt/131.84                                          #change with the current valu EUR to BDT
                bdt= round(bdt,2)
                to_lable.configure(text=str(bdt))
            else:
                to_lable.configure(text=n)
        else:
            to_lable.configure(text=n)

# currency convator functions end



def update_tabs(s_tab):
    main_tab.set(tab_names[s_tab])

    for i, (name, btn) in enumerate(tab_buttons.items()):
        if i == s_tab:
            btn.configure(text=tab_names[i], image=icons[i])
        else:
            btn.configure(text=" ", image=icons[i])



main_windo = CTk()                                                                 # main window
main_windo.geometry("500x600")

mode_change_btn=CTkButton(main_windo,
                          text="L",
                          text_color="black",
                          fg_color="white",
                          hover_color="gray",
                          command=change_mode,
                          width=30,
                          height=30,
                          font=font_16)
mode_change_btn.place(x=468,y=10)

main_tab = CTkTabview(main_windo, width=430, height=500)                           # main tab
main_tab.pack()



icon1 = CTkImage(light_image=Image.open("image/calculator.png"), size=(22, 22))
icon2 = CTkImage(light_image=Image.open("image/exchange.png"), size=(22, 22))
icon3 = CTkImage(light_image=Image.open("image/unit-1png.png"), size=(22, 22))

icons = [icon1, icon2, icon3]
tab_names = ["Calculator", "Currency Converter", "Unit Converter"]



calculator_tab = main_tab.add("Calculator")
currency_converter_tab = main_tab.add("Currency Converter")
unit_converter_tab = main_tab.add("Unit Converter")



reposition_calculater_frame = CTkFrame(calculator_tab, )                                          # calculator start
reposition_calculater_frame.pack()



# mode_btn_img_black = CTkImage(light_image=Image.open('image/screen.png'),
#                        dark_image=Image.open('image/screen.png'),
#                        size=(33,33))
# mode_btn_img_white = CTkImage(light_image=Image.open('image/screen.png'),
#                        dark_image=Image.open('image/screen.png'),
#                        size=(33,33))



calculator_fram = CTkFrame(reposition_calculater_frame, fg_color="black")
calculator_fram.pack(side="top", expand=True, fill="both")

input_box = CTkTextbox(calculator_fram, height=70,width=300, state="disabled", fg_color="black",font=font_38, text_color="white")
input_box.grid(columnspan=5, pady=10,padx=10)


num_c = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="C", command=clear, fg_color="#74cec6", text_color="red" )
num_c.grid(row=1, column=1, padx=5, pady=5)
num_open_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="(", text_color="black", fg_color="#74cec6", command=lambda :valu_input("("))
num_open_brackt.grid(row=1, column=2, padx=5, pady=5)
num_close_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text=")", fg_color="#74cec6",  text_color="black", command=lambda :valu_input(")"))
num_close_brackt.grid(row=1, column=3, padx=5, pady=5)

num_1 = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="1", fg_color="#0f1320", command=lambda: valu_input("1"))
num_1.grid(row=5, column=1, padx=5, pady=5)
num_2 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="2", fg_color="#0f1320", command=lambda: valu_input("2"))
num_2.grid(row=5, column=2, padx=5, pady=5)
num_3 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="3", fg_color="#0f1320", command=lambda: valu_input("3"))
num_3.grid(row=5, column=3, padx=5, pady=5)
num_4 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="4", fg_color="#0f1320", command=lambda: valu_input("4"))
num_4.grid(row=4, column=1, padx=5, pady=5)
num_5 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="5", fg_color="#0f1320", command=lambda: valu_input("5"))
num_5.grid(row=4, column=2, padx=5, pady=5)
num_6 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="6", fg_color="#0f1320", command=lambda: valu_input("6"))
num_6.grid(row=4, column=3, padx=5, pady=5)
num_7 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="7", fg_color="#0f1320", command=lambda: valu_input("7"))
num_7.grid(row=3, column=1, padx=5, pady=5)
num_8 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="8", fg_color="#0f1320", command=lambda: valu_input("8"))
num_8.grid(row=3, column=2, padx=5, pady=5)
num_9 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="9", fg_color="#0f1320", command=lambda: valu_input("9"))
num_9.grid(row=3, column=3, padx=5, pady=5)
num_0 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="0", fg_color="#0f1320", command=lambda: valu_input("0"))
num_0.grid(row=6, column=2, padx=5, pady=5)
num_0 = CTkButton(calculator_fram, width=60, height=60,font=font_16, text=".", fg_color="#0f1320", command=lambda: valu_input("."))
num_0.grid(row=6, column=1, padx=5, pady=5)
num_eq = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="=", fg_color="#0f1320", command=calculation)
num_eq.grid(row=6, column=3, padx=5, pady=5)

backSpace = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="⌫", text_color="#eb7546", fg_color="#74cec6", command=backspace)
backSpace.grid(row=1, column=4, padx=5, pady=5)
Square = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="x²", text_color="#f0e6ad", fg_color="#0f1320", command=square)
Square.grid(row=2, column=2, padx=5, pady=5)
Square_root = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="√", text_color="#f0e6ad", fg_color="#0f1320", command=square_root)
Square_root.grid(row=2, column=3, padx=5, pady=5)
perCentage = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="%", text_color="#f0e6ad", fg_color="#0f1320",command=lambda: (valu_input("%"), percentage()))
perCentage.grid(row=2, column=1, padx=5, pady=5)
num_plus = CTkButton(calculator_fram, width=60, height=130,font=font_16, text="+", text_color="black", fg_color="#74cec6", command=lambda: valu_input("+"))
num_plus.grid(row=5, column=4,rowspan=2, padx=5, pady=5)
num_minus = CTkButton(calculator_fram, width=60, height=60,font=font_24, text="-", text_color="black", fg_color="#74cec6", command=lambda: valu_input("-"))
num_minus.grid(row=4, column=4, padx=5, pady=5)
num_mul = CTkButton(calculator_fram, width=60, height=60,font=font_24, text="*", text_color="black", fg_color="#74cec6", command=lambda: valu_input("*"))
num_mul.grid(row=3, column=4, padx=5, pady=5)
num_div = CTkButton(calculator_fram, width=60, height=60,font=font_18, text="/", text_color="black", fg_color="#74cec6", command=lambda: valu_input("/"))
num_div.grid(row=2, column=4, padx=5, pady=5)



# back_calculator_btn = CTkButton(calculator_fram,width=10, height=10,corner_radius=50, text="<", command=calculator_fram.destroy)
# back_calculator_btn.place(x=0,y=0)
# home_calculator_btn = CTkButton(calculate_windo,width=1, text="Home", bg_color="transparent", fg_color="transparent")
# home_calculator_btn.place(x=140, y=460)


# calculator end


# currency convator start


currency_converter_frame = CTkFrame(currency_converter_tab )
currency_converter_frame.pack(fill="both", expand=True, side="top")

windo = CTkFrame(currency_converter_frame, fg_color="black")
windo.pack(fill="both", expand=True, side="top")


exc_btn_img_black = CTkImage(light_image=Image.open('image/logo black.png'),
                       dark_image=Image.open('image/logo black.png'),
                       size=(33,33))
exc_btn_img_white = CTkImage(light_image=Image.open('image/logo white.png'),
                       dark_image=Image.open('image/logo white.png'),
                       size=(33,33))

titel_leble=CTkLabel(windo,
                     text="Currency Converter",
                     font=font_22)
titel_leble.pack(pady=10)

from_leble=CTkLabel(windo,
                     text="FROM",
                     font=font_16)
from_leble.place(x=45,y=55)

to_leble=CTkLabel(windo,
                     text="TO",
                     font=font_16)
to_leble.place(x=255,y=55)

exchange_btn=CTkButton(windo,
                       width=20,
                       height=20,
                       border_spacing=0,
                       border_width=0,
                       corner_radius=5,
                       text="",
                       hover_color="black",
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

from_convart_box= CTkComboBox(windo,
                              values=cuntry,
                              justify='center',
                              font=font_14)
from_convart_box.place(x=40,y=85)
from_box_deopdown = CTkScrollableDropdown(from_convart_box, values=cuntry)

to_convart_box=CTkComboBox(windo,
                           values=cuntry,
                           justify='center',
                           font=font_14)
to_convart_box.place(x=250,y=85)
to_box_deopdown = CTkScrollableDropdown(to_convart_box, values=cuntry)

from_lable=CTkEntry(windo,
                    font=font_12,
                    placeholder_text="Enter Amount",
                    justify='center')
from_lable.place(x=40,y=130)

to_lable_extra = CTkLabel(windo, text="", 
                          corner_radius=5, 
                          fg_color="#565b5e", 
                          bg_color="transparent", 
                          height=28, width=140)
to_lable_extra.place(x=250,y=130)

to_lable=CTkLabel(windo,
                  text="0",
                  justify="center",
                  width=135,
                  height=23,
                  corner_radius=2,
                  fg_color="#343638",
                  bg_color="#343638",
                  font=font_14,)
to_lable.place(x=252,y=132)


convart_btn=CTkButton(windo,
                      text="Convert",
                      font=font_14,
                      command=convertcurrency)
convart_btn.place(x=150,y=180)



tab_buttons = main_tab._segmented_button._buttons_dict

for i, (name, btn) in enumerate(tab_buttons.items()):
    btn.configure(text="", image=icons[i], bg_color="transparent", font=font_12, border_width=2, border_spacing=4 ) 

for j, (name, btn) in enumerate(tab_buttons.items()):
    if j == 0:
        btn.configure(text=tab_names[j], image=icons[j])
    else:
        btn.configure(text=" ", image=icons[j])


for i, btn in enumerate(tab_buttons.values()):
    btn.configure(command=lambda tab_n=i: update_tabs(tab_n))

main_windo.title("Utilites")
icon = PhotoImage(file="image/logo_b.png")
main_windo.tk.call('wm', 'iconphoto', main_windo._w, icon)

main_windo.mainloop()