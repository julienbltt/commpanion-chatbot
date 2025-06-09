"""
Exemple simple d'utilisation du système d'événements des lunettes
"""

from hmi_glasses_event import GlassesHMI, ButtonEvent
import time

def on_center_pressed(event):
    """Action quand le bouton center est pressé"""
    print(f"🎯 ACTION: Bouton {event.value} pressé - Démarrage de l'écoute vocale")
    # Ici vous pourriez appeler votre fonction de transcription
    # transcribe_stream()

def on_plus_pressed(event):
    """Action quand le bouton + est pressé"""
    print(f"➕ ACTION: Bouton {event.value} pressé - Volume up ou autre")
    
def on_minus_pressed(event):
    """Action quand le bouton - est pressé"""
    print(f"➖ ACTION: Bouton {event.value} pressé - Volume down ou autre")

def on_unknown_button(event):
    """Action pour les boutons non reconnus"""
    print(f"❓ ACTION: Bouton inconnu pressé - {event.value}")

def main():
    # Configuration
    VENDOR_ID = 0x17EF
    PRODUCT_ID = 0xB813
    
    # Créer l'instance des lunettes
    glasses = GlassesHMI(vendor_id=VENDOR_ID, product_id=PRODUCT_ID)
    
    # Enregistrer les callbacks pour chaque type d'événement
    glasses.register_callback(ButtonEvent.CENTER, on_center_pressed)
    glasses.register_callback(ButtonEvent.CENTER_SOUND, on_center_pressed)
    glasses.register_callback(ButtonEvent.PLUS, on_plus_pressed)
    glasses.register_callback(ButtonEvent.MINUS, on_minus_pressed)
    glasses.register_callback(ButtonEvent.UNKNOWN, on_unknown_button)
    
    try:
        # Connecter aux lunettes
        glasses.find()
        glasses.open()
        
        print("✅ Système d'événements activé!")
        print("🕶️  Appuyez sur les boutons des lunettes pour tester")
        print("✋ Ctrl+C pour quitter\n")
        
        # Boucle principale - le programme reste en vie
        while True:
            time.sleep(1)  # Attendre - les événements sont gérés automatiquement
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du programme...")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        
    finally:
        # Nettoyage
        glasses.close()
        print("🔌 Connexion fermée")

if __name__ == "__main__":
    main()
