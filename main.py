#!/usr/share/ai-shell/.venv/bin/python3
import click
import utils

Functon = utils.Work()

@click.group()
def main() :
    pass

@main.command()
@click.argument("msg", type=str, help="Message for response")
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
    print(f"Chats: {*chats}")

if __name__ == "__main__" :
    main()