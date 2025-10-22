import cv2
import os
import numpy as np
import pandas as pd
from model.reconhecimento import carregar_banco, salvar_banco
from controller.geraId import gerar_id
import face_recognition

DB_PATH = "model/database/alunos.csv"

def codificar_rosto(frame):
    """Codifica o rosto capturado."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    if len(encodings) > 0:
        return encodings[0]
    return None

def cadastrar_aluno(nome):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    df = carregar_banco()

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro ao abrir a câmera.")
        return

    print("Pressione ESPAÇO para capturar o rosto ou ESC para sair.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar imagem.")
            break

        cv2.imshow("Cadastro de Aluno", frame)
        key = cv2.waitKey(1)

        if key == 32:  # Tecla espaço
            aluno_id = gerar_id()
            encoding = codificar_rosto(frame)
            if encoding is not None:
                new_row = pd.DataFrame([{
                    "id": aluno_id,
                    "nome": nome,
                    "encoding": np.array2string(encoding, separator=',')
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                salvar_banco(df)
                print(f"✅ Aluno '{nome}' cadastrado com ID {aluno_id}.")
            else:
                print("Nenhum rosto detectado. Tente novamente.")
            break

        elif key == 27:  # ESC
            print("Cadastro cancelado.")
            break

    cam.release()
    cv2.destroyAllWindows()
