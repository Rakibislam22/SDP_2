from customtkinter import *
from CTkScrollableDropdown import CTkScrollableDropdown
from unitconverter import converter
from PIL import Image
from pathlib import Path


# U_exchange_btn = None
# U_BASE_DIR = Path(__file__).resolve().parent
# U_exc_btn_img_black_path = U_BASE_DIR / "image" / "logo black.png"
# U_exc_btn_img_white_path = U_BASE_DIR / "image" / "logo white.png"
# U_exc_btn_img_black = CTkImage(light_image=Image.open(U_exc_btn_img_black_path),
#                            dark_image=Image.open(U_exc_btn_img_black_path),
#                            size=(25,25))
# U_exc_btn_img_white = CTkImage(light_image=Image.open(U_exc_btn_img_white_path),
#                            dark_image=Image.open(U_exc_btn_img_white_path),
#                            size=(23,23))


def unit_con(root, mode):

    global U_exchange_btn

    unit="length"
    input_val=""
    ans=""

    font_12=font=("Helvetica", 12, "bold")
    font_14=font=("Helvetica", 14, "bold")
    font_16=font=("Helvetica", 16, "bold")

    length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi", "A", "mµ", "µ" ]
    weight_units = ["mg", "cg", "dg", "g", "kg", "dag", "hg", "oz.", "lb.","st.", "st", "lt" , "T" ]
    energy_units = ["Btu", "thm", "cal", "kcal", "tcal", "MJ", "J", "GJ", "TJ", "Wh", "kWh", "MWh", "GWh", "TWh"]
    data_units = ["b", "B", "KB", "Kb", "Mb", "MB", "GB", "Gb", "Tb", "TB"]
    speed_units = ["m/s", "km/h", "cm/s", "mph", "ft/s", "yd/s", "mi/s", "knots", "c"]
    volume_units = ["ml", "L", "m3", "in3", "ft3", "pt", "qt", "gal", "bbl"]
    temperature_units = ["C", "F", "K"]
    time_units = ["s", "min", "hr", "day"]

    def exc_btn():
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

    def show_output(ans):
            U_to_output_box.configure(state="normal")
            U_to_output_box.delete(0, "end")
            U_to_output_box.insert(0, ans)
            U_to_output_box.configure(state="readonly")

    def convart():
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

            show_output(str(round(ans,2)))

        except:
            show_output("Error")






    unit_converter_frame = CTkFrame(root)
    unit_converter_frame.pack(fill="both", expand=True)


    btn_frame = CTkFrame(unit_converter_frame, fg_color="transparent", width=120, height=500)
    btn_frame.pack(fill="both", expand=False, side="left")

    converter_frame = CTkFrame(unit_converter_frame, fg_color="transparent", width=280)
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

    left_border = CTkFrame(btn_frame, width=3, fg_color="#808080")  # Customize width/color
    left_border.pack(side="right", fill="y")



    converter_frame_middle1 = CTkFrame(converter_frame, fg_color="transparent", )
    converter_frame_middle1.pack(fill="y", expand=True, anchor="center", ipadx=50)

    e = CTkLabel(converter_frame_middle1, text="", fg_color="transparent", width=205)
    e.pack()

    U_titel = CTkLabel(converter_frame_middle1, text="Length",  font=("Helvetica", 30, "bold"), fg_color="transparent")
    U_titel.pack(pady=30)

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

    U_btn_convert = CTkButton(converter_frame_middle1, text="Convert", width=120, font=font_16, command=convart)
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
                               command=exc_btn)
    U_exchange_btn.place(x=135.5,y=166)



    # if mode == "light":
    #     U_exchange_btn.configure(fg_color="transparent",
    #                            hover_color="white",
    #                            image=exc_btn_img_black)
    #     mode ="dark"

    # elif mode == "dark":
    #     U_exchange_btn.configure(fg_color="transparent",
    #                            hover_color="black",
    #                            image=U_exc_btn_img_white)
    #     mode ="light"

# def change(mode):
#     if mode == "light":
#         U_exchange_btn.configure(fg_color="transparent",
#                                hover_color="white",
#                                image=exc_btn_img_black)
#         mode ="dark"
#     elif mode == "dark":
#         U_exchange_btn.configure(fg_color="transparent",
#                                hover_color="black",
#                                image=U_exc_btn_img_white)
#         mode ="light"


# root =CTk()
# root.geometry("450x500")
# root.title("Unit Calculator")

# unit_con(root)

# root.mainloop()