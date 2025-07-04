import customtkinter as ctk
import random
from tkinter import messagebox, TclError
import math
import pygame
import time
from pathlib import Path

class RockPaperScissorsApp:
    BUTTON_CLICK_SOUND = Path(__file__).resolve().parent / "sound" / "G_click.mp3"
    BACKGROUND_MUSIC = Path(__file__).resolve().parent / "sound" / "Gmusic.mp3"

    def __init__(self, root):
        ###print("Initializing RockPaperScissorsApp")
        try:
            pygame.mixer.init()
        except pygame.error as e:
            pass##print(f"Error initializing pygame.mixer: {e}")
        self.music_playing = False
        self.click_sound = None
        self.load_sounds()
        self.play_background_music()

        self.root = root
        # self.root.geometry("600x450")
        # self.root.title("Rock Paper Scissors Deluxe")
        #self.root.resizable(False, False)
        self.is_animating = False
        self.last_click_time = 0
        self.click_cooldown = 0.5
        self.is_running = True
        self.after_ids = []
        self.animated_widgets = []

        self.choices = ["Rock", "Paper", "Scissors"]
        self.player_score = 0
        self.computer_score = 0
        self.current_round = 1
        self.max_rounds = 5
        self.round_wins = {'player': 0, 'computer': 0}
        self.player_name = None


        self.welcome_background_canvas = ctk.CTkCanvas(self.root, width=200, height=50, bg="#1C2526", highlightthickness=0)
        self.welcome_background_canvas.pack(fill="both", expand=True, pady=(20,0))
        self.root.update_idletasks()

        self.main_container_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container_frame.pack(fill='both', expand=True)
        self.root.update_idletasks()

        self.setup_welcome_screen()

    def load_sounds(self):
        try:
            self.click_sound = pygame.mixer.Sound(self.BUTTON_CLICK_SOUND)
            ##print("Button click sound loaded")
        except pygame.error as e:
            pass#print(f"Error loading button click sound '{self.BUTTON_CLICK_SOUND}': {e}, skipping sound")

    def play_background_music(self):
        try:
            pygame.mixer.music.load(self.BACKGROUND_MUSIC)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
            self.music_playing = True
            #print("Background music started")
        except pygame.error as e:
            pass#print(f"Error playing background music '{self.BACKGROUND_MUSIC}': {e}, skipping music")

    def stop_background_music(self):
        if self.music_playing:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                ##print("Background music stopped")
            except pygame.error as e:
                pass##print(f"Error stopping background music: {e}")

    def ease_out_sine(self, t):
        return math.sin((t * math.pi) / 2)

    def cancel_animations(self):
        #print("Cancelling animations")
        for after_id in self.after_ids[:]:  # Copy to avoid modifying while iterating
            try:
                self.root.after_cancel(after_id)
                self.after_ids.remove(after_id)
            except TclError:
                pass
        for widget in self.animated_widgets[:]:
            try:
                if widget.winfo_exists():
                    widget.configure(hover=False)
                self.animated_widgets.remove(widget)
            except TclError:
                pass
        #print("All animations cancelled")

    def clear_main_ui(self):
        #print("Clearing main UI")
        self.cancel_animations()
        try:
            if hasattr(self, 'welcome_background_canvas') and self.welcome_background_canvas.winfo_exists():
                self.welcome_background_canvas.destroy()
            if hasattr(self, 'round_input_frame') and self.round_input_frame.winfo_exists():
                self.round_input_frame.destroy()
            if hasattr(self, 'game_over_popup') and self.game_over_popup.winfo_exists():
                self.game_over_popup.destroy()
            for widget in self.main_container_frame.winfo_children():
                try:
                    if widget.winfo_exists():
                        widget.destroy()
                        #print(f"Destroyed widget: {widget}")
                except TclError as e:
                    pass#print(f"TclError destroying widget {widget}: {e}")
            self.main_container_frame.pack_forget()
            self.main_container_frame = ctk.CTkFrame(self.root, fg_color="transparent")
            self.main_container_frame.pack(fill='both', expand=True)
            self.root.update_idletasks()
            #print("Main UI cleared")
        except Exception as e:
            pass#print(f"Error in clear_main_ui: {e}")

    def draw_confetti(self, canvas):
        emojis = ['🎉', '✨', '🌟', '🎊']
        for _ in range(10):
            x = random.randint(0, canvas.winfo_width())
            y = random.randint(0, canvas.winfo_height() // 2)
            emoji = random.choice(emojis)
            canvas.create_text(x, y, text=emoji, font=("Arial", 16), fill="white")

    def draw_particles(self, canvas, player_type, progress):
        if not canvas.winfo_exists():
            return
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        x_offset = canvas_width * 0.25 if player_type == "player" else canvas_width * 0.75
        y_offset = canvas_height * 0.5
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 30) * progress
            size = random.uniform(1, 4)
            x = x_offset + distance * math.cos(angle)
            y = y_offset + distance * math.sin(angle)
            alpha = max(0, 1 - progress)
            color = f"#{(int(255 * alpha)):02x}{(int(255 * alpha)):02x}ff"
            canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")

    def create_glowing_button(self, master, text, command, fg_color, hover_color, width=100, height=30, text_color="#FFFFFF"):
        def wrapped_command():
            current_time = time.time()
            if current_time - self.last_click_time < self.click_cooldown:
                return
            self.last_click_time = current_time
            if self.click_sound:
                try:
                    self.click_sound.play()
                except pygame.error as e:
                    pass#print(f"Error playing button click sound: {e}")
            try:
                command()
            except Exception as e:
                pass#print(f"Error executing command for button {text}: {e}")

        glowing_button = ctk.CTkButton(
            master,
            text=text,
            command=wrapped_command,
            font=("Impact", 12, "bold"),
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color,
            corner_radius=8,
            border_color="#FFFFFF",
            border_width=1,
            width=width,
            height=height
        )
        self.animated_widgets.append(glowing_button)
        glowing_button._pulse_after_id = None

        def pulse(step=0):
            if not self.is_running or not glowing_button.winfo_exists():
                return
            try:
                if text in ["Start Game", "Reset", "Rock", "Paper", "Scissors"]:
                    scale = 1.0 + 0.05 * math.sin(step * 0.1 * math.pi)
                    glowing_button.configure(width=int(width * scale), height=int(height * scale))
                glowing_button._pulse_after_id = glowing_button.after(100, lambda: pulse(step + 1))
                self.after_ids.append(glowing_button._pulse_after_id)
            except TclError:
                pass

        def custom_destroy():
            try:
                if glowing_button._pulse_after_id:
                    glowing_button.after_cancel(glowing_button._pulse_after_id)
                    self.after_ids.remove(glowing_button._pulse_after_id) if glowing_button._pulse_after_id in self.after_ids else None
                if glowing_button in self.animated_widgets:
                    self.animated_widgets.remove(glowing_button)
                ctk.CTkButton.destroy(glowing_button)
            except TclError as e:
                pass#print(f"TclError in custom_destroy for button {text}: {e}")

        glowing_button.destroy = custom_destroy

        if text in ["Start Game", "Reset", "Rock", "Paper", "Scissors"]:
            pulse()
        return glowing_button

    def draw_gesture(self, canvas, gesture, player_type, progress):
        if not canvas.winfo_exists():
            return
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        x_offset = canvas_width * 0.25 if player_type == "player" else canvas_width * 0.75
        y_offset = canvas_height * 0.5
        eased = self.ease_out_sine(progress)
        scale_factor = 0.8 + 0.5 * eased * (1 + 0.2 * math.sin(progress * 4 * math.pi))
        alpha = min(1.0, progress * 2)
        color_intensity = int(255 * alpha)
        glow_intensity = int(255 * (0.5 + 0.4 * math.sin(progress * 6 * math.pi)))

        self.draw_particles(canvas, player_type, progress)

        if gesture == "Rock":
            radius = 25 * scale_factor
            color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"
            glow_color = f"#{glow_intensity:02x}{glow_intensity:02x}ff"
            canvas.create_oval(x_offset - radius - 5, y_offset - radius - 5, x_offset + radius + 5,
                               y_offset + radius + 5, outline=glow_color, width=4)
            canvas.create_oval(x_offset - radius - 3, y_offset - radius - 3, x_offset + radius + 3,
                               y_offset + radius + 3, outline="#FFFFFF", width=3)
            canvas.create_oval(x_offset - radius, y_offset - radius, x_offset + radius, y_offset + radius, fill=color,
                               outline="#FFD700", width=2)
            canvas.create_text(x_offset, y_offset + 30, text="✊", font=("Arial", int(20 * scale_factor)), fill="#FFD700")

        elif gesture == "Paper":
            size = 35 * scale_factor
            color = f"#{color_intensity:02x}{color_intensity:02x}ff"
            glow_color = f"#{glow_intensity:02x}ff{glow_intensity:02x}"
            canvas.create_rectangle(x_offset - size / 2 - 5, y_offset - size / 2 - 5, x_offset + size / 2 + 5,
                                    y_offset + size / 2 + 5, outline=glow_color, width=4)
            canvas.create_rectangle(x_offset - size / 2 - 3, y_offset - size / 2 - 3, x_offset + size / 2 + 3,
                                    y_offset + size / 2 + 3, outline="#FFFFFF", width=3)
            canvas.create_rectangle(x_offset - size / 2, y_offset - size / 2, x_offset + size / 2, y_offset + size / 2,
                                    fill=color, outline="#00FFFF", width=2)
            canvas.create_text(x_offset, y_offset + 30, text="📄", font=("Arial", int(20 * scale_factor)), fill="#00FFFF")

        elif gesture == "Scissors":
            angle = 15 * math.sin(progress * 3 * math.pi)
            color = f"#{color_intensity:02x}0000"
            glow_color = f"#ff{glow_intensity:02x}{glow_intensity:02x}"
            line_width = 5
            canvas.create_line(x_offset, y_offset, x_offset + 30 * scale_factor * math.cos(math.radians(angle)),
                               y_offset + 30 * scale_factor * math.sin(math.radians(angle)), width=line_width + 2,
                               fill=glow_color)
            canvas.create_line(x_offset, y_offset, x_offset + 30 * scale_factor * math.cos(math.radians(-angle)),
                               y_offset + 30 * scale_factor * math.sin(math.radians(-angle)), width=line_width + 2,
                               fill=glow_color)
            canvas.create_line(x_offset, y_offset, x_offset + 25 * scale_factor * math.cos(math.radians(angle)),
                               y_offset + 25 * scale_factor * math.sin(math.radians(angle)), width=line_width,
                               fill=color)
            canvas.create_line(x_offset, y_offset, x_offset + 25 * scale_factor * math.cos(math.radians(-angle)),
                               y_offset + 25 * scale_factor * math.sin(math.radians(-angle)), width=line_width,
                               fill=color)
            canvas.create_text(x_offset, y_offset + 30, text="✂️", font=("Arial", int(20 * scale_factor)), fill="#FF4500")

    def setup_welcome_screen(self):
        #print("Setting up welcome screen")
        try:
            self.clear_main_ui()
            self.welcome_background_canvas = ctk.CTkCanvas(self.root, width=200, height=50, bg="#1C2526", highlightthickness=0)
            self.welcome_background_canvas.pack(fill="both", expand=True, pady=(20,0))
            self.welcome_content_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
            self.welcome_content_frame.pack(expand=True, fill='both', pady=0, anchor="center")
            self.root.update_idletasks()
            #print("Welcome content frame created")

            self.welcome_title_label = ctk.CTkLabel(self.welcome_content_frame,
                                              text="🎮 Rock Paper Scissors Deluxe! ✨",
                                              font=("Impact", 34, "bold"),
                                              text_color="#FFD700")
            self.welcome_title_label.pack(pady=(0, 20))

            self.welcome_tagline_label = ctk.CTkLabel(self.welcome_content_frame,
                                         text="Are You Ready to Battle? ⚔️",
                                         font=("jell", 14, "italic"),
                                         text_color="#FF69B4")
            self.welcome_tagline_label.pack(pady=10)

            self.name_input_container_frame = ctk.CTkFrame(self.welcome_content_frame, fg_color="transparent")
            self.name_input_container_frame.pack(pady=(0, 10))

            self.player_name_entry = ctk.CTkEntry(self.name_input_container_frame,
                                           placeholder_text="Enter Your Name, Warrior!",
                                           font=("jell", 14, "bold"),
                                           width=250,
                                           height=35,
                                           fg_color="#2A2A2A",
                                           border_color="#00FFFF",
                                           border_width=2,
                                           text_color="#FFFFFF",
                                           corner_radius=8)
            self.player_name_entry.pack()
            self.player_name_entry.bind("<Return>", lambda event: self.submit_name())
            self.player_name_entry.focus_set()
            #print("Player name entry created")

            self.start_button_container_frame = ctk.CTkFrame(self.welcome_content_frame, fg_color="transparent")
            self.start_button_container_frame.pack(pady=(20, 0))

            self.start_game_button = self.create_glowing_button(self.start_button_container_frame,
                                               "Start Game",
                                               self.submit_name,
                                               "#00CED1",
                                               "#0097A7",
                                               width=150,
                                               height=40)
            self.start_game_button.pack(side='left', padx=10)
            #print("Start game button created")


            self.welcome_gesture_icon = self.welcome_background_canvas.create_text(self.welcome_background_canvas.winfo_width() / 2,
                                                           self.welcome_background_canvas.winfo_height() * 0.2,
                                                           text="✊", font=("Arial", 40), fill="#00FFFF")
            self.gesture_step = 0
            self.animate_gesture_icon()

            self.root.update()
            #print("Welcome screen setup complete")
        except TclError as e:
            pass#print(f"TclError in setup_welcome_screen: {e}")
        

    def animate_gesture_icon(self):
        if not self.is_running or not self.welcome_background_canvas.winfo_exists():
            return
        self.gesture_step += 1
        try:
            self.welcome_background_canvas.delete(self.welcome_gesture_icon)
            gestures = ["✊", "📄", "✂️"]
            current_gesture = gestures[self.gesture_step % 3]
            angle = self.gesture_step * 5
            canvas_width = self.welcome_background_canvas.winfo_width()
            canvas_height = self.welcome_background_canvas.winfo_height()
            self.welcome_gesture_icon = self.welcome_background_canvas.create_text(canvas_width / 2, canvas_height * 0.2,
                                                           text=current_gesture, font=("Arial", 40), fill="#00FFFF",
                                                           angle=angle)
            after_id = self.welcome_background_canvas.after(150, self.animate_gesture_icon)
            self.after_ids.append(after_id)
        except TclError as e:
            pass #print(f"TclError animating gesture icon: {e}")
        except Exception as e:
            pass #print(f"Error animating gesture icon: {e}")

    def submit_name(self):
        #print("submit_name called")
        try:
            name = self.player_name_entry.get().strip()
            if not name:
                #print("Empty name entered")
                messagebox.showwarning("Input Error", "Please enter your name, warrior!")
                return
            self.player_name = name
            #print(f"Player name set to: {self.player_name}")
            self.prompt_rounds()
        except TclError as e:
            pass#print(f"TclError in submit_name: {e}")
        except Exception as e:
            pass#print(f"Error in submit_name: {e}")

    def prompt_rounds(self):
        #print("prompt_rounds called")
        try:
            if hasattr(self, 'welcome_content_frame') and self.welcome_content_frame.winfo_exists():
                self.welcome_content_frame.pack_forget()
                #print("Welcome content frame hidden")

            self.round_input_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
            self.round_input_frame.pack(expand=True, fill='both', pady=0, anchor="center")
            #print("Round input frame created")

            title_label = ctk.CTkLabel(self.round_input_frame,
                                       text="🎮 Enter Number of Rounds! 🎲",
                                       font=("Impact", 34, "bold"),
                                       text_color="#FFD700")
            title_label.pack(pady=(0, 20))

            tagline_label = ctk.CTkLabel(self.round_input_frame,
                                         text="How Many Rounds Will You Battle? (1-100)",
                                         font=("jell", 14, "italic"),
                                         text_color="#FF69B4")
            tagline_label.pack(pady=10)

            self.rounds_entry = ctk.CTkEntry(self.round_input_frame,
                                             placeholder_text="Enter Rounds (e.g., 5)",
                                             font=("jell", 14, "bold"),
                                             width=250,
                                             height=35,
                                             fg_color="#2A2A2A",
                                             border_color="#00FFFF",
                                             border_width=2,
                                             text_color="#FFFFFF",
                                             corner_radius=8)
            self.rounds_entry.pack(pady=(0, 10))
            self.rounds_entry.bind("<Return>", lambda event: self.submit_rounds())
            self.rounds_entry.focus_set()
            #print("Rounds entry created")

            self.submit_rounds_button = self.create_glowing_button(self.round_input_frame,
                                                                  "Submit Rounds",
                                                                  self.submit_rounds,
                                                                  "#00CED1",
                                                                  "#0097A7",
                                                                  width=150,
                                                                  height=40)
            self.submit_rounds_button.pack(pady=(20, 0))
            #print("Submit rounds button created")

            self.root.update_idletasks()
            self.root.update()
            #print("Round input UI updated")
        except TclError as e:
            pass#print(f"TclError in prompt_rounds: {e}")
        except Exception as e:
            #print(f"Error in prompt_rounds: {e}")
            messagebox.showerror("Error", f"Failed to show round input: {e}")

    def submit_rounds(self):
        #print("submit_rounds called")
        try:
            rounds = int(self.rounds_entry.get().strip())
            if rounds < 1 or rounds > 100:
                #print("Invalid rounds entered")
                messagebox.showwarning("Input Error", "Please enter a number between 1 and 100!")
                return
            self.max_rounds = rounds
            #print(f"max_rounds set to: {self.max_rounds}")
            self.start_game()
        except ValueError:
            #print("Non-numeric rounds entered")
            messagebox.showwarning("Input Error", "Please enter a valid number!")
        except TclError as e:
            pass#print(f"TclError in submit_rounds: {e}")
        except Exception as e:
            #print(f"Error in submit_rounds: {e}")
            messagebox.showerror("Error", f"Failed to submit rounds: {e}")

    def start_game(self):
        #print("start_game called")
        try:
            self.clear_main_ui()
            self.is_running = True
            self.main_container_frame.configure(fg_color="#1C2526")
            self.setup_top_panel()
            self.setup_game_canvas()
            self.setup_round_info()
            self.setup_choice_buttons_panel()
            self.setup_control_buttons_panel()
            self.setup_commentator()
            self.setup_footer()
            self.init_result_label()
            self.enable_choice_buttons()
            self.update_score_display()
            self.root.update()
            #print("Game UI set up")
        except TclError as e:
            pass#print(f"TclError in start_game: {e}")
        except Exception as e:
            pass#print(f"Error in start_game: {e}")

    def init_result_label(self):
        self.game_result_label = ctk.CTkLabel(self.main_container_frame,
                                         text="Choose Your Move!",
                                         font=("Impact", 16, "bold"),
                                         text_color="#00FFFF")
        self.game_result_label.pack(pady=10)

    def setup_top_panel(self):
        #print("Setting up top panel")
        self.top_info_panel_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
        self.top_info_panel_frame.pack(fill='x', pady=(10, 0))

        self.game_title_label = ctk.CTkLabel(self.top_info_panel_frame,
                                        text="🎮 Rock Paper-Scissors ✨",
                                        font=("Impact", 30, "bold"),
                                        text_color="#FFD700")
        self.game_title_label.pack()

        self.info_container_frame = ctk.CTkFrame(self.top_info_panel_frame, fg_color="transparent")
        self.info_container_frame.pack(pady=(5, 10), fill='x')

        display_name = self.player_name if self.player_name else "—"
        self.player_name_label = ctk.CTkLabel(self.info_container_frame,
                                       text=f"Player: {display_name}",
                                       font=("jell", 20),
                                       text_color="#00FFFF")
        self.player_name_label.pack(side='left', padx=10)

        self.score_display_label = ctk.CTkLabel(self.info_container_frame,
                                        text=f"Score - You: {self.player_score} | CPU: {self.computer_score}",
                                        font=("Impact", 20, "bold"),
                                        text_color="#FFD700")
        self.score_display_label.pack(side='right', padx=10)
        #print("Top panel setup complete")

    def setup_game_canvas(self):
        self.game_canvas = ctk.CTkCanvas(self.main_container_frame,
                                    width=400,
                                    height=150,
                                    bg="#1C2526",
                                    highlightthickness=1,
                                    highlightbackground="#00FFFF")
        self.game_canvas.pack(pady=(0, 10))
        self.game_canvas.create_rectangle(0, 0, 400, 150, fill="#000000", stipple="gray25")
        self.init_background_stars()

    def init_background_stars(self):
        canvas_width = max(self.game_canvas.winfo_width(), 400)
        canvas_height = max(self.game_canvas.winfo_height(), 150)
        self.star_positions = [(random.randint(0, canvas_width), random.randint(0, canvas_height)) for _ in range(20)]

    def draw_background_stars(self, progress):
        if not self.game_canvas.winfo_exists():
            return
        canvas_width = max(self.game_canvas.winfo_width(), 400)
        canvas_height = max(self.game_canvas.winfo_height(), 150)
        for x, y in self.star_positions:
            size = 1.0 + 0.8 * math.sin(progress * 2 * math.pi + x)
            self.game_canvas.create_oval(x - size, y - size, x + size, y + size, fill="#FFFFFF", outline="")

    def setup_round_info(self):
        self.round_info_container_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
        self.round_info_container_frame.pack(fill='x', pady=(0, 10))

        self.current_round_label = ctk.CTkLabel(self.round_info_container_frame,
                                        text=f"Round {self.current_round} of {self.max_rounds}",
                                        font=("Impact", 14, "bold"),
                                        text_color="#FF69B4")
        self.current_round_label.pack(side='left', padx=15)

    def setup_choice_buttons_panel(self):
        #print("Setting up choice buttons panel")
        self.choice_buttons_container_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
        self.choice_buttons_container_frame.pack(fill='x', pady=(0, 10))

        colors = {
            "Rock": {"fg": "#1E90FF", "hover": "#1565C0"},
            "Paper": {"fg": "#FF00FF", "hover": "#C51162"},
            "Scissors": {"fg": "#00CED1", "hover": "#00838F"}
        }

        self.choice_buttons = {}
        for choice in ["Rock", "Paper", "Scissors"]:
            self.choice_buttons[choice] = self.create_glowing_button(
                self.choice_buttons_container_frame,
                choice,
                lambda c=choice: self.play(c),
                colors[choice]["fg"],
                colors[choice]["hover"],
                width=100,
                height=40
            )
            self.choice_buttons[choice].pack(side='left', expand=True, padx=10)
        #print("Choice buttons panel setup complete")

    def setup_control_buttons_panel(self):
        #print("Setting up control buttons panel")
        self.control_buttons_container_frame = ctk.CTkFrame(self.main_container_frame, fg_color="transparent")
        self.control_buttons_container_frame.pack(fill='x', pady=(10, 15))

        self.reset_game_button = self.create_glowing_button(self.control_buttons_container_frame,
                                                "Reset",
                                                self.reset_game,
                                                "#FFA500",
                                                "#EF6C00",
                                                width=100,
                                                height=40)
        self.reset_game_button.pack(side='left', expand=True, padx=30)

        

    def setup_commentator(self):
        self.commentator_text_label = ctk.CTkLabel(self.main_container_frame,
                                              text="",
                                              font=("jell", 12, "italic"),
                                              text_color="#FF69B4",
                                              wraplength=400)
        self.commentator_text_label.pack(fill='x', padx=20, pady=(0, 10))

    def setup_footer(self):
        self.footer_copyright_label = ctk.CTkLabel(self.main_container_frame,
                                         text="© 2025 Ishan's Rock Paper Scissors Deluxe",
                                         font=("jell", 8),
                                         text_color=("gray70", "gray30"))
        self.footer_copyright_label.pack(side='bottom', pady=10)

    def enable_choice_buttons(self):
        for btn in self.choice_buttons.values():
            try:
                btn.configure(state="normal")
            except TclError:
                pass

    def disable_choice_buttons(self):
        for btn in self.choice_buttons.values():
            try:
                btn.configure(state="disabled")
            except TclError:
                pass

    def play(self, player_choice):
        if player_choice not in self.choices or self.is_animating:
            return
        self.is_animating = True
        self.disable_choice_buttons()
        computer_choice = random.choice(self.choices)
        self.game_canvas.delete("all")
        self.game_canvas.create_rectangle(0, 0, self.game_canvas.winfo_width(), self.game_canvas.winfo_height(), fill="#000000",
                                     stipple="gray25")
        self.animation_frame = 0
        self.animate_gestures(player_choice, computer_choice)

    def animate_gestures(self, player_choice, computer_choice):
        if not self.is_running or not self.game_canvas.winfo_exists():
            self.is_animating = False
            return
        self.animation_frame += 1
        progress = self.animation_frame / 40
        if progress > 1:
            self.display_result(player_choice, computer_choice)
            return

        self.game_canvas.delete("all")
        self.game_canvas.create_rectangle(0, 0, self.game_canvas.winfo_width(), self.game_canvas.winfo_height(), fill="#000000",
                                     stipple="gray25")
        self.draw_background_stars(progress)
        self.draw_gesture(self.game_canvas, player_choice, "player", progress)
        self.draw_gesture(self.game_canvas, computer_choice, "computer", progress)

        after_id = self.root.after(30, lambda: self.animate_gestures(player_choice, computer_choice))
        self.after_ids.append(after_id)

    def display_result(self, player_choice, computer_choice):
        try:
            if player_choice == computer_choice:
                result = "It's a Tie! ⚔️"
                color = "#FFA500"
                #print(f"Tie: player_score={self.player_score}, computer_score={self.computer_score}")
            elif (player_choice == "Rock" and computer_choice == "Scissors") or \
                 (player_choice == "Paper" and computer_choice == "Rock") or \
                 (player_choice == "Scissors" and computer_choice == "Paper"):
                result = "You Win! 🏆"
                self.player_score += 1
                self.round_wins['player'] += 1
                color = "#00FF00"
                self.draw_confetti(self.game_canvas)
                #print(f"Player wins: player_score={self.player_score}, computer_score={self.computer_score}")
            else:
                result = "PC Wins! 😈"
                self.computer_score += 1
                self.round_wins['computer'] += 1
                color = "#FF0000"
                #print(f"Computer wins: player_score={self.player_score}, computer_score={self.computer_score}")

            self.game_result_label.configure(text=f"You: {player_choice} \nComputer: {computer_choice}\n{result}", text_color=color)
            self.update_score_display()
            self.is_animating = False
            self.animate_result_label()
            self.show_commentator(f"You picked {player_choice}. Computer picked {computer_choice}. {result}")
            self.check_round_completion()
        except TclError as e:
            pass#print(f"TclError in display_result: {e}")
        except Exception as e:
            pass#print(f"Error in display_result: {e}")

    def animate_result_label(self):
        def scale_text(step=0):
            if step > 3 or self.is_animating or not self.game_result_label.winfo_exists():
                return
            try:
                scale = 1.0 + 0.05 * math.sin(step * math.pi / 1.5)
                self.game_result_label.configure(font=("Impact", int(16 * scale), "bold"))
                after_id = self.root.after(50, lambda: scale_text(step + 1))
                self.after_ids.append(after_id)
            except TclError:
                pass

        scale_text()

    def update_score_display(self):
        try:
            if hasattr(self, 'score_display_label') and self.score_display_label.winfo_exists():
                self.score_display_label.configure(text=f"Score - You: {self.player_score} | CPU: {self.computer_score}")
                #print(f"Score updated: You={self.player_score}, CPU={self.computer_score}")
        except TclError as e:
            pass#print(f"TclError updating score display: {e}")
        except Exception as e:
            pass#print(f"Error updating score display: {e}")

    def check_round_completion(self):
        try:
            if self.current_round >= self.max_rounds:
                self.end_game()
            else:
                self.current_round += 1
                self.player_score = 0
                self.computer_score = 0
                if hasattr(self, 'current_round_label') and self.current_round_label.winfo_exists():
                    self.current_round_label.configure(text=f"Round {self.current_round} of {self.max_rounds}")
                    #print(f"Advanced to round {self.current_round}")
                self.update_score_display()
                self.game_result_label.configure(text="Choose Your Move!", text_color="#00FFFF")
                self.enable_choice_buttons()
        except TclError as e:
            pass#print(f"TclError in check_round_completion: {e}")
        except Exception as e:
            pass#print(f"Error in check_round_completion: {e}")

    def end_game(self):
        try:
            winner = "You" if self.round_wins['player'] > self.round_wins['computer'] else \
                     "Computer" if self.round_wins['computer'] > self.round_wins['player'] else "It's a Tie"
            self.show_game_over_popup(winner)
        except TclError as e:
            pass#print(f"TclError in end_game: {e}")
        except Exception as e:
            pass#print(f"Error in end_game: {e}")

    def show_game_over_popup(self, winner):
        try:
            self.game_over_popup = ctk.CTkToplevel(self.root)
            self.game_over_popup.geometry("500x450")
            self.game_over_popup.title("Game Over")
            self.game_over_popup.configure(fg_color="#1C2526")
            self.game_over_popup.transient(self.root)
            self.game_over_popup.grab_set()

            self.game_over_popup.protocol("WM_DELETE_WINDOW", self.close_popup)

            if winner == "You":
                title_text = f"You Won, {self.player_name}! 🏆"
                title_color = "#FFD700"
            elif winner == "Computer":
                title_text = f"You Lost, {self.player_name}! 😢"
                title_color = "#FF4500"
            else:
                title_text = f"It's a Tie, {self.player_name}! ⚖️"
                title_color = "#FFA500"

            self.game_over_title_label = ctk.CTkLabel(self.game_over_popup,
                                       text=title_text,
                                       font=("Impact", 24, "bold"),
                                       text_color=title_color)
            self.game_over_title_label.pack(pady=20)

            self.game_over_animation_canvas = ctk.CTkCanvas(self.game_over_popup, width=350, height=150, bg="#1C2526",
                                             highlightthickness=0)
            self.game_over_animation_canvas.pack(pady=10)

            if winner == "You":
                confetti_positions = [(random.randint(0, 350), random.randint(0, 150)) for _ in range(20)]
                confetti_emojis = ['🎉', '✨', '🌟', '🎊']
                confetti_items = []
                for x, y in confetti_positions:
                    emoji = random.choice(confetti_emojis)
                    item = self.game_over_animation_canvas.create_text(x, y, text=emoji, font=("Arial", 20),
                                                        fill="white")
                    confetti_items.append((item, y, random.uniform(0.5, 1.0)))

                self.winner_trophy_icon = self.game_over_animation_canvas.create_text(175, 75, text="🏆", font=("Arial", 40),
                                                      fill="#FFD700")

                def animate_confetti_and_trophy(step=0):
                    if step > 30 or not self.game_over_animation_canvas.winfo_exists():
                        return
                    try:
                        for item, start_y, speed in confetti_items:
                            self.game_over_animation_canvas.move(item, 0, speed)
                        scale = 1.0 + 0.1 * math.sin(step * 0.2 * math.pi)
                        self.game_over_animation_canvas.delete(self.winner_trophy_icon)
                        self.winner_trophy_icon = self.game_over_animation_canvas.create_text(175, 75, text="🏆", font=("Arial", int(40 * scale)), fill="#FFD700")
                        glow = int(255 * (0.5 + 0.5 * math.sin(step * 0.1 * math.pi)))
                        self.game_over_title_label.configure(text_color=f"#{glow:02x}{glow:02x}00")
                        after_id = self.game_over_popup.after(50, lambda: animate_confetti_and_trophy(step + 1))
                        self.after_ids.append(after_id)
                    except TclError:
                        pass

                animate_confetti_and_trophy()

            elif winner == "Computer":
                self.loser_sad_emoji_icon = self.game_over_animation_canvas.create_text(175, 75, text="😢", font=("Arial", 40),
                                                         fill="#FF4500")
                bg_opacity = 0

                def animate_loss(steps=0):
                    nonlocal bg_opacity
                    if steps > 50 or not self.game_over_animation_canvas.winfo_exists():
                        return
                    try:
                        bounce = 3 * math.sin(steps * 0.3 * math.pi)
                        self.game_over_animation_canvas.delete(self.loser_sad_emoji_icon)
                        self.loser_sad_emoji_icon = self.game_over_animation_canvas.create_text(175, 75 + bounce, text="😢", font=("Arial", 40), fill="#FF4500")
                        bg_opacity = min(255, bg_opacity + 5)
                        bg_color = f"#{int(bg_opacity):02x}{int(bg_opacity):02x}{int(bg_opacity):02x}"
                        self.game_over_animation_canvas.configure(bg=bg_color)
                        offset = 1 * math.sin(steps * 0.5 * math.pi)
                        self.game_over_title_label.configure(text_color="#FF4500")
                        self.game_over_title_label.place_configure(relx=0.5, rely=0.1, anchor="center", x=offset)
                        after_id = self.game_over_popup.after(50, lambda: animate_loss(steps + 1))
                        self.after_ids.append(after_id)
                    except TclError:
                        pass

                animate_loss()

            else:
                self.tie_balance_icon = self.game_over_animation_canvas.create_text(175, 75, text="⚖️", font=("Arial", 40),
                                                        fill="#FFA500")

                def animate_tie(step=0):
                    if step > 20 or not self.game_over_animation_canvas.winfo_exists():
                        return
                    try:
                        scale = 1.0 + 0.05 * math.sin(step * 0.2 * math.pi)
                        self.game_over_animation_canvas.delete(self.tie_balance_icon)
                        self.tie_balance_icon = self.game_over_animation_canvas.create_text(175, 75, text="⚖️", font=("Arial", int(40 * scale)), fill="#FFA500")
                        after_id = self.game_over_popup.after(50, lambda: animate_tie(step + 1))
                        self.after_ids.append(after_id)
                    except TclError:
                        pass

                animate_tie()

            self.play_again_button = self.create_glowing_button(self.game_over_popup,
                                               "Play Again",
                                               self.prompt_rounds_in_popup,
                                               "#00CED1",
                                               "#0097A7",
                                               width=100,
                                               height=40)
            self.play_again_button.pack(pady=10)

            self.back_button = self.create_glowing_button(self.game_over_popup,
                                         "Back",
                                         self.return_to_game,
                                         "#FF0000",
                                         "#B71C1C",
                                         width=100,
                                         height=40)
            self.back_button.pack(pady=10)
        except TclError as e:
            pass#print(f"TclError in show_game_over_popup: {e}")
        except Exception as e:
            pass#print(f"Error in show_game_over_popup: {e}")

    def close_popup(self):
        try:
            #print("close_popup called")
            self.clear_main_ui()
            self.reset_game()
            self.is_running = True
            self.main_container_frame.configure(fg_color="#1C2526")
            self.setup_top_panel()
            self.setup_game_canvas()
            self.setup_round_info()
            self.setup_choice_buttons_panel()
            self.setup_control_buttons_panel()
            self.setup_commentator()
            self.setup_footer()
            self.init_result_label()
            self.enable_choice_buttons()
            self.update_score_display()
            self.root.update()
            #print("Game UI restored after popup close")
        except TclError as e:
            pass#print(f"TclError in close_popup: {e}")
        except Exception as e:
            pass#print(f"Error in close_popup: {e}")

    def return_to_game(self):
        try:
            #print("return_to_game called")
            self.clear_main_ui()
            self.reset_game()
            self.is_running = True
            self.main_container_frame.configure(fg_color="#1C2526")
            self.setup_top_panel()
            self.setup_game_canvas()
            self.setup_round_info()
            self.setup_choice_buttons_panel()
            self.setup_control_buttons_panel()
            self.setup_commentator()
            self.setup_footer()
            self.init_result_label()
            self.enable_choice_buttons()
            self.update_score_display()
            self.root.update()
            #print("Game UI restored")
        except TclError as e:
            pass#print(f"TclError in return_to_game: {e}")
        except Exception as e:
            pass#print(f"Error in return_to_game: {e}")

    def prompt_rounds_in_popup(self):
        #print("prompt_rounds_in_popup called")
        try:
            self.play_again_button.destroy()
            self.back_button.destroy()

            label = ctk.CTkLabel(self.game_over_popup, text="Enter Number of Rounds (1-100):",
                                 font=("jell", 14, "bold"), text_color="#FFD700")
            label.pack(pady=10)

            self.rounds_entry = ctk.CTkEntry(self.game_over_popup, placeholder_text="e.g., 5",
                                             font=("jell", 12), width=150, height=30)
            self.rounds_entry.pack(pady=10)
            self.rounds_entry.bind("<Return>", lambda event: self.submit_rounds_in_popup())
            self.rounds_entry.focus_set()

            submit_button = self.create_glowing_button(self.game_over_popup, "Submit",
                                                      self.submit_rounds_in_popup, "#00CED1", "#0097A7",
                                                      width=100, height=30)
            submit_button.pack(pady=10)
            self.game_over_popup.update()
            #print("Round input popup updated")
        except TclError as e:
            pass#print(f"TclError in prompt_rounds_in_popup: {e}")
        except Exception as e:
            pass#print(f"Error in prompt_rounds_in_popup: {e}")

    def submit_rounds_in_popup(self):
        #print("submit_rounds_in_popup called")
        try:
            rounds = int(self.rounds_entry.get().strip())
            if rounds < 1 or rounds > 100:
                messagebox.showwarning("Input Error", "Please enter a number between 1 and 100!")
                return
            self.max_rounds = rounds
            self.clear_main_ui()
            self.reset_game()
            self.start_game()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number!")
        except TclError as e:
            pass#print(f"TclError in submit_rounds_in_popup: {e}")
        except Exception as e:
            pass#print(f"Error in submit_rounds_in_popup: {e}")

    def reset_game(self):
        try:
            #print("reset_game called")
            self.player_score = 0
            self.computer_score = 0
            self.current_round = 1
            self.round_wins = {'player': 0, 'computer': 0}
            if hasattr(self, 'game_result_label') and self.game_result_label.winfo_exists():
                self.game_result_label.configure(text="Game Reset! Choose Again! 💪", text_color="#00FFFF")
            if hasattr(self, 'current_round_label') and self.current_round_label.winfo_exists():
                self.current_round_label.configure(text=f"Round {self.current_round} of {self.max_rounds}", text_color="#FF69B4")
                #print(f"Reset to Round {self.current_round} of {self.max_rounds}")
            if hasattr(self, 'game_canvas') and self.game_canvas.winfo_exists():
                self.game_canvas.delete("all")
                self.game_canvas.create_rectangle(0, 0, self.game_canvas.winfo_width(), self.game_canvas.winfo_height(), fill="#000000",
                                             stipple="gray25")
                self.init_background_stars()
            self.update_score_display()
            self.enable_choice_buttons()
        
        except Exception as e:
            pass#print(f"Error in submit_rounds_in_popup: {e}")

    def show_commentator(self, text):
        if self.is_animating:
            return
        self.commentator_text = text
        self.commentator_index = 0
        if hasattr(self, 'commentator_text_label') and self.commentator_text_label.winfo_exists():
            self.commentator_text_label.configure(text="")
            self._typewriter_step()

    def _typewriter_step(self):
        if self.is_animating or self.commentator_index >= len(self.commentator_text):
            return
        try:
            current_text = self.commentator_text_label.cget("text")
            next_char = self.commentator_text[self.commentator_index]
            self.commentator_text_label.configure(text=current_text + next_char)
            self.commentator_index += 1
            after_id = self.root.after(50, self._typewriter_step)
            self.after_ids.append(after_id)
        except TclError:
            pass

    

# if __name__ == "__main__":
#     try:
#         app = ctk.CTk()
#         game = RockPaperScissorsApp(app)
#         app.mainloop()
#     except Exception as e:
#         pass#print(f"Error starting application: {e}")