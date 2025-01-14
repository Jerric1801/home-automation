from somfy.api import SomfyAPI

class SomfyCommands:
    def __init__(self, api: SomfyAPI, device_name):
        self.api = api
        self.device_name = device_name
        self.device_id = None

    def find_device_id(self):
        """Find the device ID based on the device name."""
        setup = self.api.get_setup()
        for device in setup.get("devices", []):
            if self.device_name in device["label"]:
                self.device_id = device["deviceURL"]
                print(f"Found device '{self.device_name}' with ID: {self.device_id}")
                return self.device_id
        raise Exception(f"Device '{self.device_name}' not found.")

    def close_blinds(self):
        """Close the Somfy blinds."""
        if not self.device_id:
            self.find_device_id()
        return self.api.send_command(self.device_id, "close")

    def open_blinds(self):
        """Open the Somfy Blinds"""
        if not self.device_id:
            self.find_device_id()
        return self.api.send_command(self.device_id, "open")