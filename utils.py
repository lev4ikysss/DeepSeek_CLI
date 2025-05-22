import requests
import json

class AI :
    def __init__(self, token: str, url: str, model: str):
        self.token = token
        self.url = url
        self.model = model

    def send_response(self, history: list) :
        response = requests.post(
            url=self.url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": self.model,
                "messages": history
            })
        ).json()
        history.append({
            'role': 'assistant',
            'content': response['choices'][0]['message']['content']
        })
        return history