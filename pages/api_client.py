import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_message(self, sender, receiver, message):
        """
        Sends a message using the API.
        """
        url = f"{self.base_url}/send_message"
        payload = {"sender": sender, "receiver": receiver, "message": message}
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()

    def fetch_messages(self, receiver):
        """
        Fetch messages for the receiver using the API.
        """
        url = f"{self.base_url}/fetch_messages"
        params = {"receiver": receiver}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def reset_environment(self):
        """
        Resets the messaging environment (if needed).
        """
        url = f"{self.base_url}/reset"
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
