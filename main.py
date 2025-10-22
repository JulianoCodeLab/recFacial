import cv2
import dlib
import face_recognition
from util.reconhecimento import carregar_banco, verificar_rosto, codificar_rosto
import numpy as np

def main():
    cam = cv2.VideoCapture(0)
    df = carregar_banco()

    print("Iniciando reconhecimento facial...")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces_loc = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, faces_loc)

        for (top, right, bottom, left), face_encoding in zip(faces_loc, encodings):
            match = verificar_rosto(face_encoding, df)
            
            if match is not None:
                nome = match["nome"]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"Aluno: {nome}", (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Aluno não cadastrado", (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(1) == 27:  # ESC
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
