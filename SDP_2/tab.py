import math
import re
from customtkinter import *
from currency_converter import *
from tkinter import *
from PIL import Image
from pathlib import Path
from CTkScrollableDropdown import CTkScrollableDropdown
from unitconverter import converter


set_appearance_mode("dark")
set_default_color_theme('dark-blue')


def open_calculator(main_cal_windo):

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

    #for unit converter
    unit="length"
    input_val=""
    ans=""

    font_12=("Helvetica", 12, "bold")
    font_14=("Helvetica", 14, "bold")
    font_16=("Helvetica", 16, "bold")

    length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi", "A", "mµ", "µ" ]
    weight_units = ["mg", "cg", "dg", "g", "kg", "dag", "hg", "oz.", "lb.","st.", "st", "lt" , "T" ]
    energy_units = ["Btu", "thm", "cal", "kcal", "tcal", "MJ", "J", "GJ", "TJ", "Wh", "kWh", "MWh", "GWh", "TWh"]
    data_units = ["b", "B", "KB", "Kb", "Mb", "MB", "GB", "Gb", "Tb", "TB"]
    speed_units = ["m/s", "km/h", "cm/s", "mph", "ft/s", "yd/s", "mi/s", "knots", "c"]
    volume_units = ["ml", "L", "m3", "in3", "ft3", "pt", "qt", "gal", "bbl"]
    temperature_units = ["C", "F", "K"]
    time_units = ["s", "min", "hr", "day"]



    #  calculator functions start

    def valu_input(val):
        input_box.configure(state="normal")
        nonlocal input_num
        input_num += str(val)
        input_box.delete(1.0,"end")
        input_box.insert(1.0,input_num)
        input_box.configure(state="disabled")


    def calculation():
        nonlocal input_num
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


    def clear():
        nonlocal input_num
        input_num = ""
        input_box.configure(state="normal")
        input_box.delete(1.0,"end")
        input_box.configure(state="disabled")


    def percentage():
        nonlocal input_num
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
        except:
            clear()
            input_box.configure(state="normal")
            input_box.insert(1.0,"Error")
            input_box.configure(state="disabled")


    def square():
        nonlocal input_num
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
        nonlocal input_num
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


    def backspace():
        nonlocal input_num
        if input_num:  
            input_num = input_num[:-1]  
            input_box.configure(state="normal")
            input_box.delete(1.0, "end")  
            input_box.insert(1.0, input_num)  
            input_box.configure(state="disabled")



    #   calculator functions end



    # currency convator functions start

    def change_mode():
        nonlocal mode
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
            copyright_frame.configure(fg_color="#cfcfcf", bg_color="#cfcfcf")
            
            btn_frame.configure(fg_color="white")
            converter_frame.configure(fg_color="white")
            U_exchange_btn.configure(fg_color="transparent",
                                   hover_color="white",
                                   image=U_exc_btn_img_black)
            U_copyright_frame.configure(fg_color="#cfcfcf", bg_color="#cfcfcf")

            mode ="light"

        elif mode == "light":
            mode_change_btn.configure(text="L",
                                      text_color="black",
                                      fg_color="white",
                                      hover_color="gray")
            set_appearance_mode("dark")
            calculator_fram.configure(fg_color="black")
            input_box.configure(fg_color="black", text_color="white")

            windo.configure(fg_color="black")
            to_lable.configure(fg_color="#3A3B3C")
            exchange_btn.configure(fg_color="transparent",
                                   hover_color="black",
                                   image=exc_btn_img_white)
            copyright_frame.configure(fg_color="#333333", bg_color="#333333")

            btn_frame.configure(fg_color="black")
            converter_frame.configure(fg_color="black")
            U_exchange_btn.configure(fg_color="transparent",
                                   hover_color="black",
                                   image=U_exc_btn_img_white)
            U_copyright_frame.configure(fg_color="#333333", bg_color="#333333")

            mode ="dark"


    def exc_btn():
        form=from_convart_box.get()
        too=to_convart_box.get()
        from_convart_box.set(too)
        to_convart_box.set(form)


    def show_output(ans):
        to_lable.configure(state="normal")
        to_lable.delete(0, "end")
        to_lable.insert(0, ans)
        to_lable.configure(state="readonly")


    def convertcurrency():
        nonlocal n, frm
        try:
            n=float(from_lable.get())
        except:
            n=0
        frm = from_convart_box.get()
        to = to_convart_box.get()
        try:
            ans=c.convert(n,frm,to)
            ans=round(ans,2)
            show_output(str(ans))
            # to_lable.configure(text=str(ans))
        except:
            if frm =='BDT' or to == 'BDT':
                if to == 'BDT' and frm != 'BDT':
                    bdt = c.convert(n,frm)
                    bdt = bdt*131.84                                          #change with the current valu EUR to BDT
                    bdt= round(bdt,2)
                    show_output(str(bdt))
                elif frm == 'BDT' and to != 'BDT':
                    bdt = c.convert(n,'EUR',to)
                    bdt = bdt/131.84                                          #change with the current valu EUR to BDT
                    bdt= round(bdt,2)
                    show_output(str(bdt))
                else:
                    show_output(str(n))
            else:
                show_output("Error")
                

    # currency convator functions end



    def update_tabs(s_tab):
        main_tab.set(tab_names[s_tab])

        for i, (name, btn) in enumerate(tab_buttons.items()):
            if i == s_tab:
                btn.configure(text=tab_names[i], image=icons[i])
            else:
                btn.configure(text=" ", image=icons[i])


    # unit converter function start

    def U_exc_btn():
        frm=U_from_combbox.get()
        to=U_to_combbox.get()
        U_from_combbox.set(to)
        U_to_combbox.set(frm)


    def length_btn():
        nonlocal unit
        unit="length"
        U_titel.configure(text="Length")
        U_from_combbox.configure(state="normal", values=length_units)
        U_from_combbox_deopdown.configure(values=length_units)
        U_to_combbox.configure(state="normal", values=length_units)
        U_to_combbox_deopdown.configure(values=length_units)
        U_from_combbox.set(length_units[0])
        U_to_combbox.set(length_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def volume_btn():
        nonlocal unit
        unit="volume"
        U_titel.configure(text="Volume")
        U_from_combbox.configure(state="normal", values=volume_units)
        U_from_combbox_deopdown.configure(values=volume_units)
        U_to_combbox.configure(state="normal", values=volume_units)
        U_to_combbox_deopdown.configure(values=volume_units)
        U_from_combbox.set(volume_units[0])
        U_to_combbox.set(volume_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def temperature_btn():
        nonlocal unit
        unit="temperature"
        U_titel.configure(text="Temperature")
        U_from_combbox.configure(state="normal", values=temperature_units)
        U_from_combbox_deopdown.configure(values=temperature_units)
        U_to_combbox.configure(state="normal", values=temperature_units)
        U_to_combbox_deopdown.configure(values=temperature_units)
        U_from_combbox.set(temperature_units[0])
        U_to_combbox.set(temperature_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def time_btn():
        nonlocal unit
        unit="time"
        U_titel.configure(text="Time")
        U_from_combbox.configure(state="normal", values=time_units)
        U_from_combbox_deopdown.configure(values=time_units)
        U_to_combbox.configure(state="normal", values=time_units)
        U_to_combbox_deopdown.configure(values=time_units)
        U_from_combbox.set(time_units[0])
        U_to_combbox.set(time_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def weight_btn():
        nonlocal unit
        unit="weight"
        U_titel.configure(text="Weight")
        U_from_combbox.configure(state="normal", values=weight_units)
        U_from_combbox_deopdown.configure(values=weight_units)
        U_to_combbox.configure(state="normal", values=weight_units)
        U_to_combbox_deopdown.configure(values=weight_units)
        U_from_combbox.set(weight_units[0])
        U_to_combbox.set(weight_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def speed_btn():
        nonlocal unit
        unit="speed"
        U_titel.configure(text="Speed")
        U_from_combbox.configure(state="normal", values=speed_units)
        U_from_combbox_deopdown.configure(values=speed_units)
        U_to_combbox.configure(state="normal", values=speed_units)
        U_to_combbox_deopdown.configure(values=speed_units)
        U_from_combbox.set(speed_units[0])
        U_to_combbox.set(speed_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def data_btn():
        nonlocal unit
        unit="data"
        U_titel.configure(text="Data")
        U_from_combbox.configure(state="normal", values=data_units)
        U_from_combbox_deopdown.configure(values=data_units)
        U_to_combbox.configure(state="normal", values=data_units)
        U_to_combbox_deopdown.configure(values=data_units)
        U_from_combbox.set(data_units[0])
        U_to_combbox.set(data_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")

    def energy_btn():
        nonlocal unit
        unit="energy"
        U_titel.configure(text="Energy")
        U_from_combbox.configure(state="normal", values=energy_units)
        U_from_combbox_deopdown.configure(values=energy_units)
        U_to_combbox.configure(state="normal", values=energy_units)
        U_to_combbox_deopdown.configure(values=energy_units)
        U_from_combbox.set(energy_units[0])
        U_to_combbox.set(energy_units[0])
        U_from_combbox.configure(state="readonly")
        U_to_combbox.configure(state="readonly")


    def U_show_output(ans):
        U_to_output_box.configure(state="normal")
        U_to_output_box.delete(0, "end")
        U_to_output_box.insert(0, ans)
        U_to_output_box.configure(state="readonly")


    def unit_convart():
        nonlocal input_val, ans
        frm = U_from_combbox.get()
        to = U_to_combbox.get()
        input_val = U_from_input_box.get()

        try:
            if(unit=="length"):
                ans = converter.convertLength(int(input_val), frm, to)
            elif (unit=="volume"):
                ans = converter.convertVolume(int(input_val), frm, to)
            elif (unit=="temperature"):
                ans = converter.convertTemperature(int(input_val), frm, to)
            elif (unit=="time"):
                ans = converter.convertTime(int(input_val), frm, to)
            elif (unit=="weight"):
                ans = converter.convertWeight(int(input_val), frm, to)
            elif (unit=="speed"):
                ans = converter.convertSpeed(int(input_val), frm, to)
            elif (unit=="data"):
                ans = converter.convertData(int(input_val), frm, to)
            elif (unit=="energy"):
                ans = converter.convertEnergy(int(input_val), frm, to)

            U_show_output(str(round(ans,2)))

        except:
            U_show_output("Error")




    mode_change_btn=CTkButton(main_cal_windo,
                              text="L",
                              text_color="black",
                              fg_color="white",
                              hover_color="gray",
                              command=change_mode,
                              width=30,
                              height=30,
                              font=font_16)
    mode_change_btn.place(x=468,y=10)

    main_tab = CTkTabview(main_cal_windo, width=460, height=573)                           # main tab
    main_tab.pack()

    
    BASE_DIR = Path(__file__).resolve().parent
    icon1_path = BASE_DIR / "image" / "calculator.png"
    icon2_path = BASE_DIR / "image" / "exchange.png"
    icon3_path = BASE_DIR / "image" / "unit-1png.png"


    icon1 = CTkImage(light_image=Image.open(icon1_path), size=(22, 22))
    icon2 = CTkImage(light_image=Image.open(icon2_path), size=(22, 22))
    icon3 = CTkImage(light_image=Image.open(icon3_path), size=(22, 22))

    icons = [icon1, icon2, icon3]
    tab_names = ["Calculator", "Currency Converter", "Unit Converter"]



    calculator_tab = main_tab.add("Calculator")
    currency_converter_tab = main_tab.add("Currency Converter")
    unit_converter_tab = main_tab.add("Unit Converter")



    reposition_calculater_frame = CTkFrame(calculator_tab, )                                          # calculator start
    reposition_calculater_frame.pack()


    calculator_fram = CTkFrame(reposition_calculater_frame, fg_color="black")
    calculator_fram.pack(side="top", expand=True, fill="both")

    input_box = CTkTextbox(calculator_fram, wrap="none", activate_scrollbars=True, height=70,width=300, state="disabled", fg_color="black",font=font_38, text_color="white")
    input_box.grid(columnspan=5, pady=10,padx=10)


    num_c = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="C", command=clear, fg_color="#74cec6", text_color="red" )
    num_c.grid(row=1, column=1, padx=5, pady=5)
    num_open_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="(", text_color="black", fg_color="#74cec6", command=lambda :valu_input("("))
    num_open_brackt.grid(row=1, column=2, padx=5, pady=5)
    num_close_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text=")", fg_color="#74cec6",  text_color="black", command=lambda :valu_input(")"))
    num_close_brackt.grid(row=1, column=3, padx=5, pady=5)

    
    backSpace = CTkButton(calculator_fram, width=60, height=60,font=font_16, text="⌫", text_color="red", fg_color="#74cec6", command=backspace)
    backSpace.grid(row=1, column=4, padx=5, pady=5)
    Square = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="x²", fg_color="#0f1320",  command=square)
    Square.grid(row=2, column=2, padx=5, pady=5)
    Square_root = CTkButton(calculator_fram, width=60, height=60 ,font=font_18, text="√", fg_color="#0f1320",  command=square_root)
    Square_root.grid(row=2, column=3, padx=5, pady=5)
    perCentage = CTkButton(calculator_fram, width=60, height=60 ,font=font_16, text="%", fg_color="#0f1320",  command=lambda: (valu_input("%"), percentage()))
    perCentage.grid(row=2, column=1, padx=5, pady=5)


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

    num_plus = CTkButton(calculator_fram, width=60, height=130,font=font_16, text="+", text_color="black", fg_color="#74cec6", command=lambda: valu_input("+"))
    num_plus.grid(row=5, column=4,rowspan=2, padx=5, pady=5)
    num_minus = CTkButton(calculator_fram, width=60, height=60,font=font_24, text="-", text_color="black", fg_color="#74cec6", command=lambda: valu_input("-"))
    num_minus.grid(row=4, column=4, padx=5, pady=5)
    num_mul = CTkButton(calculator_fram, width=60, height=60,font=font_24, text="*", text_color="black", fg_color="#74cec6", command=lambda: valu_input("*"))
    num_mul.grid(row=3, column=4, padx=5, pady=5)
    num_div = CTkButton(calculator_fram, width=60, height=60,font=font_18, text="/", text_color="black", fg_color="#74cec6", command=lambda: valu_input("/"))
    num_div.grid(row=2, column=4, padx=5, pady=5)


    # calculator end


    # currency convator start


    currency_converter_frame = CTkFrame(currency_converter_tab )
    currency_converter_frame.pack(fill="both", expand=True, side="top")

    windo = CTkFrame(currency_converter_frame, fg_color="black")
    windo.pack(fill="both", expand=True, side="top")

    BASE_DIR = Path(__file__).resolve().parent
    exc_btn_img_black_path = BASE_DIR / "image" / "logo black.png"
    exc_btn_img_white_path = BASE_DIR / "image" / "logo white.png"



    exc_btn_img_black = CTkImage(light_image=Image.open(exc_btn_img_black_path),
                           dark_image=Image.open(exc_btn_img_black_path),
                           size=(33,33))
    exc_btn_img_white = CTkImage(light_image=Image.open(exc_btn_img_white_path),
                           dark_image=Image.open(exc_btn_img_white_path),
                           size=(33,33))

    titel_leble=CTkLabel(windo,
                         text="Currency Converter",
                         font=font_22)
    titel_leble.pack(pady=50)

    from_leble=CTkLabel(windo,
                         text="FROM",
                         font=font_16)
    from_leble.place(x=55,y=105)

    to_leble=CTkLabel(windo,
                         text="TO",
                         font=font_16)
    to_leble.place(x=270,y=105)

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
    exchange_btn.place(x=223, y=148, anchor="center")

    cuntry = [
        "BDT", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", 
        "ISK", "NOK", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", 
        "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"
    ]

    from_convart_box= CTkComboBox(windo,
                                  values=cuntry,
                                  justify='center',
                                  font=font_14,
                                  state="readonly")
    from_convart_box.set("USD")
    from_convart_box.place(x=45,y=135)
    from_box_deopdown = CTkScrollableDropdown(from_convart_box, values=cuntry)

    to_convart_box=CTkComboBox(windo,
                               values=cuntry,
                               justify='center',
                               font=font_14,
                               state="readonly")
    to_convart_box.set("BDT")
    to_convart_box.place(x=260,y=135)
    to_box_deopdown = CTkScrollableDropdown(to_convart_box, values=cuntry)

    from_lable=CTkEntry(windo,
                        font=font_12,
                        placeholder_text="Enter Amount",
                        justify='center')
    from_lable.place(x=45,y=200)

    to_lable=CTkEntry(windo, state="readonly",
                      justify="center",
                      width=140,
                      height=28,
                      fg_color="#343638",
                      bg_color="transparent",
                      font=font_14,)
    to_lable.place(x=260,y=200)

    convart_btn=CTkButton(windo,
                          text="Convert",
                          font=font_14,
                          command=convertcurrency)
    convart_btn.place(x=460/2, y=280, anchor="center")

    # currency converter end


    # add image in tabview "start"

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

    # add image in tabview "end"


    # copyright watermark start

    copyright_frame = CTkFrame(currency_converter_frame, height=8, border_width=0,bg_color="#333333", fg_color="#333333")
    copyright_frame.pack(fill="x",side="top")

    copyrights = CTkLabel(main_tab, text="© alifjobaer12", font=("Calibri", 11), corner_radius=0, width=1, height=1, fg_color="transparent", bg_color="transparent", text_color="#9e9e9e" )
    copyrights.place(x=450, y=565, anchor="e")

    # copyright watermark end


    # unit converter start

    unit_converter_frame_main = CTkFrame(unit_converter_tab)
    unit_converter_frame_main.pack(fill="both", expand=True, side="top")

    unit_converter_frame = CTkFrame(unit_converter_frame_main)
    unit_converter_frame.pack(fill="both", expand=True, side="top")


    U_copyright_frame = CTkFrame(unit_converter_frame_main, height=8, border_width=0,bg_color="#333333", fg_color="#333333")
    U_copyright_frame.pack(fill="x",side="top")


    unit_converter_frame = CTkFrame(unit_converter_frame)
    unit_converter_frame.pack(fill="both", expand=True)


    btn_frame = CTkFrame(unit_converter_frame, fg_color="black", width=120, height=500)
    btn_frame.pack(fill="both", expand=False, side="left")

    converter_frame = CTkFrame(unit_converter_frame, fg_color="black", width=280)
    converter_frame.pack(fill="both", expand=True, side="right")

    btn_frame_middle = CTkFrame(btn_frame,corner_radius=0, fg_color="transparent")
    btn_frame_middle.pack(fill="x", expand=False, side="left", )


    btn_length = CTkButton(btn_frame_middle, width=100, font=font_12, command=length_btn, text="Length",)
    btn_length.pack(padx=20, pady=7, )
    btn_volume = CTkButton(btn_frame_middle, width=100, font=font_12, command=volume_btn, text="Volume")
    btn_volume.pack(padx=20, pady=7,)
    btn_temperature = CTkButton(btn_frame_middle, width=100, font=font_12, command=temperature_btn, text="Temperature")
    btn_temperature.pack(padx=20, pady=7,)
    btn_time = CTkButton(btn_frame_middle, width=100, font=font_12, command=time_btn, text="Time")
    btn_time.pack(padx=20, pady=7,)
    btn_weight = CTkButton(btn_frame_middle, width=100, font=font_12, command=weight_btn, text="Weight")
    btn_weight.pack(padx=20, pady=7,)
    btn_speed = CTkButton(btn_frame_middle, width=100, font=font_12, command=speed_btn, text="Speed")
    btn_speed.pack(padx=20, pady=7,)
    btn_data = CTkButton(btn_frame_middle, width=100, font=font_12, command=data_btn, text="Data")
    btn_data.pack(padx=20, pady=7,)
    btn_energy = CTkButton(btn_frame_middle, width=100, font=font_12, command=energy_btn, text="Energy")
    btn_energy.pack(padx=20, pady=7,)

    left_border = CTkFrame(btn_frame, width=3, fg_color="#808080") 
    left_border.pack(side="right", fill="y")


    converter_frame_middle1 = CTkFrame(converter_frame, fg_color="transparent", )
    converter_frame_middle1.pack(fill="both", expand=True, anchor="center", ipadx=50)

    U_titel = CTkLabel(converter_frame_middle1, text="Length",  font=("Helvetica", 30, "bold"), fg_color="transparent")
    U_titel.pack(pady=60)

    U_from_lable = CTkLabel(converter_frame_middle1, justify="center", text="From", font=font_16)
    U_from_lable.place(x=34, y=135)
    U_to_lable = CTkLabel(converter_frame_middle1, justify="center", text="To", font=font_16)
    U_to_lable.place(x=187, y=135)

    U_from_combbox = CTkComboBox(converter_frame_middle1, justify="center", values=length_units, font=font_16, width=100, state="readonly" )
    U_from_combbox.set(length_units[0])
    U_from_combbox.place(x=27, y=165)
    U_from_combbox_deopdown = CTkScrollableDropdown(U_from_combbox, values=length_units)

    U_to_combbox = CTkComboBox(converter_frame_middle1, justify="center", values=length_units, font=font_16, width=100, state="readonly" )
    U_to_combbox.set(length_units[0])
    U_to_combbox.place(x=180, y=165)
    U_to_combbox_deopdown = CTkScrollableDropdown(U_to_combbox, values=length_units)


    U_from_input_box = CTkEntry(converter_frame_middle1, justify="center", width=100, font=font_14, fg_color="transparent", placeholder_text="Input")
    U_from_input_box.place(x=27, y=220)

    U_to_output_box = CTkEntry(converter_frame_middle1, justify="center", width=100, fg_color="transparent", state="readonly", font=font_14)
    U_to_output_box.place(x=180, y=220)

    U_btn_convert = CTkButton(converter_frame_middle1, text="Convert", width=120, font=font_16, command=unit_convart)
    U_btn_convert.place(x=153.5, y=300, anchor="center")

    U_BASE_DIR = Path(__file__).resolve().parent
    U_exc_btn_img_black_path = U_BASE_DIR / "image" / "logo black.png"
    U_exc_btn_img_white_path = U_BASE_DIR / "image" / "logo white.png"

    U_exc_btn_img_black = CTkImage(light_image=Image.open(U_exc_btn_img_black_path),
                               dark_image=Image.open(U_exc_btn_img_black_path),
                               size=(25,25))
    U_exc_btn_img_white = CTkImage(light_image=Image.open(U_exc_btn_img_white_path),
                               dark_image=Image.open(U_exc_btn_img_white_path),
                               size=(23,23))

    U_exchange_btn=CTkButton(converter_frame_middle1,
                               width=20,
                               height=20,
                               border_spacing=0,
                               border_width=0,
                               corner_radius=5,
                               text="",
                               hover_color="black",
                               bg_color="transparent",
                               fg_color="transparent",
                               image=U_exc_btn_img_white,
                               command=U_exc_btn)
    U_exchange_btn.place(x=135.5,y=166)

    # unit converter end

# main_cal_windo = CTk()                                                                 # main window
# main_cal_windo.geometry("500x600")

# open_calculator(main_cal_windo)

# main_cal_windo.mainloop()