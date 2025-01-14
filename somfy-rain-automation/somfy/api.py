import requests

class SomfyAPI:
    def __init__(self, username, password, device_url):
        self.username = username
        self.password = password
        self.device_url = device_url
        self.base_url = f"https://{self.device_url}/enduser-mobile-web/enduserAPI"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.session_id = None

    def login(self):
        """Login to the Somfy API and retrieve a session ID."""
        url = f"{self.base_url}/login"
        payload = {
            "userId": self.username,
            "userPassword": self.password
        }
        response = requests.post(url, headers=self.headers, data=payload)
        if response.status_code == 200:
            self.session_id = response.cookies.get("JSESSIONID")
            print(f"Successfully logged in. Session ID: {self.session_id}")
            return self.session_id
        else:
            print(f"Failed to log in: {response.text}")
            raise Exception("Login failed")

    def get_setup(self):
        """Get the user's setup, including available devices."""
        if not self.session_id:
            self.login()

        url = f"{self.base_url}/setup"
        headers = {
            "Cookie": f"JSESSIONID={self.session_id}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            setup = response.json()
            print("Setup retrieved successfully.")
            return setup
        else:
            print(f"Failed to retrieve setup: {response.text}")
            raise Exception("Setup retrieval failed")

    def send_command(self, device_id, command_name):
        """Send a command to a specific device."""
        if not self.session_id:
            self.login()

        url = f"{self.base_url}/exec/apply"
        headers = {
            "Cookie": f"JSESSIONID={self.session_id}",
            "Content-Type": "application/json"
        }
        payload = {
            "actions": [
                {
                    "deviceURL": device_id,
                    "commands": [
                        {
                            "name": command_name,
                            "parameters": []
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Command '{command_name}' sent to device '{device_id}' successfully.")
            return True
        else:
            print(f"Failed to send command: {response.text}")
            raise Exception("Command execution failed")