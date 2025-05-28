import requests
import json

class AI :
    def __init__(self, token: str, url: str, model: str) :
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
    def __init__(self, path: str) :
        self.path = path

    def get_chats(self) -> list :
        with open(f'{self.path}/data.json', 'r') as file :
            return json.load(file)['chats']

    def get_history(self, name_chat: str) -> dict :
        with open(f'{self.path}/data.json', 'r') as file :
            chats = json.load(file)['chats']
        if not name_chat in chats :
            return {'error': 1}
        with open(f'{self.path}/chats/{name_chat}.json', 'r') as file :
            return json.load(file)

    def load_history(self, name_chat: str, history: dict) -> None :
        with open(f'{self.path}/chats/{name_chat}.json', 'w') as file :
            return json.dump(history, file, indent=4)

    def new_chat(self, name_chat: str) -> None :
        with open(f'{self.path}/data.json', 'r') as file :
            data = json.load(data)
        data['chats'].append(name_chat)
        with open(f'{self.path}/chats/{name_chat}', 'w') as file :
            json.dump({}, file, indent=4)

class Work :
    def __init__(self, url: str, model: str, token: str, path: str) :
        self.AI = AI(token, url, model)
        self.Files = Files(path)
        with open(f'{path}/data.json', 'r') as file :
            self.chat = json.load(file)['active_chat']

