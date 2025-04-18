import customtkinter as ctk
import math
import time

class Analoge(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analog Clock")
        self.geometry("720x720")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")  # Options: "light", "dark", or "system"

        self.canvas_size = 700
        self.radius = 250

        self.canvas = ctk.CTkCanvas(self, width=self.canvas_size, height=self.canvas_size, bg=None, highlightthickness=0)
        self.canvas.pack(pady=10)

        self.elements = [0 for _ in range(5)]

        self.draw_clock_face()
        self.draw()  # Start drawing clock hands

    def calculate(self, _angle, _radius):
        x = math.cos(math.radians(_angle)) * _radius + self.canvas_size / 2
        y = math.sin(math.radians(_angle)) * _radius + self.canvas_size / 2
        return x, y

    def line(self, _x1, _y1, _x2, _y2, _width, _color):
        return self.canvas.create_line(_x1, _y1, _x2, _y2, width=_width, fill=_color, capstyle="round")

    def line_from_center(self, _x, _y, _width, _color):
        return self.line(self.canvas_size / 2, self.canvas_size / 2, _x, _y, _width, _color)

    def text(self, _x, _y, _text, _color):
        return self.canvas.create_text(_x, _y, text=_text, fill=_color, font=("PT Sans", 20, "bold"), justify="center")

    def draw_clock_face(self):
        angle = 270
        for i in range(12):
            x, y = self.calculate(angle, self.radius - 45)
            self.text(x, y, str(i + 1), "#478fb3")
            angle += 360 / 12

        angle = 270
        for i in range(60):
            if i % 5 == 0:
                x1, y1 = self.calculate(angle, self.radius - 10)
                width = 5
            else:
                x1, y1 = self.calculate(angle, self.radius)
                width = 3
            x2, y2 = self.calculate(angle, self.radius + 10)
            self.line(x1, y1, x2, y2, width, "#334780")
            angle += 360 / 60

    def draw(self):
        for element in self.elements:
            self.canvas.delete(element)

        tm = time.localtime()

        # Hour hand
        x, y = self.calculate((360 / 12) * tm.tm_hour + (360 / 12 / 60) * tm.tm_min - 90, self.radius - 90)
        self.elements[1] = self.line_from_center(x, y, 12, "#8c2a4b")

        # Minute hand
        x, y = self.calculate((360 / 60) * tm.tm_min + (360 / 60 / 60) * tm.tm_sec - 90, self.radius - 40)
        self.elements[2] = self.line_from_center(x, y, 7, "#2a8c7c")

        # Second hand
        x1, y1 = self.calculate((360 / 60) * tm.tm_sec + 90, self.radius - 200)
        x2, y2 = self.calculate((360 / 60) * tm.tm_sec - 90, self.radius - 30)
        self.elements[3] = self.line(x1, y1, x2, y2, 4, "#2a638c")

        # Center dot
        self.elements[4] = self.canvas.create_oval(
            self.canvas_size / 2 - 10, self.canvas_size / 2 - 10,
            self.canvas_size / 2 + 10, self.canvas_size / 2 + 10,
            fill="#405b80", width=0
        )

        self.after(1000, self.draw)  # Redraw every second


# Run the app
if __name__ == "__main__":
    clock = Analoge()
    clock.mainloop()
