import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, Toplevel
import random
import pygame
from pathlib import Path
import math
import colorsys

class CustomCTk(ctk.CTk):
    def block_update_dimensions_event(self):
        pass  # Override to prevent scaling errors

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color='transparent')

        # Disable customtkinter scaling
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        # Initialize pygame mixer
        pygame.mixer.init()
        self.background_music_path = Path(__file__).resolve().parent / "sound" / "Gmusic.mp3"
        self.button_sound_path = Path(__file__).resolve().parent / "sound" / "G_click.mp3"

        try:
            pygame.mixer.music.load(self.background_music_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            pass#print(f"Error loading background music: {e}")

        try:
            self.button_sound = pygame.mixer.Sound(self.button_sound_path)
        except pygame.error as e:
            #print(f"Error loading button sound: {e}")
            self.button_sound = None

        # Color scheme
        self.bg_color = "#222222"
        self.frame_color = "transparent"
        self.popup_color = "#333333"
        self.text_color = "#FFFFFF"
        self.accent_color = "#00FFFF"
        self.secondary_color = "#FFD700"
        self.button_color = "#2F4F4F"
        self.button_hover = "#5F9EA0"

        # Game state
        self.player_round_wins = 0  # For PvC
        self.computer_round_wins = 0
        self.player1_round_wins = 0  # For PvP
        self.player2_round_wins = 0
        self.board = [""] * 9
        self.game_active = True
        self.current_level = None
        self.game_mode = None  # "pvc" or "pvp"
        self.game_count = 0
        self.player_name = ""
        self.player2_name = ""
        self.current_player = 1  # 1 for X, 2 for O in PvP
        self.rounds_played = 0
        self.current_round = 1
        self.max_rounds = 5  # Default, will be set by user
        self.current_screen = None

        # Animation variables
        self.glow_elements = []
        self.glow_phase = 0
        self.particles = []
        self.popup_anim_phase = 0
        self.grid_anim_states = [0] * 9
        self.grid_glow_ids = [None] * 9
        self.transition_alpha = 1.0

        self.setup_ui()
        self.start_animations()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color,
            bg_color=self.bg_color
        )
        self.main_frame.pack(fill='both', expand=True)

        self.particle_canvas = tk.Canvas(
            self.main_frame,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.particle_canvas.place(relwidth=1, relheight=1)
        self.particles = []

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            bg_color="transparent"
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        self.show_welcome_screen()

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def start_animations(self):
        self.animate_glow()
        self.animate_particles()
        self.animate_grid_buttons()
        self.animate_screen_transition()

    def animate_glow(self):
        self.glow_phase = (self.glow_phase + 0.05) % (2 * math.pi)
        intensity = (math.sin(self.glow_phase) + 1) / 2

        for element, base_color, is_label in self.glow_elements:
            try:
                base_rgb = tuple(int(base_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                h, s, v = colorsys.rgb_to_hsv(base_rgb[0]/255, base_rgb[1]/255, base_rgb[2]/255)
                v = min(1.0, v + intensity * 0.3)
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                glow_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                if is_label:
                    element.configure(text_color=glow_color)
                else:
                    element.configure(fg_color=glow_color)
            except Exception:
                continue

        self.root.after(50, self.animate_glow)

    def animate_particles(self):
        self.particle_canvas.delete("particle")
        new_particles = []
        for particle in self.particles:
            x, y, vx, vy, age, ptype, size = particle
            x += vx
            y += vy
            age += 1
            if 0 <= x <= 500 and 0 <= y <= 450 and age < 100:
                new_particles.append([x, y, vx, vy, age, ptype, size])
                if ptype == "star":
                    color = "#FFD700"
                    self.particle_canvas.create_oval(
                        x-size, y-size, x+size, y+size,
                        fill=color,
                        outline="",
                        tags="particle"
                    )
                elif ptype == "spark":
                    color = "#00FFFF"
                    self.particle_canvas.create_line(
                        x, y, x+vx*2, y+vy*2,
                        fill=color,
                        width=size/2,
                        tags="particle"
                    )
                else:  # Glow
                    color = "#00AAAA"
                    self.particle_canvas.create_oval(
                        x-size*1.5, y-size*1.5, x+size*1.5, y+size*1.5,
                        fill=color,
                        outline="",
                        tags="particle"
                    )

        if random.random() < 0.4:
            x = random.randint(0, 500)
            y = random.randint(0, 450)
            vx = random.uniform(-1.5, 1.5)
            vy = random.uniform(-1.5, 1.5)
            ptype = random.choice(["star", "spark", "glow"])
            size = random.uniform(2, 4)
            new_particles.append([x, y, vx, vy, 0, ptype, size])

        self.particles = new_particles[:30]
        self.particle_canvas.lower("particle")
        self.root.after(50, self.animate_particles)

    def animate_grid_buttons(self):
        if self.current_screen != "game":
            self.root.after(50, self.animate_grid_buttons)
            return

        for i, state in enumerate(self.grid_anim_states):
            if state > 0:
                self.grid_anim_states[i] = max(0, state - 0.1)
                scale = 1.0 + self.grid_anim_states[i] * 0.2
                try:
                    self.grid_buttons[i].configure(width=int(70 * scale), height=int(70 * scale))
                    if self.grid_glow_ids[i]:
                        self.particle_canvas.delete(self.grid_glow_ids[i])
                    if state > 0:
                        color = "#00FFFF" if self.board[i] == "X" else "#FF0000"
                        x = 175 + (i % 3) * 80 + 40
                        y = 230 + (i // 3) * 80 + 40
                        size = 30 * state
                        self.grid_glow_ids[i] = self.particle_canvas.create_oval(
                            x-size, y-size, x+size, y+size,
                            outline=color,
                            width=1,
                            tags="particle"
                        )
                except Exception:
                    pass

        self.root.after(50, self.animate_grid_buttons)

    def animate_screen_transition(self):
        if self.transition_alpha > 0:
            self.transition_alpha = max(0, self.transition_alpha - 0.03)
            try:
                self.content_frame.configure(fg_color="#000000")
            except Exception:
                pass
        self.root.after(50, self.animate_screen_transition)

    def show_welcome_screen(self):
        self.current_screen = "welcome"
        self.current_round = 1
        self.player_round_wins = 0
        self.computer_round_wins = 0
        self.player1_round_wins = 0
        self.player2_round_wins = 0
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Tic Tac Toe",
            font=("Arial", 28, "bold"),  # Changed from Poppins to Arial
            text_color=self.accent_color
        )
        title_label.pack(pady=5)
        self.glow_elements.append((title_label, self.accent_color, True))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", border_color=self.secondary_color, border_width=2)
        input_frame.pack(pady=10)

        self.name_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type Your Name, Warrior! ⚔️",
            font=("Arial", 16),  # Changed from Roboto to Arial
            width=180,
            fg_color=self.button_color,
            text_color=self.text_color
        )
        self.name_entry.pack(pady=8, padx=10)
        self.name_entry.bind("<KeyRelease>", self.check_name_input)
        self.name_entry.bind("<Return>", self.enter_bind)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Game 🚀",
            command=lambda: [self.play_button_sound(), self.show_mode_selection_screen()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#00FF00",
            hover_color="#32CD32",
            text_color="black",
            corner_radius=10,
            width=100,
            state="disabled"
        )
        self.start_btn.pack(pady=5)
        self.glow_elements.append((self.start_btn, "#00FF00", False))

        self.create_footer()

    def check_name_input(self, event):
        self.player_name = self.name_entry.get().strip()
        if self.player_name:
            self.start_btn.configure(state="normal")
            self.name_entry.bind("<Return>", self.enter_bind)
        else:
            self.start_btn.configure(state="disabled")

    def enter_bind(self, event=None):
        self.play_button_sound()
        self.show_mode_selection_screen()

    def show_mode_selection_screen(self):
        self.current_screen = "mode_selection"
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Choose Game Mode",
            font=("Arial", 24, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        title_label.pack(pady=5)
        self.glow_elements.append((title_label, self.secondary_color, True))

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.pvc_btn = ctk.CTkButton(
            button_frame,
            text="Player vs Computer 👾",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_round_selection_screen("pvc")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#00FF00",
            hover_color="#32CD32",
            corner_radius=10,
            width=100
        )
        self.pvc_btn.pack(pady=5)
        self.glow_elements.append((self.pvc_btn, "#00FF00", False))

        self.pvp_btn = ctk.CTkButton(
            button_frame,
            text="Player vs Player ⚔️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_pvp_start_screen()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#FFA500",
            hover_color="#FFB6C1",
            corner_radius=10,
            width=100
        )
        self.pvp_btn.pack(pady=5)
        self.glow_elements.append((self.pvp_btn, "#FFA500", False))

        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_welcome_screen()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=100
        )
        self.back_btn.pack(pady=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.create_footer()

    def show_pvp_start_screen(self):
        self.current_screen = "pvp_start"
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Player vs Player Mode",
            font=("Arial", 24, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        title_label.pack(pady=5)
        self.glow_elements.append((title_label, self.secondary_color, True))

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.pvp_start_btn = ctk.CTkButton(
            button_frame,
            text="Start PvP Game 🚀",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_pvp_name_input()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#FFA500",
            hover_color="#FFB6C1",
            corner_radius=10,
            width=100
        )
        self.pvp_start_btn.pack(pady=5)
        self.glow_elements.append((self.pvp_start_btn, "#FFA500", False))

        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_mode_selection_screen()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=100
        )
        self.back_btn.pack(pady=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.create_footer()

    def show_pvp_name_input(self):
        self.current_screen = "pvp_name"
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Enter Player 2's Name",
            font=("Arial", 24, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        title_label.pack(pady=5)
        self.glow_elements.append((title_label, self.secondary_color, True))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", border_color=self.secondary_color, border_width=2)
        input_frame.pack(pady=10)

        self.player2_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type Player 2's Name! 🛡️",
            font=("Arial", 16),  # Changed from Roboto to Arial
            width=180,
            fg_color=self.button_color,
            text_color=self.text_color
        )
        self.player2_entry.pack(pady=8, padx=10)
        self.player2_entry.bind("<KeyRelease>", self.check_player2_input)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.pvp_start_btn = ctk.CTkButton(
            button_frame,
            text="Proceed to Rounds 🚀",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_round_selection_screen("pvp")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#FFA500",
            hover_color="#FFB6C1",
            corner_radius=10,
            width=100,
            state="disabled"
        )
        self.pvp_start_btn.pack(pady=5)
        self.glow_elements.append((self.pvp_start_btn, "#FFA500", False))

        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_pvp_start_screen()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=100
        )
        self.back_btn.pack(pady=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.create_footer()

    def check_player2_input(self, event):
        self.player2_name = self.player2_entry.get().strip()
        if self.player2_name:
            self.pvp_start_btn.configure(state="normal")
        else:
            self.pvp_start_btn.configure(state="disabled")

    def show_round_selection_screen(self, mode):
        self.game_mode = mode
        self.current_screen = "round_selection"
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Select Number of Rounds",
            font=("Arial", 24, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        title_label.pack(pady=5)
        self.glow_elements.append((title_label, self.secondary_color, True))

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", border_color=self.secondary_color, border_width=2)
        input_frame.pack(pady=10)

        self.rounds_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter number of rounds (1-10)",
            font=("Arial", 16),  # Changed from Roboto to Arial
            width=180,
            fg_color=self.button_color,
            text_color=self.text_color
        )
        self.rounds_entry.pack(pady=8, padx=10)
        self.rounds_entry.bind("<KeyRelease>", self.check_rounds_input)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.rounds_start_btn = ctk.CTkButton(
            button_frame,
            text="Start Game 🚀",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.set_rounds()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#00FF00",
            hover_color="#32CD32",
            corner_radius=10,
            width=100,
            state="disabled"
        )
        self.rounds_start_btn.pack(pady=5)
        self.glow_elements.append((self.rounds_start_btn, "#00FF00", False))

        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_mode_selection_screen() if mode == "pvc" else self.show_pvp_name_input()],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=100
        )
        self.back_btn.pack(pady=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.create_footer()

    def check_rounds_input(self, event):
        rounds_input = self.rounds_entry.get().strip()
        try:
            rounds = int(rounds_input)
            if 1 <= rounds <= 10:
                self.max_rounds = rounds
                self.rounds_start_btn.configure(state="normal")
            else:
                self.rounds_start_btn.configure(state="disabled")
        except ValueError:
            self.rounds_start_btn.configure(state="disabled")

    def set_rounds(self):
        if self.game_mode == "pvc":
            self.show_level_selection_screen()
        else:
            self.current_player = 1
            self.reset_full_game()
            self.show_game_screen()

    def show_level_selection_screen(self):
        self.current_screen = "level_selection"
        self.glow_elements = []
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        title_frame.pack(fill='x', pady=10)

        self.level_label = ctk.CTkLabel(
            title_frame,
            text="Select Difficulty Level",
            font=("Arial", 24, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        self.level_label.pack(pady=5)
        self.glow_elements.append((self.level_label, self.secondary_color, True))

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.beginner_btn = ctk.CTkButton(
            button_frame,
            text="Beginner 😊",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.set_level("beginner")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#00FF00",
            hover_color="#32CD32",
            corner_radius=10,
            width=100
        )
        self.beginner_btn.pack(pady=5)
        self.glow_elements.append((self.beginner_btn, "#00FF00", False))

        self.medium_btn = ctk.CTkButton(
            button_frame,
            text="Medium 😎",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.set_level("medium")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#FFA500",
            hover_color="#FFB6C1",
            corner_radius=10,
            width=100
        )
        self.medium_btn.pack(pady=5)
        self.glow_elements.append((self.medium_btn, "#FFA500", False))

        self.hard_btn = ctk.CTkButton(
            button_frame,
            text="Hard 😈",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.set_level("hard")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#FF0000",
            hover_color="#FF4500",
            corner_radius=10,
            width=100
        )
        self.hard_btn.pack(pady=5)
        self.glow_elements.append((self.hard_btn, "#FF0000", False))

        self.back_btn = ctk.CTkButton(
            button_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_round_selection_screen("pvc")],
            font=("Arial", 16),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=100
        )
        self.back_btn.pack(pady=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.create_footer()

    def set_level(self, level):
        self.current_level = level
        # Perform a full game reset to ensure clean state
        self.board = [""] * 9
        self.game_active = True
        self.player_round_wins = 0
        self.computer_round_wins = 0
        self.player1_round_wins = 0
        self.player2_round_wins = 0
        self.game_count = 0
        self.rounds_played = 0
        self.current_round = 1
        self.current_player = 1  # Reset for PvP consistency
        self.grid_anim_states = [0] * 9
        self.grid_glow_ids = [None] * 9
        self.glow_elements = []
        #print(f"Game state reset for level {level}: Board={self.board}, Active={self.game_active}, Round={self.current_round}")
        self.show_game_screen()

    def show_game_screen(self):
        self.current_screen = "game"
        self.glow_elements = []
        self.grid_anim_states = [0] * 9
        self.grid_glow_ids = [None] * 9
        self.transition_alpha = 1.0
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Ensure board and game state are fresh
        self.board = [""] * 9
        self.game_active = True
        #print(f"Showing game screen: Mode={self.game_mode}, Level={self.current_level}, Round={self.current_round}, Board={self.board}")

        status_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        status_frame.pack(fill='x', pady=5)

        if self.game_mode == "pvc":
            result_text = f"Level: {self.current_level.capitalize()} | Round: {self.current_round}/{self.max_rounds} | {self.player_name}'s Move!"
        else:
            result_text = f"Round: {self.current_round}/{self.max_rounds} | Player {self.current_player}'s Move!"
        self.result_label = ctk.CTkLabel(
            status_frame,
            text=result_text,
            font=("Arial", 16, "bold"),  # Changed from Poppins to Arial
            text_color=self.accent_color
        )
        self.result_label.pack(pady=5)
        self.glow_elements.append((self.result_label, self.accent_color, True))

        score_text = (f"Round Wins - {self.player_name}: {self.player_round_wins} | Computer: {self.computer_round_wins}"
                      if self.game_mode == "pvc"
                      else f"Round Wins - {self.player_name}: {self.player1_round_wins} | {self.player2_name}: {self.player2_round_wins}")
        self.score_label = ctk.CTkLabel(
            status_frame,
            text=score_text,
            font=("Arial", 14, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        self.score_label.pack(pady=5)
        self.glow_elements.append((self.score_label, self.secondary_color, True))

        self.grid_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.grid_frame.pack(pady=10)
        self.grid_buttons = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.grid_frame,
                text="",
                text_color="black",
                command=lambda idx=i: self.play(idx),
                font=("Arial", 28, "bold"),  # Changed from Roboto to Arial
                fg_color=self.button_color,
                hover_color=self.button_hover,
                text_color_disabled="#A9A9A9",
                width=70,
                height=70,
                corner_radius=8,
                state="normal"
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.grid_buttons.append(btn)
            self.glow_elements.append((btn, self.button_color, False))

        control_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        control_frame.pack(pady=10)

        self.back_btn = ctk.CTkButton(
            control_frame,
            text="Back ↩️",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.show_level_selection_screen() if self.game_mode == "pvc" else self.show_round_selection_screen("pvp")],
            font=("Arial", 14),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=90
        )
        self.back_btn.pack(side="left", padx=5)
        self.glow_elements.append((self.back_btn, "#1E90FF", False))

        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="Reset",
            text_color="black",
            command=lambda: [self.play_button_sound(), self.reset_full_game()],
            font=("Arial", 14),  # Changed from Roboto to Arial
            fg_color="#FFA500",
            hover_color="#FFB6C1",
            corner_radius=10,
            width=90
        )
        self.reset_btn.pack(side="left", padx=5)
        self.glow_elements.append((self.reset_btn, "#FFA500", False))


        self.create_footer()
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()

    def show_round_result_popup(self, result, color, winner):
        popup = ctk.CTkToplevel(self.root)
        popup.geometry("300x200")
        popup.transient(self.root)
        popup.configure(fg_color=self.popup_color)
        popup.title("Round Result")
        popup.bind("<Button-1>", lambda e: self.close_round_popup(popup))
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_round_popup(popup))

        self.popup_anim_phase = 0
        score_alpha = 0
        def animate_popup():
            if not popup.winfo_exists():
                return
            self.popup_anim_phase += 0.1
            nonlocal score_alpha
            score_alpha = min(1.0, score_alpha + 0.05)
            slide = min(1.0, self.popup_anim_phase)
            shake = math.sin(self.popup_anim_phase * 5) * (1 - slide) * 5
            glow_intensity = (math.sin(self.popup_anim_phase) + 1) / 2
            try:
                popup.geometry(f"300x200+{int(self.root.winfo_x() + 100 + shake)}+{int(self.root.winfo_y() + slide * 100)}")
                result_label.configure(font=("Arial", 18 + int(slide * 2), "bold"))  # Changed from Poppins to Arial
                popup.configure(fg_color=f"#{int(51 + glow_intensity*20):02x}{int(51 + glow_intensity*20):02x}{int(51 + glow_intensity*20):02x}")
            except Exception:
                return
            if slide < 1.0 or score_alpha < 1.0:
                self.root.after(20, animate_popup)

        popup.grab_set()
        popup_frame = ctk.CTkFrame(popup, fg_color="transparent")
        popup_frame.pack(fill='both', expand=True, padx=10, pady=10)

        result_label = ctk.CTkLabel(
            popup_frame,
            text=f"{result}\nClick anywhere to continue 🕹️",
            font=("Arial", 18, "bold"),  # Changed from Poppins to Arial
            text_color=color,
            wraplength=250
        )
        result_label.pack(pady=10)
        self.glow_elements.append((result_label, color, True))

        animate_popup()

    def close_round_popup(self, popup):
        self.play_button_sound()
        popup.grab_release()
        popup.destroy()
        if self.current_round <= self.max_rounds:
            self.reset_game()
        else:
            self.show_final_result_popup()

    def show_final_result_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.geometry("300x250")
        popup.transient(self.root)
        popup.configure(fg_color=self.popup_color)
        popup.title("Final Result")

        self.popup_anim_phase = 0
        score_alpha = 0

        def animate_popup():
            if not popup.winfo_exists():
                return
            self.popup_anim_phase += 0.1
            nonlocal score_alpha
            score_alpha = min(1.0, score_alpha + 0.05)
            slide = min(1.0, self.popup_anim_phase)
            shake = math.sin(self.popup_anim_phase * 5) * (1 - slide) * 5
            glow_intensity = (math.sin(self.popup_anim_phase) + 1) / 2

            # CENTER POSITION
            popup_width, popup_height = 300, 200
            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()
            parent_width = self.root.winfo_width()
            parent_height = self.root.winfo_height()

            center_x = parent_x + (parent_width - popup_width) // 2 + int(shake)
            center_y = parent_y + (parent_height - popup_height) // 2 + int(slide * 20)

            try:
                popup.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
                result_label.configure(font=("Arial", 18 + int(slide * 2), "bold"))
                popup.configure(fg_color=f"#{int(51 + glow_intensity*20):02x}"*3)
            except Exception:
                return

            if slide < 1.0 or score_alpha < 1.0:
                self.root.after(20, animate_popup)


        def play_again():
            self.play_button_sound()
            popup.grab_release()
            popup.destroy()
            self.reset_full_game()

        def back_to_selection():
            self.play_button_sound()
            popup.grab_release()
            popup.destroy()
            if self.game_mode == "pvc":
                self.show_level_selection_screen()
            else:
                self.show_round_selection_screen("pvp")

        popup.grab_set()
        popup_frame = ctk.CTkFrame(popup, fg_color="transparent")
        popup_frame.pack(fill='both', expand=True, padx=10, pady=10)

        if self.game_mode == "pvc":
            if self.player_round_wins > self.computer_round_wins:
                result = f"{self.player_name} is the Champion!"
                color = "#00FF00"
                emoji = "🏆🎉✨"
            elif self.computer_round_wins > self.player_round_wins:
                result = "Computer is the Champion!"
                color = "#FF0000"
                emoji = "😈💥🔥"
            else:
                result = "It's a Tie!"
                color = "#FFA500"
                emoji = "⚔️🤝🎯"
            score_text = f"Round Wins\n{self.player_name}: {self.player_round_wins} | Computer: {self.computer_round_wins}"
        else:
            if self.player1_round_wins > self.player2_round_wins:
                result = f"{self.player_name} is the Champion!"
                color = "#00FF00"
                emoji = "🏆🎉✨"
            elif self.player2_round_wins > self.player1_round_wins:
                result = f"{self.player2_name} is the Champion!"
                color = "#FF0000"
                emoji = "🏆🎉🔥"
            else:
                result = "It's a Tie!"
                color = "#FFA500"
                emoji = "⚔️🤝🎯"
            score_text = f"Round Wins\n{self.player_name}: {self.player1_round_wins} | {self.player2_name}: {self.player2_round_wins}"

        result_label = ctk.CTkLabel(
            popup_frame,
            text=f"{result}\n{emoji}",
            font=("Arial", 18, "bold"),  # Changed from Poppins to Arial
            text_color=color,
            wraplength=250
        )
        score_label = ctk.CTkLabel(
            popup_frame,
            text=score_text,
            font=("Arial", 14, "bold"),  # Changed from Poppins to Arial
            text_color=self.secondary_color
        )
        result_label.pack(pady=10)
        score_label.pack(pady=10)
        self.glow_elements.append((result_label, color, True))
        self.glow_elements.append((score_label, self.secondary_color, True))

        button_frame = ctk.CTkFrame(popup_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        play_again_btn = ctk.CTkButton(
            button_frame,
            text="Play Again 🔄",
            text_color="black",
            command=play_again,
            font=("Arial", 14),  # Changed from Roboto to Arial
            fg_color="#00FF00",
            hover_color="#32CD32",
            corner_radius=10,
            width=90
        )
        play_again_btn.pack(side="left", padx=5)
        self.glow_elements.append((play_again_btn, "#00FF00", False))

        back_btn = ctk.CTkButton(
            button_frame,
            text="Back to Selection",
            text_color="black",
            command=back_to_selection,
            font=("Arial", 14),  # Changed from Roboto to Arial
            fg_color="#1E90FF",
            hover_color="#4682B4",
            corner_radius=10,
            width=90
        )
        back_btn.pack(side="left", padx=5)
        self.glow_elements.append((back_btn, "#1E90FF", False))

        animate_popup()

    def create_footer(self):
        footer_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer_frame.pack(side='bottom', fill='x', pady=5)

        self.footer_label = ctk.CTkLabel(
            footer_frame,
            text="(c) Copyright 2025 Ishan.",
            font=("Arial", 8),  # Changed from Poppins to Arial
            text_color=("gray70", "gray30")
        )
        self.footer_label.pack(side='left', expand=True)


    def play(self, index):
        if not self.game_active or self.board[index] != "":
            #print(f"Play blocked: Active={self.game_active}, Board[{index}]={self.board[index]}")
            return

        if self.game_mode == "pvc":
            self.board[index] = "X"
            self.grid_buttons[index].configure(text="X", text_color="#00FF00", state="disabled")
            self.grid_anim_states[index] = 1.0
            result = self.check_game_over()
            #print(f"Player move {index}, Board: {self.board}, Result: {result}")
            if result != "continue":
                self.display_result()
            else:
                # Delay computer move to ensure UI updates
                self.root.after(500, self.computer_move)
        else:  # pvp
            symbol = "X" if self.current_player == 1 else "O"
            color = "#00FF00" if self.current_player == 1 else "#FF0000"
            self.board[index] = symbol
            self.grid_buttons[index].configure(text=symbol, text_color=color, state="disabled")
            self.grid_anim_states[index] = 1.0
            result = self.check_game_over()
            #print(f"Player {self.current_player} move {index}, Board: {self.board}, Result: {result}")
            if result != "continue":
                self.display_result()
            else:
                self.current_player = 2 if self.current_player == 1 else 1
                self.result_label.configure(
                    text=f"Round: {self.current_round}/{self.max_rounds} | Player {self.current_player}'s Move!",
                    text_color=self.accent_color
                )

    def computer_move(self):
        if not self.game_active:
            #print("Computer move blocked: Game not active")
            return

        available_moves = [i for i in range(9) if self.board[i] == ""]
        if not available_moves:
            #print("No available moves, Board:", self.board)
            return

        if self.current_level == "beginner":
            best_move = random.choice(available_moves)
        elif self.current_level == "medium":
            self.game_count += 1
            if random.random() < 0.7:
                best_score = -float('inf')
                best_move = None
                original_board = self.board.copy()
                for i in available_moves:
                    self.board[i] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i] = ""
                    if score > best_score:
                        best_score = score
                        best_move = i
                self.board = original_board.copy()
                if best_move is None:
                    #print("Medium: No best move found, falling back to random")
                    best_move = random.choice(available_moves)
            else:
                best_move = random.choice(available_moves)
        else:  # Hard level
            best_score = -float('inf')
            best_move = None
            original_board = self.board.copy()
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i] = ""
                    if score > best_score:
                        best_score = score
                        best_move = i
                    elif score == best_score and best_move is None:
                        best_move = i
            self.board = original_board.copy()
            if best_move is None:
                best_move = random.choice(available_moves)

        #print(f"Computer selecting move {best_move}, Board before: {self.board}")
        self.board[best_move] = "O"
        self.grid_buttons[best_move].configure(text="O", text_color="#FF0000", state="disabled")
        self.grid_anim_states[best_move] = 1.0
        #print(f"Computer move {best_move}, Board after: {self.board}")
        # Delay result check to ensure UI updates
        self.root.after(500, self.check_and_display_result)

    def check_and_display_result(self):
        result = self.check_game_over()
        #print(f"Checking result after computer move, Board: {self.board}, Result: {result}")
        if result != "continue":
            self.display_result()
        else:
            self.result_label.configure(
                text=f"Level: {self.current_level.capitalize()} | Round: {self.current_round}/{self.max_rounds} | {self.player_name}'s Move!",
                text_color=self.accent_color
            )

    def minimax(self, board, depth, is_maximizing):
        result = self.check_game_over()
        if result == "win":
            return 1 - depth * 0.1
        if result == "tie":
            return 0
        if result == "lose":
            return -1 + depth * 0.1

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def check_game_over(self):
        #print(f"Checking game over, Board: {self.board}")
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != "":
                #print(f"Win detected in row {i//3}: {self.board[i]}")
                if self.game_mode == "pvc":
                    return "win" if self.board[i] == "O" else "lose"
                else:
                    return "player1_win" if self.board[i] == "X" else "player2_win"
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != "":
                #print(f"Win detected in column {i}: {self.board[i]}")
                if self.game_mode == "pvc":
                    return "win" if self.board[i] == "O" else "lose"
                else:
                    return "player1_win" if self.board[i] == "X" else "player2_win"
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != "":
            #print(f"Win detected in diagonal (0,4,8): {self.board[0]}")
            if self.game_mode == "pvc":
                return "win" if self.board[0] == "O" else "lose"
            else:
                return "player1_win" if self.board[0] == "X" else "player2_win"
        if self.board[2] == self.board[4] == self.board[6] != "":
            #print(f"Win detected in diagonal (2,4,6): {self.board[2]}")
            if self.game_mode == "pvc":
                return "win" if self.board[2] == "O" else "lose"
            else:
                return "player1_win" if self.board[2] == "X" else "player2_win"
        # Check for tie
        if all(cell != "" for cell in self.board):
            #print("Tie detected")
            return "tie"
        #print("Game continues")
        return "continue"

    def display_result(self):
        self.game_active = False
        self.rounds_played += 1
        result_state = self.check_game_over()
        #print(f"Displaying result, Round: {self.current_round}, Board: {self.board}, Result: {result_state}")

        if self.game_mode == "pvc":
            if result_state == "win":
                result = f"PC Wins Round {self.current_round}! 😈"
                self.computer_round_wins += 1
                color = "#FF0000"
                winner = "Computer"
            elif result_state == "lose":
                result = f"{self.player_name} Wins Round {self.current_round}! 🎉"
                self.player_round_wins += 1
                color = "#00FF00"
                winner = self.player_name
            else:
                result = f"Round {self.current_round} is a Tie! 🤝"
                color = "#FFA500"
                winner = None
        else:
            if result_state == "player1_win":
                result = f"{self.player_name} Wins Round {self.current_round}! 🎉"
                self.player1_round_wins += 1
                color = "#00FF00"
                winner = self.player_name
            elif result_state == "player2_win":
                result = f"{self.player2_name} Wins Round {self.current_round}! 🎉"
                self.player2_round_wins += 1
                color = "#FF0000"
                winner = self.player2_name
            else:
                result = f"Round {self.current_round} is a Tie! 🤝"
                color = "#FFA500"
                winner = None

        self.result_label.configure(text=result, text_color=color)
        self.update_score_display()
        for btn in self.grid_buttons:
            btn.configure(state="disabled")

        # Increment round after updating result
        self.current_round += 1
        # Show popup after a slight delay to ensure UI updates
        self.root.after(500, lambda: self.show_round_result_popup(result, color, winner))

    def update_score_display(self):
        score_text = (f"Round Wins - {self.player_name}: {self.player_round_wins} | Computer: {self.computer_round_wins}"
                      if self.game_mode == "pvc"
                      else f"Round Wins - {self.player_name}: {self.player1_round_wins} | {self.player2_name}: {self.player2_round_wins}")
        self.score_label.configure(
            text=score_text,
            text_color=self.secondary_color
        )

    def reset_game(self):
        self.board = [""] * 9
        self.game_active = True
        self.grid_anim_states = [0] * 9
        self.grid_glow_ids = [None] * 9
        if self.game_mode == "pvp":
            self.current_player = 1
        #print(f"Reset game: Board={self.board}, Active={self.game_active}, Player={self.current_player}")
        self.show_game_screen()

    def reset_full_game(self):
        self.board = [""] * 9
        self.game_active = True
        self.current_round = 1
        self.player_round_wins = 0
        self.computer_round_wins = 0
        self.player1_round_wins = 0
        self.player2_round_wins = 0
        self.game_count = 0
        self.rounds_played = 0
        self.grid_anim_states = [0] * 9
        self.grid_glow_ids = [None] * 9
        if self.game_mode == "pvp":
            self.current_player = 1
        #print(f"Full game reset: Board={self.board}, Round={self.current_round}, Wins={self.player_round_wins}/{self.computer_round_wins}")
        self.show_game_screen()


def launch_tictactoe(parent_frame):
    frame = ctk.CTkFrame(parent_frame,width=650,height=600)
    frame.pack(fill="both", expand=True)
    frame.pack_propagate(False)
    TicTacToeApp(frame)
    return frame