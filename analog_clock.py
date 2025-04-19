import customtkinter as ctk
from tkinter import Canvas
from datetime import datetime
import math

class AnalogClock(ctk.CTkFrame):
    def __init__(self, master=None, size=200, **kwargs):
        super().__init__(master, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = self.center - 10

        self.canvas = Canvas(self, width=size, height=size, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.update_clock()

    def draw_hand(self, angle_deg, length, width, color):
        angle_rad = math.radians(angle_deg)
        x = self.center + length * math.sin(angle_rad)
        y = self.center - length * math.cos(angle_rad)
        return self.canvas.create_line(self.center, self.center, x, y, width=width, fill=color)

    def update_clock(self):
        self.canvas.delete("all")

        # Draw clock face
        self.canvas.create_oval(5, 5, self.size - 5, self.size - 5, outline="black", width=2)

        # Draw hour marks
        for i in range(12):
            angle = math.radians(i * 30)
            x1 = self.center + (self.radius - 10) * math.sin(angle)
            y1 = self.center - (self.radius - 10) * math.cos(angle)
            x2 = self.center + self.radius * math.sin(angle)
            y2 = self.center - self.radius * math.cos(angle)
            self.canvas.create_line(x1, y1, x2, y2, width=2)

        now = datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second

        # Calculate angles
        hour_angle = (h + m / 60) * 30
        min_angle = (m + s / 60) * 6
        sec_angle = s * 6

        # Draw hands
        self.draw_hand(hour_angle, self.radius * 0.5, 5, "black")
        self.draw_hand(min_angle, self.radius * 0.7, 3, "blue")
        self.draw_hand(sec_angle, self.radius * 0.9, 1, "red")

        self.after(1000, self.update_clock)
