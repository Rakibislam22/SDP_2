from customtkinter import *
import google.generativeai as ai
import threading
import time
import os
from dotenv import load_dotenv
load_dotenv()


def open_chatbot(chatbot_main_windo):

    API_KEY = os.getenv("G_API_KEY")
    ai.configure(api_key=API_KEY)
    model = ai.GenerativeModel("gemini-2.0-flash")
    conversation = model.start_chat()

    messages =""

    def clear_chat():
        # time.sleep(1)
        chatbot_chatbox.configure(state="normal")
        chatbot_chatbox.delete(1.0, "end")
        see_message("ChronoAI: Chat Cleared...\n\n")
        chatbot_chatbox.configure(state="disabled")

    def get_message():
        global messages
        messages = chatbot_entry.get().strip()

        if not messages:
            s=f"ChronoAI: Please enter a valid message... "
            see_message(s+"\n\n")
            return
        if messages.lower() == "clear":
            chatbot_entry.delete(0, END)
            chatbot_chatbox.configure(state="normal")
            see_message("ChronoAI: Chat clearing ")
            chatbot_chatbox.update()
            time.sleep(1)
            for i in range(3):
                see_message(".")
                chatbot_chatbox.update()
                time.sleep(1)
            clear_chat()
            chatbot_chatbox.configure(state="disabled")
            return

        see_message("You: " + messages + "\n\n")
        chatbot_entry.delete(0, END)
        threading.Thread(target=chatbot_response, args=(messages,), daemon=True).start()

    def see_message(text):
        chatbot_chatbox.configure(state="normal")
        chatbot_chatbox.insert(END, text)
        chatbot_chatbox.configure(state="disabled")
        chatbot_chatbox.see(END)

    def chatbot_response(sms):
        try:
            response = conversation.send_message(sms)
            r=f"ChronoAI: {response.text} "
        except Exception as e:
            r = f"Error: {str(e)}. Please try again."
        see_message(r+"\n\n")


    chatbot_window = CTkToplevel(chatbot_main_windo)
    chatbot_window.title("ChronoAI - Your Time Assistant")
    chatbot_window.geometry("505x575")
    chatbot_window.resizable(False, False)

    # Center it
    chatbot_window.update_idletasks()
    main_x = chatbot_main_windo.winfo_rootx()
    main_y = chatbot_main_windo.winfo_rooty()
    main_width = chatbot_main_windo.winfo_width()
    main_height = chatbot_main_windo.winfo_height()
    chatbot_width = 500
    chatbot_height = 570
    x = main_x + (main_width // 2) - (chatbot_width // 2)
    y = main_y + (main_height // 2) - (chatbot_height // 2)
    chatbot_window.geometry(f"{chatbot_width}x{chatbot_height}+{x}+{y}")

    # Focus & bring to front
    chatbot_window.lift()
    chatbot_window.focus_force()
    chatbot_window.attributes("-topmost", True)
    chatbot_window.after(500, lambda: chatbot_window.attributes("-topmost", False))

    #Frame for Chatbot
    chatbot_frame = CTkFrame(chatbot_window, fg_color="light blue", width=400, height=500 )
    chatbot_frame.pack(side="top", expand=True, fill="both",)

    chatbot_chatbox = CTkTextbox(chatbot_frame, wrap="word", font=("JetBrains Mono", 14), state="normal", width=500, height=490, text_color="white",  fg_color="black")
    chatbot_chatbox.pack(side="top", anchor="w", padx=1, pady=5 )
    chatbot_chatbox.insert(1.0, "ChronoAI: Hello! I'm your time-savvy assistant. Ask me anything...\n\n")
    chatbot_chatbox.configure(state="disabled")

    chatbot_entry = CTkEntry(chatbot_frame, placeholder_text="Type your message..." , font=("JetBrains Mono", 14), width=385, height=50, fg_color="white", text_color="black")
    chatbot_entry.pack( anchor="w", padx=1, pady=0, ipadx=19)
    chatbot_entry.bind("<Return>", lambda event: get_message())  

    chatbot_send_btn = CTkButton(chatbot_frame, font=("Helvetica", 16, "bold"), text="Send", width=70, height=48, command = get_message,)
    chatbot_send_btn.place( x=427+35, y=502+23, anchor="center")

    copyrights = CTkLabel(chatbot_frame, text="© alifjobaer12", font=("Calibri", 10), corner_radius=0, width=1, height=1, fg_color="transparent", bg_color="transparent", text_color="#9e9e9e", )
    copyrights.place(x=495, y=510+50, anchor="e") 



    

# chatbot_main_windo = CTk()

# chatbot_main_windo.geometry("400x500")
# chatbot_main_windo.title("Chat Bot")

# open_chatbot(chatbot_main_windo)

# chatbot_main_windo.mainloop()