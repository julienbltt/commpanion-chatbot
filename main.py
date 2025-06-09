import keyboard
from stt import transcribe_stream
from llm import get_lmstudio_response
import time

try:
    while True:       
        print("Press ENTER to start listening.")
        keyboard.wait("enter")
        tic = time.time()
        prompt = transcribe_stream()
        #prompt = transcribe_audio()
        tac = time.time()
        print(f"Whisper duration: {(tac-tic):.6f} seconds. ")
        print(f"Understood: {prompt}")
        if not prompt.strip():
            print(" No speech detected. Try again.")
            continue
        print("LLM responding wait...")
        tic = time.time()
        get_lmstudio_response(prompt)
        tac = time.time( )
        print(f"LLM finished, time: {(tac-tic):.6f} seconds")

except KeyboardInterrupt:
    print("Exiting...")

except Exception as e:
    print(f"Error: {e}")
