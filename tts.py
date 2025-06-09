import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def talk(text: str):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()
    return "spoken"
