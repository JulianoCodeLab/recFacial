import cv2
import numpy as np
import face_recognition
from model.reconhecimento import carregar_banco

def iniciar_reconhecimento():
    alunos = carregar_banco()  # Agora retorna uma lista de dicionários

    if not alunos:  # Lista vazia
        print("Nenhum aluno cadastrado.")
        return

    encodings_cadastrados = []
    nomes = []

    # Percorre os alunos salvos no Mongo
    for aluno in alunos:
        try:
            # O campo 'encoding' agora é uma lista salva no Mongo
            enc = np.array(aluno["encoding"], dtype=np.float64)
            encodings_cadastrados.append(enc)
            nomes.append(aluno["nome"])
        except Exception as e:
            print(f"Erro ao carregar aluno {aluno.get('nome', 'desconhecido')}: {e}")
            continue

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print("Erro ao abrir a câmera.")
        return

    print("Iniciando reconhecimento facial. Pressione ESC para sair.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar imagem.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, faces)

        for (top, right, bottom, left), face_encoding in zip(faces, encodings):
            matches = face_recognition.compare_faces(encodings_cadastrados, face_encoding, tolerance=0.5)
            name = "Não cadastrado"
            color = (0, 0, 255)

            if True in matches:
                index = matches.index(True)
                name = nomes[index]
                color = (0, 255, 0)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Reconhecimento Facial", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()
