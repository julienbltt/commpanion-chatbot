import whisper
import sounddevice as sd
import numpy as np
import queue

MODEL_NAME = "small"
SAMPLERATE = 16000
CHUNK_DURATION = 0.5  # seconds
SILENCE_THRESHOLD = 0.01
MAX_SILENCE_SECONDS = 1.0

model = whisper.load_model(MODEL_NAME)
audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print("Audio input status:", status)
    audio_queue.put(indata.copy())

def is_silent(audio_chunk):
    return np.abs(audio_chunk).mean() < SILENCE_THRESHOLD

def record_until_silence():
    buffer = np.empty((0, 1), dtype=np.float32)
    silent_duration = 0

    while True:
        chunk = audio_queue.get()
        buffer = np.append(buffer, chunk, axis=0)

        if is_silent(chunk):
            silent_duration += CHUNK_DURATION
        else:
            silent_duration = 0

        if silent_duration > MAX_SILENCE_SECONDS and len(buffer) > SAMPLERATE * 0.5:
            break

    return np.squeeze(buffer)

def transcribe_stream():
    print("Listening... Speak now.")
    with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype='float32',
                        callback=audio_callback, blocksize=int(SAMPLERATE * CHUNK_DURATION)):
        audio_data = record_until_silence()
        result = model.transcribe(audio_data, language='fr', fp16=False, verbose=False)
        return result['text'].strip()
    