from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Caminho para o arquivo de frases
FRASES_PATH = os.path.join(os.path.dirname(__file__), 'frases.txt')  # Ou 'frases.json'

# Função para ler o arquivo de frases
def ler_frases():
    try:
        with open(FRASES_PATH, 'r', encoding='utf-8') as file:
            if FRASES_PATH.endswith('.json'):
                return json.load(file)  # Retorna uma lista de dicionários
            else:
                return [line.strip() for line in file if line.strip()]  # Retorna uma lista de frases
    except Exception as e:
        print(f"Erro ao ler o arquivo de frases: {e}")
        return []

# Função para selecionar a frase do dia
def selecionar_frase_do_dia(frases):
    # Obtém o dia do ano (1 a 365)
    dia_do_ano = datetime.now().timetuple().tm_yday

    # Usa o dia do ano como índice para selecionar uma frase
    indice = dia_do_ano % len(frases)  # Garante que o índice esteja dentro do range
    return frases[indice]

# Rota para retornar a frase do dia
@app.route('/frase', methods=['GET'])
def frase_do_dia():
    frases = ler_frases()
    if not frases:
        return jsonify({"error": "Nenhuma frase encontrada."}), 500

    frase = selecionar_frase_do_dia(frases)
    if isinstance(frase, dict):  # Se for JSON, retorna frase e autor
        return jsonify(frase)
    else:  # Se for TXT, retorna apenas a frase
        return jsonify({"frase": frase})

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)