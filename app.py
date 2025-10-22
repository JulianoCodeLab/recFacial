from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import pandas as pd

app = Flask(__name__)
EXCEL_PATH = "base_dados.xlsx"

# Cria pasta de rostos
if not os.path.exists("rostos"):
    os.makedirs("rostos")

# Cria Excel se não existir
if not os.path.exists(EXCEL_PATH):
    df = pd.DataFrame(columns=["ID", "Nome", "Sobrenome", "Curso", "Periodo"])
    df.to_excel(EXCEL_PATH, index=False)

def gerar_id():
    df = pd.read_excel(EXCEL_PATH)
    return 1 if df.empty else df["ID"].max() + 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        curso = request.form["curso"]
        periodo = request.form["periodo"]

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "Erro ao acessar a câmera."

        nome_arquivo = f"rostos/{nome}_{sobrenome}.jpg"
        cv2.imwrite(nome_arquivo, frame)

        df = pd.read_excel(EXCEL_PATH)
        novo_id = gerar_id()
        df.loc[len(df)] = [novo_id, nome, sobrenome, curso, periodo]
        df.to_excel(EXCEL_PATH, index=False)

        return redirect(url_for("index"))

    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)
