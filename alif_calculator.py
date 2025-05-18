import math
import re
from customtkinter import *
from currency_converter import CurrencyConverter
from tkinter import *
from PIL import Image
from pathlib import Path
from CTkScrollableDropdown import CTkScrollableDropdown
from unitconverter import converter


class MultiUtilityApp:
    def __init__(self, main_cal_windo):
        self.main_cal_windo = main_cal_windo

        #set_appearance_mode("dark")
        set_default_color_theme('dark-blue')

        self.open_calculator()

    def change_mode(self, m):
        if m == "light":
            set_appearance_mode("light")
            self.calculator_fram.configure(fg_color="white")
            self.input_box.configure(fg_color="white", text_color="black")

            self.windo.configure(fg_color="white")
            self.to_lable.configure(fg_color="white")
            self.exchange_btn.configure(fg_color="transparent",
                                        hover_color="white",
                                        image=self.exc_btn_img_black)
            self.copyright_frame.configure(fg_color="transparent", bg_color="transparent")

            self.btn_frame.configure(fg_color="white")
            self.converter_frame.configure(fg_color="white")
            self.U_exchange_btn.configure(fg_color="transparent",
                                          hover_color="white",
                                          image=self.U_exc_btn_img_black)
            self.U_copyright_frame.configure(fg_color="transparent", bg_color="transparent")

        elif m == "dark":
            set_appearance_mode("dark")
            self.calculator_fram.configure(fg_color="black")
            self.input_box.configure(fg_color="black", text_color="white")

            self.windo.configure(fg_color="black")
            self.to_lable.configure(fg_color="#3A3B3C")
            self.exchange_btn.configure(fg_color="transparent",
                                        hover_color="black",
                                        image=self.exc_btn_img_white)
            self.copyright_frame.configure(fg_color="transparent", bg_color="transparent")

            self.btn_frame.configure(fg_color="black")
            self.converter_frame.configure(fg_color="black")
            self.U_exchange_btn.configure(fg_color="transparent",
                                          hover_color="black",
                                          image=self.U_exc_btn_img_white)
            self.U_copyright_frame.configure(fg_color="transparent", bg_color="transparent")


    def open_calculator(self):
        self.c=CurrencyConverter()

        self.font_12 = ("Helvetica",12,"bold")
        self.font_16 = ("Helvetica",16,"bold")
        self.font_14 = ("Helvetica",14,"bold")
        self.font_18 = ("Helvetica",18,"bold")
        self.font_22 = ("Helvetica",22,"bold")
        self.font_24 = ("Helvetica",24,"bold")
        self.font_38 = ("Helvetica",38,"bold")

        self.n=1            # for currency converter
        self.frm=""         # for currency converter
        self.mode="dark"
        self.input_num=""   # for calculator

        self.unit="length"
        self.input_val=""
        self.ans=""
        
        self.font_12=("Helvetica", 12, "bold")
        self.font_14=("Helvetica", 14, "bold")
        self.font_16=("Helvetica", 16, "bold")
        self.length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi", "A", "mµ", "µ" ]

        self.weight_units = ["mg", "cg", "dg", "g", "kg", "dag", "hg", "oz.", "lb.","st.", "st", "lt" , "T" ]
        self.energy_units = ["Btu", "thm", "cal", "kcal", "tcal", "MJ", "J", "GJ", "TJ", "Wh", "kWh", "MWh", "GWh", "TWh"]
        self.data_units = ["b", "B", "KB", "Kb", "Mb", "MB", "GB", "Gb", "Tb", "TB"]
        self.speed_units = ["m/s", "km/h", "cm/s", "mph", "ft/s", "yd/s", "mi/s", "knots", "c"]
        self.volume_units = ["ml", "L", "m3", "in3", "ft3", "pt", "qt", "gal", "bbl"]
        self.temperature_units = ["C", "F", "K"]
        self.time_units = ["s", "min", "hr", "day"]



        #  calculator functions start

        def valu_input(val):
            self.input_box.configure(state="normal")
            self.input_num
            self.input_num += str(val)
            self.input_box.delete(1.0,"end")
            self.input_box.insert(1.0,self.input_num)
            self.input_box.configure(state="disabled")


        def calculation():
            self.input_num
            try:
                self.input_num = str(eval(self.input_num))
                self.input_box.configure(state="normal")
                self.input_box.delete(1.0,"end")
                self.input_box.insert(1.0,self.input_num)
                self.input_box.configure(state="disabled")
            except:
                clear()
                self.input_box.configure(state="normal")
                self.input_box.insert(1.0,"Error")
                self.input_box.configure(state="disabled")


        def clear():
            self.input_num
            self.input_num = ""
            self.input_box.configure(state="normal")
            self.input_box.delete(1.0,"end")
            self.input_box.configure(state="disabled")


        def percentage():
            self.input_num
            try:
                # Match the last number and operator before %
                match = re.search(r'([\d\.]+)([\+\-\*/])([\d\.]+)%$', self.input_num)
                if match:
                    first, operator, percent = match.groups()
                    new_expr = f"{first}{operator}({first}*{percent}/100)"
                    self.input_num = re.sub(r'([\d\.]+[\+\-\*/][\d\.]+)%$', new_expr, self.input_num)
                else:
                    # Handle single number % like 50% = 0.5
                    match = re.search(r'([\d\.]+)%$', self.input_num)
                    if match:
                        num = match.group(1)
                        self.input_num = re.sub(r'([\d\.]+)%$', f"({num}/100)", self.input_num)
            except:
                clear()
                self.input_box.configure(state="normal")
                self.input_box.insert(1.0,"Error")
                self.input_box.configure(state="disabled")


        def square():
            self.input_num
            try:
                result = float(self.input_num) ** 2
                self.input_num = str(result)
                self.input_box.configure(state="normal")
                self.input_box.delete(1.0, "end")
                self.input_box.insert(1.0, self.input_num)
                self.input_box.configure(state="disabled")
            except:
                clear()
                self.input_box.configure(state="normal")
                self.input_box.insert(1.0,"Error")
                self.input_box.configure(state="disabled")


        def square_root():
            self.input_num
            try:
                result = math.sqrt(float(self.input_num))
                self.input_num = str(result)
                self.input_box.configure(state="normal")
                self.input_box.delete(1.0, "end")
                self.input_box.insert(1.0, self.input_num)
                self.input_box.configure(state="disabled")
            except:
                clear()
                self.input_box.configure(state="normal")
                self.input_box.insert(1.0,"Error")
                self.input_box.configure(state="disabled")


        def backspace():
            self.input_num
            if self.input_num:  
                self.input_num = self.input_num[:-1]  
                self.input_box.configure(state="normal")
                self.input_box.delete(1.0, "end")  
                self.input_box.insert(1.0, self.input_num)  
                self.input_box.configure(state="disabled")



        #   calculator functions end



        # currency convator functions start


        def exc_btn():
            form=self.from_convart_box.get()
            too=self.to_convart_box.get()
            self.from_convart_box.set(too)
            self.to_convart_box.set(form)


        def show_output(ans):
            self.to_lable.configure(state="normal")
            self.to_lable.delete(0, "end")
            self.to_lable.insert(0, ans)
            self.to_lable.configure(state="readonly")


        def convertcurrency():
            
            try:
                self.n=float(self.from_lable.get())
            except:
                self.n=0
            frm = self.from_convart_box.get()
            to = self.to_convart_box.get()
            try:
                ans=self.c.convert(self.n,frm,to)
                ans=round(ans,2)
                show_output(str(ans))
                # to_lable.configure(text=str(ans))
            except:
                if frm =='BDT' or to == 'BDT':
                    if to == 'BDT' and frm != 'BDT':
                        bdt = self.c.convert(self.n,frm)
                        bdt = bdt*131.84                                          #change with the current valu EUR to BDT
                        bdt= round(bdt,2)
                        show_output(str(bdt))
                    elif frm == 'BDT' and to != 'BDT':
                        bdt = self.c.convert(self.n,'EUR',to)
                        bdt = bdt/131.84                                          #change with the current valu EUR to BDT
                        bdt= round(bdt,2)
                        show_output(str(bdt))
                    else:
                        show_output(str(self.n))
                else:
                    show_output("Error")


        # currency convator functions end



        def update_tabs(s_tab):
            self.main_tab.set(tab_names[s_tab])

            for i, (name, btn) in enumerate(tab_buttons.items()):
                if i == s_tab:
                    btn.configure(text=tab_names[i], image=icons[i])
                else:
                    btn.configure(text=" ", image=icons[i])


        # unit converter function start

        def U_exc_btn():
            frm=self.U_from_combbox.get()
            to=self.U_to_combbox.get()
            self.U_from_combbox.set(to)
            self.U_to_combbox.set(frm)


        def length_btn():
            self.unit
            self.unit="length"
            self.U_titel.configure(text="Length")
            self.U_from_combbox.configure(state="normal", values=self.length_units)
            self.U_from_combbox_deopdown.configure(values=self.length_units)
            self.U_to_combbox.configure(state="normal", values=self.length_units)
            self.U_to_combbox_deopdown.configure(values=self.length_units)
            self.U_from_combbox.set(self.length_units[0])
            self.U_to_combbox.set(self.length_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def volume_btn():
            self.unit
            self.unit="volume"
            self.U_titel.configure(text="Volume")
            self.U_from_combbox.configure(state="normal", values=self.volume_units)
            self.U_from_combbox_deopdown.configure(values=self.volume_units)
            self.U_to_combbox.configure(state="normal", values=self.volume_units)
            self.U_to_combbox_deopdown.configure(values=self.volume_units)
            self.U_from_combbox.set(self.volume_units[0])
            self.U_to_combbox.set(self.volume_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def temperature_btn():
            self.unit
            self.unit="temperature"
            self.U_titel.configure(text="Temperature")
            self.U_from_combbox.configure(state="normal", values=self.temperature_units)
            self.U_from_combbox_deopdown.configure(values=self.temperature_units)
            self.U_to_combbox.configure(state="normal", values=self.temperature_units)
            self.U_to_combbox_deopdown.configure(values=self.temperature_units)
            self.U_from_combbox.set(self.temperature_units[0])
            self.U_to_combbox.set(self.temperature_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def time_btn():
            self.unit
            self.unit="time"
            self.U_titel.configure(text="Time")
            self.U_from_combbox.configure(state="normal", values=self.time_units)
            self.U_from_combbox_deopdown.configure(values=self.time_units)
            self.U_to_combbox.configure(state="normal", values=self.time_units)
            self.U_to_combbox_deopdown.configure(values=self.time_units)
            self.U_from_combbox.set(self.time_units[0])
            self.U_to_combbox.set(self.time_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def weight_btn():
            self.unit
            self.unit="weight"
            self.U_titel.configure(text="Weight")
            self.U_from_combbox.configure(state="normal", values=self.weight_units)
            self.U_from_combbox_deopdown.configure(values=self.weight_units)
            self.U_to_combbox.configure(state="normal", values=self.weight_units)
            self.U_to_combbox_deopdown.configure(values=self.weight_units)
            self.U_from_combbox.set(self.weight_units[0])
            self.U_to_combbox.set(self.weight_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def speed_btn():
            self.unit
            self.unit="speed"
            self.U_titel.configure(text="Speed")
            self.U_from_combbox.configure(state="normal", values=self.speed_units)
            self.U_from_combbox_deopdown.configure(values=self.speed_units)
            self.U_to_combbox.configure(state="normal", values=self.speed_units)
            self.U_to_combbox_deopdown.configure(values=self.speed_units)
            self.U_from_combbox.set(self.speed_units[0])
            self.U_to_combbox.set(self.speed_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def data_btn():
            self.unit
            self.unit="data"
            self.U_titel.configure(text="Data")
            self.U_from_combbox.configure(state="normal", values=self.data_units)
            self.U_from_combbox_deopdown.configure(values=self.data_units)
            self.U_to_combbox.configure(state="normal", values=self.data_units)
            self.U_to_combbox_deopdown.configure(values=self.data_units)
            self.U_from_combbox.set(self.data_units[0])
            self.U_to_combbox.set(self.data_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")

        def energy_btn():
            self.unit
            self.unit="energy"
            self.U_titel.configure(text="Energy")
            self.U_from_combbox.configure(state="normal", values=self.energy_units)
            self.U_from_combbox_deopdown.configure(values=self.energy_units)
            self.U_to_combbox.configure(state="normal", values=self.energy_units)
            self.U_to_combbox_deopdown.configure(values=self.energy_units)
            self.U_from_combbox.set(self.energy_units[0])
            self.U_to_combbox.set(self.energy_units[0])
            self.U_from_combbox.configure(state="readonly")
            self.U_to_combbox.configure(state="readonly")


        def U_show_output(ans):
            self.U_to_output_box.configure(state="normal")
            self.U_to_output_box.delete(0, "end")
            self.U_to_output_box.insert(0, ans)
            self.U_to_output_box.configure(state="readonly")


        def unit_convart():
            self.input_val, self.ans
            frm =self.U_from_combbox.get()
            to = self.U_to_combbox.get()
            self.input_val = self.U_from_input_box.get()

            try:
                if(self.unit=="length"):
                    self.ans = converter.convertLength(int(self.input_val), frm, to)
                elif (self.unit=="volume"):
                    self.ans = converter.convertVolume(int(self.input_val), frm, to)
                elif (self.unit=="temperature"):
                    self.ans = converter.convertTemperature(int(self.input_val), frm, to)
                elif (self.unit=="time"):
                    self.ans = converter.convertTime(int(self.input_val), frm, to)
                elif (self.unit=="weight"):
                    self.ans = converter.convertWeight(int(self.input_val), frm, to)
                elif (self.unit=="speed"):
                    self.ans = converter.convertSpeed(int(self.input_val), frm, to)
                elif (self.unit=="data"):
                    self.ans = converter.convertData(int(self.input_val), frm, to)
                elif (self.unit=="energy"):
                    self.ans = converter.convertEnergy(int(self.input_val), frm, to)

                U_show_output(str(round(self.ans,2)))

            except:
                U_show_output("Error")





        self.main_tab = CTkTabview(self.main_cal_windo, width=460, height=573)                           # main tab
        self.main_tab.pack()


        BASE_DIR = Path(__file__).resolve().parent
        icon1_path = BASE_DIR / "image" / "calculator.png"
        icon2_path = BASE_DIR / "image" / "exchange.png"
        icon3_path = BASE_DIR / "image" / "unit-1png.png"


        icon1 = CTkImage(light_image=Image.open(icon1_path), size=(22, 22))
        icon2 = CTkImage(light_image=Image.open(icon2_path), size=(22, 22))
        icon3 = CTkImage(light_image=Image.open(icon3_path), size=(22, 22))

        icons = [icon1, icon2, icon3]
        tab_names = ["Calculator", "Currency Converter", "Unit Converter"]



        self.calculator_tab = self.main_tab.add("Calculator")
        self.currency_converter_tab = self.main_tab.add("Currency Converter")
        self.unit_converter_tab = self.main_tab.add("Unit Converter")



        self.reposition_calculater_frame = CTkFrame(self.calculator_tab, )                                          # calculator start
        self.reposition_calculater_frame.pack()


        self.calculator_fram = CTkFrame(self.reposition_calculater_frame, fg_color="black")
        self.calculator_fram.pack(side="top", expand=True, fill="both")

        self.input_box = CTkTextbox(self.calculator_fram, wrap="none", activate_scrollbars=True, height=70,width=300, state="disabled", fg_color="black",font=self.font_38, text_color="white")
        self.input_box.grid(columnspan=5, pady=10,padx=10)


        self.num_c = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text="C", command=clear, fg_color="#74cec6", text_color="red" )
        self.num_c.grid(row=1, column=1, padx=5, pady=5)
        self.num_open_brackt = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text="(", text_color="black", fg_color="#74cec6", command=lambda :valu_input("("))
        self.num_open_brackt.grid(row=1, column=2, padx=5, pady=5)
        self.num_close_brackt = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text=")", fg_color="#74cec6",  text_color="black", command=lambda :valu_input(")"))
        self.num_close_brackt.grid(row=1, column=3, padx=5, pady=5)


        self.backSpace = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="⌫", text_color="red", fg_color="#74cec6", command=backspace)
        self.backSpace.grid(row=1, column=4, padx=5, pady=5)
        self.Square = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text="x²", fg_color="#0f1320",  command=square)
        self.Square.grid(row=2, column=2, padx=5, pady=5)
        self.Square_root = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_18, text="√", fg_color="#0f1320",  command=square_root)
        self.Square_root.grid(row=2, column=3, padx=5, pady=5)
        self.perCentage = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text="%", fg_color="#0f1320",  command=lambda: (valu_input("%"), percentage()))
        self.perCentage.grid(row=2, column=1, padx=5, pady=5)


        self.num_1 = CTkButton(self.calculator_fram, width=60, height=60 ,font=self.font_16, text="1", fg_color="#0f1320", command=lambda: valu_input("1"))
        self.num_1.grid(row=5, column=1, padx=5, pady=5)
        self.num_2 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="2", fg_color="#0f1320", command=lambda: valu_input("2"))
        self.num_2.grid(row=5, column=2, padx=5, pady=5)
        self.num_3 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="3", fg_color="#0f1320", command=lambda: valu_input("3"))
        self.num_3.grid(row=5, column=3, padx=5, pady=5)
        self.num_4 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="4", fg_color="#0f1320", command=lambda: valu_input("4"))
        self.num_4.grid(row=4, column=1, padx=5, pady=5)
        self.num_5 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="5", fg_color="#0f1320", command=lambda: valu_input("5"))
        self.num_5.grid(row=4, column=2, padx=5, pady=5)
        self.num_6 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="6", fg_color="#0f1320", command=lambda: valu_input("6"))
        self.num_6.grid(row=4, column=3, padx=5, pady=5)
        self.num_7 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="7", fg_color="#0f1320", command=lambda: valu_input("7"))
        self.num_7.grid(row=3, column=1, padx=5, pady=5)
        self.num_8 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="8", fg_color="#0f1320", command=lambda: valu_input("8"))
        self.num_8.grid(row=3, column=2, padx=5, pady=5)
        self.num_9 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="9", fg_color="#0f1320", command=lambda: valu_input("9"))
        self.num_9.grid(row=3, column=3, padx=5, pady=5)
        self.num_0 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="0", fg_color="#0f1320", command=lambda: valu_input("0"))
        self.num_0.grid(row=6, column=2, padx=5, pady=5)
        self.num_0 = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text=".", fg_color="#0f1320", command=lambda: valu_input("."))
        self.num_0.grid(row=6, column=1, padx=5, pady=5)
        self.num_eq = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_16, text="=", fg_color="#0f1320", command=calculation)
        self.num_eq.grid(row=6, column=3, padx=5, pady=5)

        self.num_plus = CTkButton(self.calculator_fram, width=60, height=130,font=self.font_16, text="+", text_color="black", fg_color="#74cec6", command=lambda: valu_input("+"))
        self.num_plus.grid(row=5, column=4,rowspan=2, padx=5, pady=5)
        self.num_minus = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_24, text="-", text_color="black", fg_color="#74cec6", command=lambda: valu_input("-"))
        self.num_minus.grid(row=4, column=4, padx=5, pady=5)
        self.num_mul = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_24, text="*", text_color="black", fg_color="#74cec6", command=lambda: valu_input("*"))
        self.num_mul.grid(row=3, column=4, padx=5, pady=5)
        self.num_div = CTkButton(self.calculator_fram, width=60, height=60,font=self.font_18, text="/", text_color="black", fg_color="#74cec6", command=lambda: valu_input("/"))
        self.num_div.grid(row=2, column=4, padx=5, pady=5)

        # Digit bindings
        for digit in "0123456789":
            self.input_box.bind(digit, lambda event, d=digit: valu_input(d))

        # Decimal point
        self.input_box.bind(".", lambda event: valu_input("."))

        # Operators
        self.input_box.bind("+", lambda event: valu_input("+"))
        self.input_box.bind("-", lambda event: valu_input("-"))
        self.input_box.bind("*", lambda event: valu_input("*"))
        self.input_box.bind("/", lambda event: valu_input("/"))
        self.input_box.bind("%", lambda event: (valu_input("%"), percentage()))

        # Brackets
        self.input_box.bind("(", lambda event: valu_input("("))
        self.input_box.bind(")", lambda event: valu_input(")"))

        # Clear (C or c)
        self.input_box.bind("c", lambda event: clear())
        self.input_box.bind("C", lambda event: clear())

        # Backspace
        self.input_box.bind("<BackSpace>", lambda event: backspace())

        # Square (x or X)
        self.input_box.bind("x", lambda event: square())
        self.input_box.bind("X", lambda event: square())

        # Square root (r or R for √)
        self.input_box.bind("r", lambda event: square_root())
        self.input_box.bind("R", lambda event: square_root())

        # Enter key or = for equals
        self.input_box.bind("<Return>", lambda event: calculation())
        self.input_box.bind("=", lambda event: calculation())

        # calculator end


        # currency convator start


        self.currency_converter_frame = CTkFrame(self.currency_converter_tab )
        self.currency_converter_frame.pack(fill="both", expand=True, side="top")

        self.windo = CTkFrame(self.currency_converter_frame, fg_color="black")
        self.windo.pack(fill="both", expand=True, side="top")

        BASE_DIR = Path(__file__).resolve().parent
        exc_btn_img_black_path = BASE_DIR / "image" / "logo black.png"
        exc_btn_img_white_path = BASE_DIR / "image" / "logo white.png"



        self.exc_btn_img_black = CTkImage(light_image=Image.open(exc_btn_img_black_path),
                               dark_image=Image.open(exc_btn_img_black_path),
                               size=(33,33))
        self.exc_btn_img_white = CTkImage(light_image=Image.open(exc_btn_img_white_path),
                               dark_image=Image.open(exc_btn_img_white_path),
                               size=(33,33))

        self.titel_leble=CTkLabel(self.windo,
                             text="Currency Converter",
                             font=self.font_22)
        self.titel_leble.pack(pady=50)

        self.from_leble=CTkLabel(self.windo,
                             text="FROM",
                             font=self.font_16)
        self.from_leble.place(x=55,y=105)

        self.to_leble=CTkLabel(self.windo,
                             text="TO",
                             font=self.font_16)
        self.to_leble.place(x=270,y=105)

        self.exchange_btn=CTkButton(self.windo,
                               width=20,
                               height=20,
                               border_spacing=0,
                               border_width=0,
                               corner_radius=5,
                               text="",
                               hover_color="black",
                               bg_color="transparent",
                               fg_color="transparent",
                               image=self.exc_btn_img_white,
                               command=exc_btn)
        self.exchange_btn.place(x=223, y=148, anchor="center")

        cuntry = [
            "BDT", "USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", 
            "ISK", "NOK", "TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", 
            "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"
        ]

        self.from_convart_box= CTkComboBox(self.windo,
                                      values=cuntry,
                                      justify='center',
                                      font=self.font_14,
                                      state="readonly")
        self.from_convart_box.set("USD")
        self.from_convart_box.place(x=45,y=135)
        from_box_deopdown = CTkScrollableDropdown(self.from_convart_box, values=cuntry)

        self.to_convart_box=CTkComboBox(self.windo,
                                   values=cuntry,
                                   justify='center',
                                   font=self.font_14,
                                   state="readonly")
        self.to_convart_box.set("BDT")
        self.to_convart_box.place(x=260,y=135)
        self.to_box_deopdown = CTkScrollableDropdown(self.to_convart_box, values=cuntry)

        self.from_lable=CTkEntry(self.windo,
                            font=self.font_12,
                            placeholder_text="Enter Amount",
                            justify='center')
        self.from_lable.place(x=45,y=200)
        self.from_lable.bind("=", lambda event: convertcurrency())
        self.from_lable.bind("<Return>", lambda event: convertcurrency())

        self.to_lable=CTkEntry(self.windo, state="readonly",
                          justify="center",
                          width=140,
                          height=28,
                          fg_color="#343638",
                          bg_color="transparent",
                          font=self.font_14,)
        self.to_lable.place(x=260,y=200)

        self.convart_btn=CTkButton(self.windo,
                              text="Convert",
                              font=self.font_14,
                              command=convertcurrency)
        self.convart_btn.place(x=460/2, y=280, anchor="center")

        # currency converter end


        # add image in tabview "start"

        tab_buttons = self.main_tab._segmented_button._buttons_dict

        for i, (name, btn) in enumerate(tab_buttons.items()):
            btn.configure(text="", image=icons[i], bg_color="transparent", font=self.font_12, border_width=2, border_spacing=4 ) 

        for j, (name, btn) in enumerate(tab_buttons.items()):
            if j == 0:
                btn.configure(text=tab_names[j], image=icons[j])
            else:
                btn.configure(text=" ", image=icons[j])

        for i, btn in enumerate(tab_buttons.values()):
            btn.configure(command=lambda tab_n=i: update_tabs(tab_n))

        # add image in tabview "end"


        # copyright watermark start

        self.copyright_frame = CTkFrame(self.currency_converter_frame, height=8, border_width=0,bg_color="#333333", fg_color="#333333")
        self.copyright_frame.pack(fill="x",side="top")

        copyrights = CTkLabel(self.main_tab, text="© alifjobaer12", font=("Calibri", 11), corner_radius=0, width=1, height=1, fg_color="transparent", bg_color="transparent", text_color="#9e9e9e" )
        copyrights.place(x=450, y=565, anchor="e")

        # copyright watermark end


        # unit converter start

        self.unit_converter_frame_main = CTkFrame(self.unit_converter_tab)
        self.unit_converter_frame_main.pack(fill="both", expand=True, side="top")

        self.unit_converter_frame = CTkFrame(self.unit_converter_frame_main)
        self.unit_converter_frame.pack(fill="both", expand=True, side="top")


        self.U_copyright_frame = CTkFrame(self.unit_converter_frame_main, height=8, border_width=0,bg_color="#333333", fg_color="#333333")
        self.U_copyright_frame.pack(fill="x",side="top")


        self.unit_converter_frame = CTkFrame(self.unit_converter_frame)
        self.unit_converter_frame.pack(fill="both", expand=True)


        self.btn_frame = CTkFrame(self.unit_converter_frame, fg_color="black", width=120, height=500)
        self.btn_frame.pack(fill="both", expand=False, side="left")

        self.converter_frame = CTkFrame(self.unit_converter_frame, fg_color="black", width=280)
        self.converter_frame.pack(fill="both", expand=True, side="right")

        self.btn_frame_middle = CTkFrame(self.btn_frame,corner_radius=0, fg_color="transparent")
        self.btn_frame_middle.pack(fill="x", expand=False, side="left", )


        self.btn_length = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=length_btn, text="Length",)
        self.btn_length.pack(padx=20, pady=7, )
        self.btn_volume = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=volume_btn, text="Volume")
        self.btn_volume.pack(padx=20, pady=7,)
        self.btn_temperature = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=temperature_btn, text="Temperature")
        self.btn_temperature.pack(padx=20, pady=7,)
        self.btn_time = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=time_btn, text="Time")
        self.btn_time.pack(padx=20, pady=7,)
        self.btn_weight = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=weight_btn, text="Weight")
        self.btn_weight.pack(padx=20, pady=7,)
        self.btn_speed = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=speed_btn, text="Speed")
        self.btn_speed.pack(padx=20, pady=7,)
        self.btn_data = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=data_btn, text="Data")
        self.btn_data.pack(padx=20, pady=7,)
        self.btn_energy = CTkButton(self.btn_frame_middle, width=100, font=self.font_12, command=energy_btn, text="Energy")
        self.btn_energy.pack(padx=20, pady=7,)

        self.left_border = CTkFrame(self.btn_frame, width=3, fg_color="#808080") 
        self.left_border.pack(side="right", fill="y")


        self.converter_frame_middle1 = CTkFrame(self.converter_frame, fg_color="transparent", )
        self.converter_frame_middle1.pack(fill="y", expand=True, anchor="center", ipadx=50)

        e = CTkLabel(self.converter_frame_middle1, text="", fg_color="transparent", width=200)
        e.pack()

        self.U_titel = CTkLabel(self.converter_frame_middle1, text="Length",  font=("Helvetica", 30, "bold"), fg_color="transparent")
        self.U_titel.pack(pady=30)

        self.U_from_lable = CTkLabel(self.converter_frame_middle1, justify="center", text="From", font=self.font_16)
        self.U_from_lable.place(x=34, y=135)
        self.U_to_lable = CTkLabel(self.converter_frame_middle1, justify="center", text="To", font=self.font_16)
        self.U_to_lable.place(x=187, y=135)

        self.U_from_combbox = CTkComboBox(self.converter_frame_middle1, justify="center", values=self.length_units, font=self.font_16, width=100, state="readonly" )
        self.U_from_combbox.set(self.length_units[0])
        self.U_from_combbox.place(x=27, y=165)
        self.U_from_combbox_deopdown = CTkScrollableDropdown(self.U_from_combbox, values=self.length_units)

        self.U_to_combbox = CTkComboBox(self.converter_frame_middle1, justify="center", values=self.length_units, font=self.font_16, width=100, state="readonly" )
        self.U_to_combbox.set(self.length_units[0])
        self.U_to_combbox.place(x=180, y=165)
        self.U_to_combbox_deopdown = CTkScrollableDropdown(self.U_to_combbox, values=self.length_units)


        self.U_from_input_box = CTkEntry(self.converter_frame_middle1, justify="center", width=100, font=self.font_14, fg_color="transparent", placeholder_text="Input")
        self.U_from_input_box.place(x=27, y=220.)
        self.U_from_input_box.bind("=", lambda event: unit_convart())
        self.U_from_input_box.bind("<Return>", lambda event: unit_convart())

        self.U_to_output_box = CTkEntry(self.converter_frame_middle1, justify="center", width=100, fg_color="transparent", state="readonly", font=self.font_14)
        self.U_to_output_box.place(x=180, y=220)

        self.U_btn_convert = CTkButton(self.converter_frame_middle1, text="Convert", width=120, font=self.font_16, command=unit_convart)
        self.U_btn_convert.place(x=153.5, y=300, anchor="center")

        self.U_BASE_DIR = Path(__file__).resolve().parent
        self.U_exc_btn_img_black_path = self.U_BASE_DIR / "image" / "logo black.png"
        self.U_exc_btn_img_white_path = self.U_BASE_DIR / "image" / "logo white.png"

        self.U_exc_btn_img_black = CTkImage(light_image=Image.open(self.U_exc_btn_img_black_path),
                                   dark_image=Image.open(self.U_exc_btn_img_black_path),
                                   size=(25,25))
        self.U_exc_btn_img_white = CTkImage(light_image=Image.open(self.U_exc_btn_img_white_path),
                                   dark_image=Image.open(self.U_exc_btn_img_white_path),
                                   size=(23,23))

        self.U_exchange_btn=CTkButton(self.converter_frame_middle1,
                                   width=20,
                                   height=20,
                                   border_spacing=0,
                                   border_width=0,
                                   corner_radius=5,
                                   text="",
                                   hover_color="black",
                                   bg_color="transparent",
                                   fg_color="transparent",
                                   image=self.U_exc_btn_img_white,
                                   command=U_exc_btn)
        self.U_exchange_btn.place(x=135.5,y=166)


if __name__ == "__main__":
    main_cal_windo = CTk()
    # main_cal_windo.geometry("500x600")
    app = MultiUtilityApp(main_cal_windo)
    # main_cal_windo.mainloop()
