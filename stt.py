import whisper
import sounddevice as sd
import numpy as np
import queue
import time

MODEL_NAME = "small"
SAMPLERATE = 16000
CHUNK_DURATION = 0.5  # seconds
SILENCE_THRESHOLD = 0.01
MAX_SILENCE_SECONDS = 1.0

model = whisper.load_model(MODEL_NAME)

def is_silent(audio_chunk):
    return np.abs(audio_chunk).mean() < SILENCE_THRESHOLD

def record_until_silence(audio_queue):
    """Enregistre jusqu'à détection de silence avec une queue dédiée"""
    buffer = np.empty((0, 1), dtype=np.float32)
    silent_duration = 0
    
    print("🎤 Début de l'enregistrement...")
    start_time = time.time()
    min_recording_time = 0.5  # Minimum 0.5 secondes d'enregistrement

    while True:
        try:
            # Timeout pour éviter les blocages
            chunk = audio_queue.get(timeout=5.0)
            buffer = np.append(buffer, chunk, axis=0)

            if is_silent(chunk):
                silent_duration += CHUNK_DURATION
            else:
                silent_duration = 0

            # Conditions pour arrêter l'enregistrement
            recording_time = time.time() - start_time
            if (silent_duration > MAX_SILENCE_SECONDS and 
                recording_time > min_recording_time and 
                len(buffer) > SAMPLERATE * 0.5):
                break
                
            # Sécurité : arrêt après 30 secondes maximum
            if recording_time > 30:
                print("⚠️ Arrêt automatique après 30 secondes")
                break
                
        except queue.Empty:
            print("⚠️ Timeout lors de l'enregistrement audio")
            break

    print(f"🎤 Fin de l'enregistrement ({time.time() - start_time:.2f}s)")
    return np.squeeze(buffer)

def clear_audio_queue(audio_queue):
    """Vide complètement la queue audio"""
    cleared_count = 0
    try:
        while True:
            audio_queue.get_nowait()
            cleared_count += 1
    except queue.Empty:
        pass
    
    if cleared_count > 0:
        print(f"🧹 Queue audio nettoyée ({cleared_count} éléments supprimés)")

def transcribe_stream():
    """Transcrit un flux audio avec nettoyage approprié des ressources"""
    print("🎧 Préparation de l'écoute...")
    
    # Créer une nouvelle queue pour cette session
    audio_queue = queue.Queue()
    
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"⚠️ Audio input status: {status}")
        audio_queue.put(indata.copy())
    
    try:
        print("👂 Listening... Speak now.")
        
        # Créer le stream audio avec gestion explicite des ressources
        with sd.InputStream(
            samplerate=SAMPLERATE, 
            channels=1, 
            dtype='float32',
            callback=audio_callback, 
            blocksize=int(SAMPLERATE * CHUNK_DURATION)
        ) as stream:
            
            # Petit délai pour s'assurer que le stream est prêt
            time.sleep(0.1)
            
            # Vider la queue au cas où il y aurait des données résiduelles
            clear_audio_queue(audio_queue)
            
            # Enregistrer jusqu'au silence
            audio_data = record_until_silence(audio_queue)
            
        # Le stream est automatiquement fermé grâce au context manager
        
        # Vérifier que nous avons des données audio valides
        if len(audio_data) == 0:
            print("❌ Aucune donnée audio capturée")
            return ""
            
        if len(audio_data) < SAMPLERATE * 0.3:  # Moins de 0.3 secondes
            print("❌ Audio trop court pour être traité")
            return ""
        
        print("🤖 Transcription en cours...")
        
        # Transcription avec Whisper
        result = model.transcribe(
            audio_data, 
            language='fr', 
            fp16=False, 
            verbose=False
        )
        
        transcribed_text = result['text'].strip()
        print(f"✅ Transcription terminée: '{transcribed_text}'")
        
        return transcribed_text
        
    except Exception as e:
        print(f"❌ Erreur lors de la transcription: {e}")
        return ""
    
    finally:
        # Nettoyage final
        clear_audio_queue(audio_queue)
        print("🧹 Ressources audio nettoyées")

def test_transcription():
    """Fonction de test pour vérifier le bon fonctionnement"""
    print("=== TEST DE TRANSCRIPTION ===")
    for i in range(3):
        print(f"\n--- Test {i+1}/3 ---")
        result = transcribe_stream()
        print(f"Résultat: '{result}'")
        time.sleep(1)  # Pause entre les tests

if __name__ == "__main__":
    test_transcription()