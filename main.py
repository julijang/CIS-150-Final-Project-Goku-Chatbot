# main.py
import speech_recognition as sr

def get_user_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak:")

        # Adjust the timeout to control the duration of silence required to end speech input
        audio = recognizer.listen(source, timeout=5)

    try:
        # Using Google Web Speech API for recognition
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Error making the request; {e}")
        return ""

def display_response(response):
    # Print to console the AI response
    print("AI: " + response)

def main():
    print("Welcome to the Conversation!")

    while True:
        user_input = get_user_input()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input:
            display_response("You said: " + user_input)

if __name__ == "__main__":
    main()
