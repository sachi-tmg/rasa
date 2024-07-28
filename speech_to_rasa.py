import speech_recognition as sr
import requests
import json
import pyttsx3

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Rasa server endpoint
rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"

while True:
    try:
        # Use the microphone as the audio source
        with sr.Microphone() as mic:
            # Adjust the recognizer sensitivity to ambient noise
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Listening...")

            # Listen for the user's input
            audio = recognizer.listen(mic)
            print("Processing audio...")

            # Use Google's speech recognition to convert the audio to text
            text = recognizer.recognize_google(audio)
            text = text.lower()

            # Print the recognized text
            print(f"Recognized: {text}")

            # Send the recognized text to the Rasa server
            payload = {
                "sender": "user",  # You can customize the sender ID
                "message": text
            }
            response = requests.post(rasa_endpoint, data=json.dumps(payload))

            # Extract the messages from the Rasa response
            rasa_responses = response.json()
            for message in rasa_responses:
                if 'text' in message:
                    bot_response = message['text']
                    print("Rasa response:", bot_response)
                    
                    # Speak the response
                    engine.say(bot_response)
                    engine.runAndWait()

    except sr.UnknownValueError:
        # If the recognizer couldn't understand the audio, reset and continue
        recognizer = sr.Recognizer()
        print("Could not understand audio. Retrying...")
        continue
    except Exception as e:
        print(f"An error occurred: {e}")
        break
