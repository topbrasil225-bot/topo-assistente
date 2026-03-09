from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

with open("brain.json", "r", encoding="utf-8") as f:
    brain = json.load(f)

def responder(msg):
    msg = msg.lower()

    for item in brain:
        for palavra in item["inputs"]:
            if palavra in msg:
                return random.choice(item["responses"])

    return "Não entendi muito bem 😅"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensagem = data["msg"]

    resposta = responder(mensagem)

    return jsonify({
        "reply": resposta
    })

@app.route("/")
def home():
    return "IA rodando!"

app.run(host="0.0.0.0", port=10000)