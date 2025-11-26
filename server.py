import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.cadastro import codificar_rosto
from model.reconhecimento import salvar_aluno
from controller.geraId import gerar_id

app = Flask(__name__)
CORS(app)

def base64_to_frame(base64_img):
    try:
        header, data = base64_img.split(',')
        img_bytes = base64.b64decode(data)
        np_array = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        return frame
    except:
        return None

@app.post("/cadastrar")
def cadastrar():
    data = request.json

    nome = data.get("nome")
    curso = data.get("curso")
    periodo = data.get("periodo")
    imagem_base64 = data.get("imagem")

    if not nome or not imagem_base64:
        return jsonify({"erro": "Nome e imagem são obrigatórios"}), 400

    frame = base64_to_frame(imagem_base64)

    if frame is None:
        return jsonify({"erro": "Imagem inválida"}), 400

    encoding = codificar_rosto(frame)
    if encoding is None:
        return jsonify({"erro": "Nenhum rosto detectado"}), 400

    aluno_id = gerar_id()

    aluno = {
        "id": aluno_id,
        "nome": nome,
        "curso": curso,
        "periodo": periodo,
        "encoding": encoding.tolist()
    }

    salvar_aluno(aluno)

    return jsonify({"mensagem": "Aluno cadastrado com sucesso!", "id": aluno_id}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
