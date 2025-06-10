import keyboard
from stt import transcribe_stream
from llm import get_lmstudio_response
import time
import threading
from hmi_glasses_event import GlassesHMI, ButtonEvent

class VoiceAssistant:
    def __init__(self):
        self.glasses = None
        self.is_processing = False
        self.processing_lock = threading.Lock()
        
        # Configuration des lunettes
        self.VENDOR_ID = 0x17EF
        self.PRODUCT_ID = 0xB813
        
    def setup_glasses(self):
        """Configure et connecte les lunettes"""
        try:
            self.glasses = GlassesHMI(
                vendor_id=self.VENDOR_ID,
                product_id=self.PRODUCT_ID
            )
            
            # Enregistrer les callbacks pour les événements
            self.glasses.register_callback(ButtonEvent.CENTER, self.on_voice_trigger)
            self.glasses.register_callback(ButtonEvent.CENTER_SOUND, self.on_voice_trigger)
            
            # Boutons additionnels avec autres fonctions
            self.glasses.register_callback(ButtonEvent.PLUS, self.on_plus_button)
            self.glasses.register_callback(ButtonEvent.MINUS, self.on_minus_button)
            
            self.glasses.find()
            self.glasses.open()
            
            print("✅ Lunettes connectées et prêtes!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la configuration des lunettes: {e}")
            return False
    
    def on_voice_trigger(self, event):
        """Callback déclenché quand on appuie sur le bouton center"""
        with self.processing_lock:
            if self.is_processing:
                print("🔄 Traitement en cours, veuillez patienter...")
                return
            
            self.is_processing = True
        
        try:
            print("🎤 Bouton détecté - Début de l'écoute...")
            self.process_voice_command()
        except Exception as e:
            print(f"❌ Erreur lors du traitement vocal: {e}")
        finally:
            with self.processing_lock:
                self.is_processing = False
    
    def on_plus_button(self, event):
        """Callback pour le bouton +"""
        print("➕ Bouton + pressé - Fonction personnalisée")
        # Vous pouvez ajouter ici d'autres fonctionnalités
        
    def on_minus_button(self, event):
        """Callback pour le bouton -"""
        print("➖ Bouton - pressé - Fonction personnalisée")
        # Vous pouvez ajouter ici d'autres fonctionnalités
    
    def process_voice_command(self):
        """Traite une commande vocale complète"""
        try:
            # Transcription audio
            tic = time.time()
            prompt = transcribe_stream()
            tac = time.time()
            
            print(f"⚡ Whisper duration: {(tac-tic):.6f} seconds")
            print(f"🎯 Understood: {prompt}")
            
            if not prompt.strip():
                print("❌ No speech detected. Try again.")
                return
            
            # Réponse LLM
            print("🤖 LLM responding wait...")
            tic = time.time()
            get_lmstudio_response(prompt)
            tac = time.time()
            print(f"✅ LLM finished, time: {(tac-tic):.6f} seconds")
            
        except Exception as e:
            print(f"❌ Error in voice processing: {e}")
    
    def run_with_keyboard_fallback(self):
        """Lance le système avec fallback clavier si les lunettes ne marchent pas"""
        glasses_available = self.setup_glasses()
        
        if glasses_available:
            print("🕶️  Mode lunettes activé - Appuyez sur le bouton center pour parler")
            print("⌨️  Vous pouvez aussi utiliser ENTER comme fallback")
        else:
            print("⌨️  Mode clavier uniquement - Appuyez sur ENTER pour parler")
        
        try:
            while True:
                if glasses_available:
                    print("\n👆 Appuyez sur le bouton des lunettes ou ENTER pour commencer...")
                else:
                    print("\n👆 Press ENTER to start listening.")
                
                # Attendre soit l'événement des lunettes soit ENTER
                keyboard.wait("enter")
                
                # Si on arrive ici, c'est qu'ENTER a été pressé
                print("⌨️  Déclenchement clavier détecté")
                self.process_voice_command()
                        
        except KeyboardInterrupt:
            print("\n🛑 Exiting...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if self.glasses:
                self.glasses.close()
    
    def run_glasses_only(self):
        """Lance le système uniquement avec les lunettes"""
        if not self.setup_glasses():
            print("❌ Impossible de connecter les lunettes. Utilisez run_with_keyboard_fallback()")
            return
        
        print("🕶️  Mode lunettes uniquement - Appuyez sur le bouton center pour parler")
        print("✋ Ctrl+C pour quitter")
        
        try:
            # Maintenir le programme en vie
            while True:
                time.sleep(1)
                        
        except KeyboardInterrupt:
            print("\n🛑 Exiting...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if self.glasses:
                self.glasses.close()

# Point d'entrée principal
if __name__ == "__main__":
    assistant = VoiceAssistant()
    
    # Choisir le mode de fonctionnement
    print("Choisissez le mode de fonctionnement:")
    print("1. Lunettes + Clavier (fallback)")
    print("2. Lunettes uniquement")
    
    try:
        choice = input("Votre choix (1 ou 2): ").strip()
        
        if choice == "2":
            assistant.run_glasses_only()
        else:
            assistant.run_with_keyboard_fallback()
            
    except KeyboardInterrupt:
        print("\n🛑 Programme interrompu")
    except Exception as e:
        print(f"❌ Erreur: {e}")
