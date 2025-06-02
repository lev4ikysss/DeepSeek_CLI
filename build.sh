mkdir -p /usr/share/ai-shell/chats
cp -r * /usr/share/ai-shell
python -m venv /usr/share/ai-shell/.venv
/usr/share/ai-shell/.venv/bin/pip install -r req.txt
cp main.py /usr/bin/ai
cp main.py /usr/bin/ai-shell