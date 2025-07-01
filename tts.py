import pyttsx3

class _TTS:

    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200) 

    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

def talk(text: str):
    tts = _TTS() # Initialize the tts engine
    print(f"🎤 Vocal synthesis: {text}")
    tts.start(text)  