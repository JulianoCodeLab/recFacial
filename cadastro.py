import cv2
import os
import numpy as np
import pandas as pd
from util.reconhecimento import carregar_banco, salvar_banco
from geraId import gerar_id
import face_recognition

DB_PATH = "database/alunos.csv"

def codificar_rosto(frame):
    """Codifica o rosto a partir do frame (numpy.ndarray)."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    if len(encodings) > 0:
        return encodings[0]
    return None

def cadastrar_aluno(nome):
    # Garantir que a pasta do banco exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Carregar ou criar banco de dados
    df = carregar_banco()  

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Não foi possível abrir a câmera")
        return

    print("Pressione ESPAÇO para capturar o rosto ou ESC para sair.")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Não foi possível ler o frame da câmera")
                break

            cv2.imshow("Cadastro de Aluno", frame)
            key = cv2.waitKey(1)

            # Captura com ESPAÇO
            if key == 32:
                aluno_id = gerar_id()
                encoding = codificar_rosto(frame)

                if encoding is not None:
                    new_row = pd.DataFrame([{
                        "id": aluno_id,
                        "nome": nome,
                        "encoding": np.array2string(encoding, separator=' ')
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    salvar_banco(df)
                    print(f"Aluno '{nome}' cadastrado com sucesso com ID {aluno_id}!")
                else:
                    print("Nenhum rosto detectado. Tente novamente.")
                break

            # Sair com ESC
            elif key == 27:
                print("Cadastro cancelado pelo usuário.")
                break

            # Fecha se a janela for fechada
            if cv2.getWindowProperty("Cadastro de Aluno", cv2.WND_PROP_VISIBLE) < 1:
                print("Janela fechada pelo usuário.")
                break

    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    nome = input("Digite o nome do aluno: ").strip()
    if nome:
        cadastrar_aluno(nome)
    else:
        print("Nome inválido. Saindo...")
