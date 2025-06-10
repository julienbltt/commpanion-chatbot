import pyttsx3

class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()

def talk(text: str):
    print(f"🎤 Synthèse vocale: {text}")
    tts = _TTS()
    tts.start(text)
    del(tts)
