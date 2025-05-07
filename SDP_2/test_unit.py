from customtkinter import *
from CTkScrollableDropdown import CTkScrollableDropdown
from unitconverter import converter
from PIL import Image


unit="length"
input_val=""
ans=""

font_16=font=("Helvetica", 16, "bold")
font_14=font=("Helvetica", 14, "bold")

length_units = ["mm", "cm", "m", "km", "in", "ft", "yd", "mi", "A", "mµ", "µ" ]
weight_units = ["mg", "cg", "dg", "g", "kg", "dag", "hg", "oz.", "lb.","st.", "st", "lt" , "T" ]
energy_units = ["Btu", "thm", "cal", "kcal", "tcal", "MJ", "J", "GJ", "TJ", "Wh", "kWh", "MWh", "GWh", "TWh"]
data_units = ["b", "B", "KB", "Kb", "Mb", "MB", "GB", "Gb", "Tb", "TB"]
speed_units = ["m/s", "km/h", "cm/s", "mph", "ft/s", "yd/s", "mi/s", "knots", "c"]
volume_units = ["ml", "L", "m3", "in3", "ft3", "pt", "qt", "gal", "bbl"]
temperature_units = ["C", "F", "K"]
time_units = ["s", "min", "hr", "day"]

def exc_btn():
    frm=from_combbox.get()
    to=to_combbox.get()
    from_combbox.set(to)
    to_combbox.set(frm)

def length_btn():
    global unit
    unit="length"
    titel.configure(text="Length")
    from_combbox.configure(state="normal", values=length_units)
    from_combbox_deopdown.configure(values=length_units)
    to_combbox.configure(state="normal", values=length_units)
    to_combbox_deopdown.configure(values=length_units)
    from_combbox.set(length_units[0])
    to_combbox.set(length_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")


def volume_btn():
    global unit
    unit="volume"
    titel.configure(text="Volume")
    from_combbox.configure(state="normal", values=volume_units)
    from_combbox_deopdown.configure(values=volume_units)
    to_combbox.configure(state="normal", values=volume_units)
    to_combbox_deopdown.configure(values=volume_units)
    from_combbox.set(volume_units[0])
    to_combbox.set(volume_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def temperature_btn():
    global unit
    unit="temperature"
    titel.configure(text="Temperature")
    from_combbox.configure(state="normal", values=temperature_units)
    from_combbox_deopdown.configure(values=temperature_units)
    to_combbox.configure(state="normal", values=temperature_units)
    to_combbox_deopdown.configure(values=temperature_units)
    from_combbox.set(temperature_units[0])
    to_combbox.set(temperature_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def time_btn():
    global unit
    unit="time"
    titel.configure(text="Time")
    from_combbox.configure(state="normal", values=time_units)
    from_combbox_deopdown.configure(values=time_units)
    to_combbox.configure(state="normal", values=time_units)
    to_combbox_deopdown.configure(values=time_units)
    from_combbox.set(time_units[0])
    to_combbox.set(time_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def weight_btn():
    global unit
    unit="weight"
    titel.configure(text="Weight")
    from_combbox.configure(state="normal", values=weight_units)
    from_combbox_deopdown.configure(values=weight_units)
    to_combbox.configure(state="normal", values=weight_units)
    to_combbox_deopdown.configure(values=weight_units)
    from_combbox.set(weight_units[0])
    to_combbox.set(weight_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def speed_btn():
    global unit
    unit="speed"
    titel.configure(text="Speed")
    from_combbox.configure(state="normal", values=speed_units)
    from_combbox_deopdown.configure(values=speed_units)
    to_combbox.configure(state="normal", values=speed_units)
    to_combbox_deopdown.configure(values=speed_units)
    from_combbox.set(speed_units[0])
    to_combbox.set(speed_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def data_btn():
    global unit
    unit="data"
    titel.configure(text="Data")
    from_combbox.configure(state="normal", values=data_units)
    from_combbox_deopdown.configure(values=data_units)
    to_combbox.configure(state="normal", values=data_units)
    to_combbox_deopdown.configure(values=data_units)
    from_combbox.set(data_units[0])
    to_combbox.set(data_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def energy_btn():
    global unit
    unit="energy"
    titel.configure(text="Energy")
    from_combbox.configure(state="normal", values=energy_units)
    from_combbox_deopdown.configure(values=energy_units)
    to_combbox.configure(state="normal", values=energy_units)
    to_combbox_deopdown.configure(values=energy_units)
    from_combbox.set(energy_units[0])
    to_combbox.set(energy_units[0])
    from_combbox.configure(state="readonly")
    to_combbox.configure(state="readonly")

def show_output(ans):
        to_output_box.configure(state="normal")
        to_output_box.delete(0, "end")
        to_output_box.insert(0, ans)
        to_output_box.configure(state="readonly")

def convart():
    global input_val, ans
    frm = from_combbox.get()
    to = to_combbox.get()
    input_val = from_input_box.get()

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



    pass


root =CTk()

root.geometry("450x500")

root.title("Unit Calculator")



unit_converter_frame = CTkFrame(root)
unit_converter_frame.pack(fill="both", expand=True)


btn_frame = CTkFrame(unit_converter_frame, fg_color="transparent", width=120, height=500)
btn_frame.pack(fill="both", expand=False, side="left")

converter_frame = CTkFrame(unit_converter_frame, fg_color="transparent", width=280)
converter_frame.pack(fill="both", expand=True, side="right")

btn_frame_middle = CTkFrame(btn_frame,corner_radius=0, fg_color="transparent")
btn_frame_middle.pack(fill="x", expand=False, side="left", )


btn_length = CTkButton(btn_frame_middle, width=100, command=length_btn, text="Length",)
btn_length.pack(padx=20, pady=7, )
btn_volume = CTkButton(btn_frame_middle, width=100, command=volume_btn, text="Volume")
btn_volume.pack(padx=20, pady=7,)
btn_temperature = CTkButton(btn_frame_middle, width=100, command=temperature_btn, text="Temperature")
btn_temperature.pack(padx=20, pady=7,)
btn_time = CTkButton(btn_frame_middle, width=100, command=time_btn, text="Time")
btn_time.pack(padx=20, pady=7,)
btn_weight = CTkButton(btn_frame_middle, width=100, command=weight_btn, text="Weight")
btn_weight.pack(padx=20, pady=7,)
btn_speed = CTkButton(btn_frame_middle, width=100, command=speed_btn, text="Speed")
btn_speed.pack(padx=20, pady=7,)
btn_data = CTkButton(btn_frame_middle, width=100, command=data_btn, text="Data")
btn_data.pack(padx=20, pady=7,)
btn_energy = CTkButton(btn_frame_middle, width=100, command=energy_btn, text="Energy")
btn_energy.pack(padx=20, pady=7,)


converter_frame_middle1 = CTkFrame(converter_frame, fg_color="transparent", )
converter_frame_middle1.pack(fill="both", expand=True, anchor="center", ipadx=50)

titel = CTkLabel(converter_frame_middle1, text="Length",  font=("Helvetica", 30, "bold"), fg_color="transparent")
titel.pack(pady=60)

from_lable = CTkLabel(converter_frame_middle1, justify="center", text="From", font=font_16)
from_lable.place(x=37, y=135)
to_lable = CTkLabel(converter_frame_middle1, justify="center", text="To", font=font_16)
to_lable.place(x=187, y=135)

from_combbox = CTkComboBox(converter_frame_middle1, justify="center", values=length_units, font=font_16, width=100, state="readonly" )
from_combbox.set(length_units[0])
from_combbox.place(x=30, y=165)
from_combbox_deopdown = CTkScrollableDropdown(from_combbox, values=length_units)

to_combbox = CTkComboBox(converter_frame_middle1, justify="center", values=length_units, font=font_16, width=100, state="readonly" )
to_combbox.set(length_units[0])
to_combbox.place(x=180, y=165)
to_combbox_deopdown = CTkScrollableDropdown(to_combbox, values=length_units)


from_input_box = CTkEntry(converter_frame_middle1, justify="center", width=100, font=font_14, fg_color="transparent", placeholder_text="Input")
from_input_box.place(x=30, y=220)

to_output_box = CTkEntry(converter_frame_middle1, justify="center", width=100, fg_color="transparent", state="readonly", font=font_14)
to_output_box.place(x=180, y=220)

btn_convert = CTkButton(converter_frame_middle1, text="Convert", width=120, font=font_16, command=convart)
btn_convert.place(x=155, y=300, anchor="center")


exc_btn_img_black = CTkImage(light_image=Image.open('image/logo black.png'),
                           dark_image=Image.open('image/logo black.png'),
                           size=(25,25))
exc_btn_img_white = CTkImage(light_image=Image.open('image/logo white.png'),
                           dark_image=Image.open('image/logo white.png'),
                           size=(23,23))

exchange_btn=CTkButton(converter_frame_middle1,
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
exchange_btn.place(x=137,y=166)




root.mainloop()