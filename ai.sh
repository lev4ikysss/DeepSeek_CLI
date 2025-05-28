if [ ! -d "/usr/share/ai-shell" ]; then
    mkdir -p /usr/share/ai-shell/chats
    cp * /usr/share/ai-shell
    python -m venv /usr/share/ai-shell/.venv
    /usr/share/ai-shell/.venv/bin/pip install -r req.txt
    
fi