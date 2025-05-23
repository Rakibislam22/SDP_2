from customtkinter import *
import google.generativeai as ai
import threading
import webbrowser
import time
import os
from dotenv import load_dotenv
import re
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
            cleaned_text = clean_response_text(response.text)
            r=f"ChronoAI: {cleaned_text} "
        except Exception as e:
            r = f"Error: {str(e)}. Please try again."
        see_message(r+"\n\n")


    def clean_response_text(text):
        # Replace Gemini with ChronoAi
        text = re.sub(r'\bgemini\b', 'ChronoAi', text, flags=re.IGNORECASE)
      
        # Replace Google and Google AI with Team_ChronoMate
        text = re.sub(r'\bgoogle ai\b', 'ChronoAi', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgoogle\b', 'Team_ChronoMate', text, flags=re.IGNORECASE)
    
        # Add signature
        text = text.strip() + "\n\n\t\t\t\tPowered by Team_ChronoMate"
        return text
    
    #Frame for Chatbot
    chatbot_frame = CTkFrame(chatbot_main_windo, fg_color="light blue", width=400, height=500 )
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

    def open_alif_github(event=None):
        webbrowser.open_new("https://github.com/alifjobaer12")  

    copyrights = CTkLabel(
        chatbot_frame,
        text="© alifjobaer12",
        font=("Calibri", 10),
        corner_radius=0,
        width=1,
        height=1,
        fg_color="transparent",
        bg_color="transparent",
        text_color="#848383",
        cursor="hand2"  # shows pointer on hover
    )
    copyrights.place(
        x=460+35, 
        y=542+23, 
        anchor="se"
    )
    
    copyrights.bind("<Button-1>", open_alif_github)




    

# chatbot_main_windo = CTk()

# chatbot_main_windo.geometry("400x500")
# chatbot_main_windo.title("Chat Bot")

# open_chatbot(chatbot_main_windo)

# chatbot_main_windo.mainloop()