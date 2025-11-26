import cv2
import numpy as np
import face_recognition
from model.reconhecimento import carregar_banco, salvar_aluno
from controller.geraId import gerar_id

def codificar_rosto(frame):
    """Codifica o rosto capturado."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_frame)
    if len(encodings) > 0:
        return encodings[0]
    return None

def cadastrar_aluno(nome):
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
                # Converte o array NumPy para lista (MongoDB não armazena np.array direto)
                encoding_list = encoding.tolist()

                aluno = {
                    "id": aluno_id,
                    "nome": nome,
                    "encoding": encoding_list
                }

                salvar_aluno(aluno)
                print(f"✅ Aluno '{nome}' cadastrado com ID {aluno_id}.")
            else:
                print("Nenhum rosto detectado. Tente novamente.")
            break

        elif key == 27:  # ESC
            print("Cadastro cancelado.")
            break

    cam.release()
    cv2.destroyAllWindows()
