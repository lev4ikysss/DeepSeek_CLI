#!/usr/share/ai-shell/.venv/bin/python3
import json
import os
import requests
import click

path = os.path.expanduser('~/.local/share/ai-shell/')

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
    @staticmethod
    def get_chats() -> list :
        with open(f'{path}data.json', 'r') as file :
            return json.load(file)['chats']

    @staticmethod
    def get_history(name_chat: str) -> dict :
        with open(f'{path}data.json', 'r') as file :
            chats = json.load(file)['chats']
        if not name_chat in chats :
            return {'error': 1}
        with open(f'{path}chats/{name_chat}.json', 'r') as file :
            return json.load(file)

    @staticmethod
    def load_history(name_chat: str, history: dict) -> None :
        with open(f'{path}chats/{name_chat}.json', 'w') as file :
            return json.dump(history, file, indent=4)

    @staticmethod
    def new_chat(name_chat: str) -> None :
        with open(f'{path}data.json', 'r') as file :
            data = json.load(file)
        data['chats'].append(name_chat)
        with open(f'{path}data.json', 'w') as file :
            json.dump(data, file, indent=4)
        with open(f'{path}chats/{name_chat}.json', 'w') as file :
            json.dump([], file, indent=4)

    @staticmethod
    def change_data(url: str, model: str, token: str) -> None :
        with open(f'{path}data.json', 'r') as file :
            data = json.load(file)
        data['url'] = url
        data['model'] = model
        data['token'] = token
        with open(f'{path}data.json', 'w') as file :
            json.dump(data, file, indent=4)

class Work :
    def __init__(self) :
        with open(f'{path}data.json', 'r') as file :
            data = json.load(file)
            self.chat = data['active_chat']
            self.AI = AI(data['token'], data['url'], data['model'])
        self.Files = Files()

    def new_message(self, message: str) -> str :
        history = self.Files.get_history(self.chat)
        history = self.AI.send_response(history, message)
        self.Files.load_history(self.chat, history)
        return history[-1]['content']
    
    def set_active_chat(self, name_chat: str) -> int :
        with open(f'{path}data.json', 'r') as file :
            data = json.load(file)
        if not name_chat in data['chats'] :
            return 1
        data['active_chat'] = name_chat
        with open(f'{path}data.json', 'w') as file :
            json.dump(data, file, indent=4)

Functon = Work()

@click.group()
def main() :
    pass

@main.command()
@click.argument("msg")
def ask(msg) :
    answr = Functon.new_message(msg)
    print(f'ai:\n{answr}')

@main.command()
@click.option("--url", "-u", type=str, help="URL for ai api", default=None)
@click.option("--model", "-m", type=str, help="model for ai api", default=None)
@click.option("--token", "-t", type=str, help="token for ai api", default=None)
def config(url, model, token) :
    if url == None :
        url = input("Enter url: ")
    if model == None :
        model = input("Enter model: ")
    if token == None :
        token = input("Enter token: ")
    Functon.Files.change_data(url, model, token)
    print("Success!")

@main.command()
@click.option("--name", "-n", type=str, help="name chat", default=None)
def new_chat(name) :
    if name == None :
        name = input("Enter chat name: ")
    Functon.Files.new_chat(name)
    print(f"Success create {name} chat!")

@main.command()
@click.option("--name", "-n", type=str, help="name chat", default=None)
def change_chat(name) :
    if name == None :
        name = input("Enter chat name: ")
    answr = Functon.set_active_chat(name)
    if answr == 1 :
        print("Uncorrected name, please, use \"ai new_chat [-n]\"")
    else :
        print(f"Success, current chat is: {name}")

@main.command()
@click.option("--name", "-n", type=str, help="name chat", default=None)
def see_history(name) :
    if name == None :
        name = Functon.chat
    history = Functon.Files.get_history(name)
    for msg in history :
        role = msg['role']
        content = msg['content']
        print(f'{role}:\n{content}\n')

@main.command()
def see_chats() :
    chats = Functon.Files.get_chats()
    print("Chats: ", end="")
    for chat in chats :
        print(chat, end=" ")
    print("\n")

if __name__ == "__main__" :
    main()