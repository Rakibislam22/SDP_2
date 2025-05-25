import customtkinter as ctk
from tkinter import messagebox
import calendar
import datetime
import os

EVENTS_FILE = 'events.txt'

class CalendarApp(ctk.CTkFrame):
    def __init__(self, main_frame, width=600, height=650):
        super().__init__(main_frame, width=width, height=height)
        self.pack_propagate(False)  # Prevent resizing to content

        self.events = {}
        self.load_from_file()

        today = datetime.date.today()
        self.year = today.year
        self.month = today.month
        self.selected_date = today

        # Search bar
        sr = ctk.CTkFrame(self)
        sr.pack(pady=5, anchor='ne', padx=10)
        self.search_entry = ctk.CTkEntry(sr, width=120, placeholder_text="Search")
        self.search_entry.pack(side=ctk.LEFT, padx=(0, 5))
        ctk.CTkButton(sr, text="🔍", width=30, command=self.search_notes).pack(side=ctk.LEFT)

        # Header with month navigation
        hdr = ctk.CTkFrame(self)
        hdr.pack(pady=10)
        ctk.CTkButton(hdr, text="<<", width=30, command=self.prev_month).pack(side=ctk.LEFT, padx=5)
        self.title_lbl = ctk.CTkLabel(hdr, text="", width=200)
        self.title_lbl.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(hdr, text=">>", width=30, command=self.next_month).pack(side=ctk.LEFT, padx=5)

        # Calendar
        self.cal_frame = ctk.CTkFrame(self)
        self.cal_frame.pack()

        # Notes section
        na = ctk.CTkFrame(self)
        na.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(na, text="Day Note:").pack(anchor='w')
        self.note_text = ctk.CTkTextbox(na, height=80)
        self.note_text.pack(fill="x")

        btn_frame = ctk.CTkFrame(na)
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="Save Note", command=self.save_event).pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Delete Note", command=self.delete_event).pack(side=ctk.LEFT, padx=5)

        # Footer
        ctk.CTkLabel(self, text="© Jubaer Rahman", text_color='gray').pack(side=ctk.BOTTOM, pady=5)

        self.default_text_color = "#FFFFFF"

        self.draw_calendar()
        self.on_date_click(self.selected_date)

    def draw_calendar(self):
        today = datetime.date.today()
        for w in self.cal_frame.winfo_children():
            w.destroy()

        self.title_lbl.configure(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, d in enumerate(days):
            ctk.CTkLabel(self.cal_frame, text=d, width=50).grid(row=0, column=i, padx=2, pady=2)
 
        weekend_color = "#FF6961"

        mc = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(mc, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    ctk.CTkLabel(self.cal_frame, text="", width=50, height=55).grid(row=r, column=c)
                else:
                    d_obj = datetime.date(self.year, self.month, day)

                    btn = ctk.CTkButton(
                        self.cal_frame,
                        text=f"{day}",
                        width=50,
                        height=50,
                        fg_color="transparent",
                        #border_width=2,
                        #border_color="#13638B",
                        command=lambda d=d_obj: self.on_date_click(d)
                    )

                    if d_obj.isoformat() in self.events :
                        btn.configure(border_width=3, border_color="#95A508")

                    btn.configure(
                        text_color=("red" if c in [5, 6] else self.default_text_color),
                        font=("Arial", 15),
                        hover=False
                    )

                    if d_obj == today:
                        btn.configure(fg_color="#3676A6")

                    if d_obj == self.selected_date:
                        btn.configure(border_width=3, border_color="#0DBC5C")

                    btn.grid(row=r, column=c, padx=1, pady=1)

    
    def mode_c(self, mode):
        ctk.set_appearance_mode(mode)  # Handles "light", "dark", or "system"
        self.default_text_color = "#000000" if mode == "light" else "#FFFFFF"
        self.draw_calendar()


    def prev_month(self):
        if self.month == 1:
            self.month, self.year = 12, self.year - 1
        else:
            self.month -= 1
        self.selected_date = None
        self.note_text.delete('1.0', 'end')
        self.draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month, self.year = 1, self.year + 1
        else:
            self.month += 1
        self.selected_date = None
        self.note_text.delete('1.0', 'end')
        self.draw_calendar()

    def on_date_click(self, date_obj):
        self.selected_date = date_obj
        self.note_text.delete('1.0', 'end')
        self.note_text.insert('end', self.events.get(date_obj.isoformat(), ''))
        self.draw_calendar()

    def save_event(self):
        if not self.selected_date:
            return
        nk = self.selected_date.isoformat()
        txt = self.note_text.get('1.0', 'end').strip()
        if txt:
            self.events[nk] = txt
        else:
            self.events.pop(nk, None)
        self.write_to_file()
        messagebox.showinfo("Saved", f"Note saved for {nk}")
        self.draw_calendar()

    def delete_event(self):
        if not self.selected_date:
            return
        nk = self.selected_date.isoformat()
        if nk in self.events:
            del self.events[nk]
            self.write_to_file()
            self.note_text.delete('1.0', 'end')
            messagebox.showinfo("Deleted", f"Note deleted for {nk}")
            self.draw_calendar()

    def move_selection(self, days):
        base = self.selected_date or datetime.date.today()
        new = base + datetime.timedelta(days=days)
        self.year, self.month = new.year, new.month
        self.on_date_click(new)

    def write_to_file(self):
        with open(EVENTS_FILE, 'w') as f:
            for d, n in self.events.items():
                f.write(f"{d}:{n}\n")

    def load_from_file(self):
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE) as f:
                for ln in f:
                    if ':' in ln:
                        d, n = ln.strip().split(':', 1)
                        self.events[d] = n

    def search_notes(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            return
        for date_str, note in self.events.items():
            if keyword in note.lower():
                y, m, d = map(int, date_str.split('-'))
                self.year, self.month = y, m
                self.on_date_click(datetime.date(y, m, d))
                return
        messagebox.showinfo("Not found", f"No notes containing: {keyword}")


if __name__ == "__main__":
    
    root = ctk.CTk()
    app = CalendarApp(root)
