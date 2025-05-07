from customtkinter import *
from tkinter import *
from PIL import Image

set_appearance_mode("dark")
set_default_color_theme("blue")

input_num=""


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


def clear():
    global input_num
    input_num = ""
    input_box.configure(state="normal")
    input_box.delete(1.0,"end")
    input_box.configure(state="disabled")


calculate_windo = CTk()
calculate_windo.title("Calculator")
calculate_windo.geometry("327x500")
# calculate_windo.resizable(height=False, width=False)

calculator_fram = CTkFrame(calculate_windo, )
calculator_fram.pack(side="top", expand=False, fill="both")

input_box = CTkTextbox(calculator_fram,height=70,width=300, state="disabled", font=("Helvetica",38,"bold"), text_color="white", bg_color="black")
input_box.grid(columnspan=5, pady=10,padx=10)

# text = ctk.CTkTextbox (frame, wrap="none", activate_scrollbars=True, height=200, width=300)
# text.grid(row=0, column=0, sticky="nsew")


num_c = CTkButton(calculator_fram, width=60, height=60 ,font=("Helvetica",16,"bold"), text="C", command=clear)
num_c.grid(row=1, column=1, padx=5, pady=5)
num_open_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=("Helvetica",16,"bold"), text="(",command=lambda :valu_input("("))
num_open_brackt.grid(row=1, column=2, padx=5, pady=5)
num_close_brackt = CTkButton(calculator_fram, width=60, height=60 ,font=("Helvetica",16,"bold"), text=")",command=lambda :valu_input(")"))
num_close_brackt.grid(row=1, column=3, padx=5, pady=5)

num_1 = CTkButton(calculator_fram, width=60, height=60 ,font=("Helvetica",16,"bold"), text="1",command=lambda: valu_input("1"))
num_1.grid(row=2, column=1, padx=5, pady=5)
num_2 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="2",command=lambda: valu_input("2"))
num_2.grid(row=2, column=2, padx=5, pady=5)
num_3 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="3",command=lambda: valu_input("3"))
num_3.grid(row=2, column=3, padx=5, pady=5)
num_4 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="4",command=lambda: valu_input("4"))
num_4.grid(row=3, column=1, padx=5, pady=5)
num_5 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="5",command=lambda: valu_input("5"))
num_5.grid(row=3, column=2, padx=5, pady=5)
num_6 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="6",command=lambda: valu_input("6"))
num_6.grid(row=3, column=3, padx=5, pady=5)
num_7 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="7",command=lambda: valu_input("7"))
num_7.grid(row=4, column=1, padx=5, pady=5)
num_8 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="8",command=lambda: valu_input("8"))
num_8.grid(row=4, column=2, padx=5, pady=5)
num_9 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="9",command=lambda: valu_input("9"))
num_9.grid(row=4, column=3, padx=5, pady=5)
num_0 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="0",command=lambda: valu_input("0"))
num_0.grid(row=5, column=2, padx=5, pady=5)
num_0 = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text=".",command=lambda: valu_input("."))
num_0.grid(row=5, column=1, padx=5, pady=5)
num_eq = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="=",command=calculation)
num_eq.grid(row=5, column=3, padx=5, pady=5)

num_plus = CTkButton(calculator_fram, width=60, height=130,font=("Helvetica",16,"bold"), text="+",command=lambda: valu_input("+"))
num_plus.grid(row=4, column=4,rowspan=2, padx=5, pady=5)
num_minus = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",24,"bold"), text="-",command=lambda: valu_input("-"))
num_minus.grid(row=3, column=4, padx=5, pady=5)
num_mul = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",24,"bold"), text="*",command=lambda: valu_input("*"))
num_mul.grid(row=2, column=4, padx=5, pady=5)
num_div = CTkButton(calculator_fram, width=60, height=60,font=("Helvetica",16,"bold"), text="/",command=lambda: valu_input("/"))
num_div.grid(row=1, column=4, padx=5, pady=5)



back_calculator_btn = CTkButton(calculator_fram,width=10, height=10,corner_radius=50, text="<", command=calculator_fram.destroy)
back_calculator_btn.place(x=0,y=0)
home_calculator_btn = CTkButton(calculate_windo,width=1, text="Home", bg_color="transparent", fg_color="transparent")
home_calculator_btn.place(x=140, y=460)


calculate_windo.mainloop()