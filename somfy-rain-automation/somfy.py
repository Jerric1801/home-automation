import requests
import time
from dotenv import load_dotenv
import os


# Replace with your Somfy credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DEVICE_URL = os.getenv("DEVICE_URL")
DEVICE_NAME = os.getenv("DEVICE_NAME")

# API Endpoints
LOGIN_URL = f"https://{DEVICE_URL}/enduser-mobile-web/enduserAPI/login"
SETUP_URL = f"https://{DEVICE_URL}/enduser-mobile-web/enduserAPI/setup"
COMMAND_URL = f"https://{DEVICE_URL}/enduser-mobile-web/enduserAPI/exec/apply"

# Headers for the API
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

def login():
    """Login to the Cloud API and retrieve a session ID."""
    payload = {
        "userId": USERNAME,
        "userPassword": PASSWORD
    }
    response = requests.post(LOGIN_URL, headers=HEADERS, data=payload)
    if response.status_code == 200:
        session_id = response.cookies.get("JSESSIONID")
        print(f"Successfully logged in. Session ID: {session_id}")
        return session_id
    else:
        print(f"Failed to log in: {response.text}")
        raise Exception("Login failed")

def get_setup(session_id):
    """Get the user's setup, including available devices."""
    headers = {
        "Cookie": f"JSESSIONID={session_id}",
        "Content-Type": "application/json"
    }
    response = requests.get(SETUP_URL, headers=headers)
    if response.status_code == 200:
        setup = response.json()
        print("Setup retrieved successfully.")
        return setup
    else:
        print(f"Failed to retrieve setup: {response.text}")
        raise Exception("Setup retrieval failed")

def send_command(session_id, device_id, command_name):
    """Send a command to a specific device."""
    headers = {
        "Cookie": f"JSESSIONID={session_id}",
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
    response = requests.post(COMMAND_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Command '{command_name}' sent to device '{device_id}' successfully.")
    else:
        print(f"Failed to send command: {response.text}")
        raise Exception("Command execution failed")

def main():
    try:
        # Step 1: Login
        session_id = login()

        # Step 2: Retrieve setup
        setup = get_setup(session_id)

        # Step 3: Find devices and send commands
        for device in setup.get("devices", []):
            print(f"Device: {device['label']}, URL: {device['deviceURL']}")
            
            # Example: Open the blinds for 5 seconds and then stop
            if DEVICE_NAME in device["label"]:  
                device_id = device["deviceURL"]

                # Open the blinds
                send_command(session_id, device_id, "close")


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()