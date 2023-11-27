# assistant.py

import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
from openai import OpenAI
import pyttsx3
from PIL import Image, ImageTk
from config import OPENAI_API_KEY  # Import the API key from the config file


class GokuAssistant:
    recorded_text = ""  # Empty variable to store recorded text

    def __init__(self, root):
        self.root = root
        self.root.title("Goku Voice Assistant")

        # Load background image
        background_image = Image.open("C:/Users/Julijan/Documents/CIS 150/FinalProject/CIS-150-Final-Project/pic/background.jpg")
        background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Set background image
        background_label = tk.Label(root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for centering UI widgets
        self.center_frame = tk.Frame(root)
        self.center_frame.pack(expand=True)

        # Create UI components
        self.text_area = scrolledtext.ScrolledText(self.center_frame, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(pady=10, padx=(10, 10))  # Add padding on the x-axis

        self.record_button = tk.Button(self.center_frame, text="Record", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        # Initialize STT variables
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recording = False

        # Set your OpenAI API key using config
        self.api_key = OPENAI_API_KEY
        self.openai_client = OpenAI(api_key=self.api_key)

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

        # Bind the root window to center widgets when resized
        root.bind("<Configure>", lambda e: self.center_widgets())

    def center_widgets(self):
        # Center the widgets when the window is resized
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Calculate the center coordinates
        x_center = width / 2
        y_center = height / 2

        # Move the center_frame to the center coordinates
        self.root.update_idletasks()  # Ensure geometry information is up-to-date
        frame_width = self.center_frame.winfo_reqwidth()
        frame_height = self.center_frame.winfo_reqheight()

        x_position = x_center - frame_width / 2
        y_position = y_center - frame_height / 2

        self.center_frame.place(x=x_position, y=y_position)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.record_button.config(text="Listening", state=tk.DISABLED)  # Disable the button
        self.text_area.delete(1.0, tk.END)  # Clear previous text

        # Start a new thread for recording
        self.record_thread = threading.Thread(target=self.record_thread_function)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="Record", state=tk.NORMAL)  # Enable the button
        recorded_text = self.text_area.get("1.0", tk.END).strip()
        if recorded_text:
            self.recorded_text = f"User: {recorded_text}\n"  # Update recorded text

            # Display the recorded text in the text area
            self.text_area.insert(tk.END, self.recorded_text)
            self.text_area.yview(tk.END)

            # Send recorded text to ChatGPT
            self.chatgpt_response()

    def record_thread_function(self):
        with self.microphone as source:
            try:
                while self.recording:
                    # Adjust the timeout and phrase_time_limit parameters
                    audio_data = self.recognizer.listen(source, timeout=15, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio_data)
                    self.text_area.insert(tk.END, text + "\n")
                    self.text_area.yview(tk.END)
            except sr.UnknownValueError:
                pass  # Handle case when speech cannot be recognized
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
            finally:
                self.stop_recording()

    def chatgpt_response(self):
        user_input = self.recorded_text.strip()

        # Make sure there is user input before sending it to ChatGPT
        if user_input:
            try:
                # Create an OpenAI instance
                client = OpenAI(api_key=self.api_key)

                # Send user input to ChatGPT using the OpenAI instance
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Son Goku from Dragon Ball Z. You keep peace on earth."},
                        {"role": "user", "content": user_input},
                    ]
                )

                # Extract the assistant's reply from the response
                assistant_reply = response.choices[0].message.content

                # Update the GUI with ChatGPT's response
                self.text_area.insert(tk.END, f"{assistant_reply}\n")
                self.text_area.yview(tk.END)

                # Read the ChatGPT response using text-to-speech
                self.tts_engine.say(assistant_reply)
                self.tts_engine.runAndWait()

                # Close the chatgpt instance
                client.close()

            except Exception as e:
                print(f"Error communicating with ChatGPT: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GokuAssistant(root)
    root.mainloop()
