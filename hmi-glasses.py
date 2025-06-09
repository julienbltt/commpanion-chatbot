import pywinusb.hid as hid

class GlassesUI:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None

        self.id_button = None
        self.previous_id_button = None

    def find(self):
        """Find and connect to the USB device"""
        device_filter = hid.HidDeviceFilter(vendor_id=self.vendor_id, product_id=self.product_id)
        devices = device_filter.get_devices()

        if devices:
            self.device = devices[14]  # Assume the fourtheen matching device
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
        if len(data) == 3:
            self.previous_id_button = self.id_button
            self.id_button = data[1]
                    
    def close(self):
        """Close the device connection"""
        if self.device:
            self.device.close()
            print("Device closed.")

# Example usage
"""
if __name__ == "__main__":
    glasses = GlassesUI(vendor_id=0x1234, product_id=0x5678)  # Replace with actual VID & PID
    glasses.find()
    glasses.open()

    # Keep running (Modify as needed for actual program logic)
    input("Press Enter to exit...\n")
    glasses.close()
"""