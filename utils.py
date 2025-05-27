import requests
import json

class AI :
    def __init__(self, token: str, url: str, model: str):
        self.token = token
        self.url = url + "chat/completions" if url[-1] == "/" else url + "/chat/completions"
        self.model = model

    def send_response(self, history: list, ask: str) :
        history.append({
            'role': 'user',
            'content': ask
        })
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
    
class Files :
    def get_chats():
        with open('data.json', 'r') as file :
            return json.load(file)['chats']
    
    def get_history(name_chat: str) :
        with open(f'/chats/{name_chat}.json', 'r') as file :
            return json.load(file)
        
    def load_history(name_chat: str, history: dict) :
        with open(f'/chats/{name_chat}.json', 'w') as file :
            return json.dump(history, file, indent=4)
        
    def new_chat(name_chat: str) :
        with open(f'/chats/{name_chat}.json', 'w') as file :
            return json.dump({}, file, indent=4)