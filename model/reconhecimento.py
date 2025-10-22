import os
import pandas as pd

DB_PATH = "model/database/alunos.csv"

def carregar_banco():
    if os.path.exists(DB_PATH):
        return pd.read_csv(DB_PATH)
    return pd.DataFrame(columns=["id", "nome", "encoding"])

def salvar_banco(df):
    df.to_csv(DB_PATH, index=False)
