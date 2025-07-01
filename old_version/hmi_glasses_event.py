import pywinusb.hid as hid
import threading
from enum import Enum
from typing import Callable, Optional

class ButtonEvent(Enum):
    CENTER = "center"
    CENTER_SOUND = "center_sound"
    PLUS = "plus"
    MINUS = "minus"
    UNKNOWN = "unknown"

class GlassesHMI:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None

        self.id_button = None
        self.previous_id_button = None

        # Système d'événements
        self.event_callbacks = {}
        self.button_pressed_lock = threading.Lock()
        
        # Mapping des boutons
        self.button_mapping = {
            140: ButtonEvent.CENTER,
            141: ButtonEvent.CENTER_SOUND,
            143: ButtonEvent.PLUS,
            139: ButtonEvent.MINUS
        }

    def register_callback(self, event: ButtonEvent, callback: Callable):
        """Enregistre une fonction callback pour un événement de bouton"""
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)
        print(f"Callback enregistré pour l'événement: {event.value}")

    def unregister_callback(self, event: ButtonEvent, callback: Callable):
        """Supprime une fonction callback pour un événement de bouton"""
        if event in self.event_callbacks and callback in self.event_callbacks[event]:
            self.event_callbacks[event].remove(callback)

    def _trigger_event(self, event: ButtonEvent):
        """Déclenche tous les callbacks associés à un événement"""
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                try:
                    # Exécute le callback dans un thread séparé pour éviter les blocages
                    thread = threading.Thread(target=callback, args=(event,))
                    thread.daemon = True
                    thread.start()
                except Exception as e:
                    print(f"Erreur lors de l'exécution du callback pour {event.value}: {e}")

    def find(self):
        """Find and connect to the USB device"""
        device_filter = hid.HidDeviceFilter(vendor_id=self.vendor_id, product_id=self.product_id)
        devices = device_filter.get_devices()
        print(f"Found {len(devices)} devices matching VID: {self.vendor_id}, PID: {self.product_id}")
        
        if devices:
            for idx, device in enumerate(devices):
                print(f"[{idx}] Device: {device.vendor_name} ({device.product_name})")
            input_idx = int(input("Select device index: "))
            self.device = devices[input_idx]
            print(f"Connected to: {self.device.vendor_name} ({self.device.product_name})")
        else:
            print("No matching USB device found.")

    def open(self):
        """Open the device and set up the data handler"""
        if self.device:
            self.device.set_raw_data_handler(self._data_handler)
            self.device.open()
            print("Device opened and ready.")
        else:
            print("Device not found, cannot open.")

    def _data_handler(self, data):
        """Handle incoming USB data"""
        print(f"Data received: {data}")
        if len(data) == 3:
            with self.button_pressed_lock:
                self.previous_id_button = self.id_button
                self.id_button = data[1]
                
                # Détection de la libération du bouton (passage à 0)
                if self.id_button == 0 and self.previous_id_button:
                    button_event = self.button_mapping.get(
                        self.previous_id_button, 
                        ButtonEvent.UNKNOWN
                    )
                    
                    print(f"Button {button_event.value} pressed (ID: {self.previous_id_button})")
                    
                    # Déclenche l'événement correspondant
                    self._trigger_event(button_event)
                    
                    if button_event == ButtonEvent.UNKNOWN:
                        print(f"Unknown button ID: {self.previous_id_button}")
                    
    def close(self):
        """Close the device connection"""
        if self.device:
            self.device.close()
            print("Device closed.")

# Example usage
THINKREALITY_VENDOR_ID = 0x17EF
THINKREALITY_PRODUCT_ID = 0xB813

# This script demonstrates how to use the GlassesHMI class to handle button events
# and register callbacks for specific button presses.
if __name__ == "__main__":
    def on_center_button(event):
        print(f"Callback déclenché pour: {event.value}")
    
    def on_plus_button(event):
        print(f"Callback PLUS déclenché pour: {event.value}")

    # Initialize the GlassesUI with the appropriate vendor and product IDs
    glasses = GlassesHMI(
        vendor_id=THINKREALITY_VENDOR_ID, 
        product_id=THINKREALITY_PRODUCT_ID
    )
    
    # Enregistrer des callbacks
    glasses.register_callback(ButtonEvent.CENTER, on_center_button)
    glasses.register_callback(ButtonEvent.CENTER_SOUND, on_center_button)
    glasses.register_callback(ButtonEvent.PLUS, on_plus_button)
    
    glasses.find() # Find the device
    glasses.open() # Open the device

    input("Press Enter to exit...\n")
    glasses.close()
