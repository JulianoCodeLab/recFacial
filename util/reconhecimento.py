import face_recognition
import numpy as np
import os
import pandas as pd

DB_PATH = "database/alunos.csv"
IMG_PATH = "imagens"

def carregar_banco():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=["id", "nome", "encoding", "imagem"])
    return pd.read_csv(DB_PATH)

def salvar_banco(df):
    df.to_csv(DB_PATH, index=False)

def codificar_rosto(imagem_path):
    img = face_recognition.load_image_file(imagem_path)
    faces = face_recognition.face_encodings(img)
    if len(faces) > 0:
        return faces[0]
    return None

def verificar_rosto(encoding, df):
    if len(df) == 0:
        return None
    
    encodings_salvos = [np.fromstring(e[1:-1], sep=' ') for e in df["encoding"].values]
    results = face_recognition.compare_faces(encodings_salvos, encoding)
    
    for i, match in enumerate(results):
        if match:
            return df.iloc[i]
    return None
