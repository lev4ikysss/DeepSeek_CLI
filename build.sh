#!/bin/bash

sudo mkdir -pv /usr/share/ai-shell/
sudo cp -rv * /usr/share/ai-shell/
sudo python -m venv /usr/share/ai-shell/.venv
sudo /usr/share/ai-shell/.venv/bin/pip install -r req.txt
sudo cp -v main.py /usr/bin/ai
sudo cp -v main.py /usr/bin/ai-shell
mkdir -pv ~/.local/share/ai-shell/chats/
cp -v data.json ~/.local/share/ai-shell/
cp -v chats/base_chat.json ~/.local/share/ai-shell/chats/
sudo chmod -v 777 /usr/bin/ai
sudo chmod -v 777 /usr/bin/ai-shell

echo "Success! Please run \"ai config\" for change setting"