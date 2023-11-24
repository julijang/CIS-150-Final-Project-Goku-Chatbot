import tkinter as tk
from tkinter import scrolledtext

class ChatUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chatbot UI")

        # Chat history
        self.chat_history = "Chat history:"
        self.chat_history_text = scrolledtext.ScrolledText(self.master, width=50, height=10)
        self.chat_history_text.insert(tk.END, self.chat_history)
        self.chat_history_text.grid(row=0, column=0, padx=10, pady=10)

        # Transcription label
        self.transcription_label = tk.Label(self.master, text="Transcription:")
        self.transcription_label.grid(row=1, column=0, padx=10, pady=5)

        # Record button
        self.record_button = tk.Button(self.master, text="Record", command=self.record_audio)
        self.record_button.grid(row=2, column=0, padx=10, pady=10)

    def record_audio(self):
        # Simulate voice transcription (replace this with actual speech recognition)
        transcribed_text = "This is a sample transcription."
        self.update_chat_history(transcribed_text)

    def update_chat_history(self, text):
        # Update the chat history text area
        self.chat_history += f"\nUser: {text}"
        self.chat_history_text.delete(1.0, tk.END)
        self.chat_history_text.insert(tk.END, self.chat_history)

        # Update the transcription label
        self.transcription_label.config(text=f"Transcription: {text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatUI(root)
    root.mainloop()
