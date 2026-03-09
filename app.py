from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)

# Cria brain.json vazio se não existir
if not os.path.exists("brain.json"):
    with open("brain.json", "w", encoding="utf-8") as f:
        json.dump({}, f)

# Funções para carregar e salvar o cérebro
def carregar():
    with open("brain.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(data):
    with open("brain.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Endpoint de chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("msg", "").lower()

    brain = carregar()

    if msg in brain:
        resposta = random.choice(brain[msg])
    else:
        resposta = "Ainda não sei responder 😅"

    return jsonify({"reply": resposta})

# Endpoint para ensinar a IA
@app.route("/learn", methods=["POST"])
def learn():
    data = request.json
    pergunta = data["pergunta"].lower()
    resposta = data["resposta"]

    brain = carregar()
    if pergunta not in brain:
        brain[pergunta] = []

    brain[pergunta].append(resposta)
    salvar(brain)

    return jsonify({"status": "aprendido"})

@app.route("/")
def home():
    return "IA rodando no Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
