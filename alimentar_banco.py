from pymongo import MongoClient
import random

# --- Conexão com o MongoDB Atlas ---
client = MongoClient("uri")
db = client["db_name"]
collection = db["collection_name"]

# --- Gera 50.000 documentos ---
docs = []
for i in range(1, 50001):
    encoding = [random.random() for _ in range(128)]  # 128 doubles aleatórios
    doc = {
        "id": i,
        "nome": f"Pessoa_{i}",
        "encoding": encoding
    }
    docs.append(doc)

# --- Insere em lotes (pra evitar travar o Atlas) ---
batch_size = 1000
for j in range(0, len(docs), batch_size):
    batch = docs[j:j + batch_size]
    collection.insert_many(batch)
    print(f"Inseridos {j + len(batch)} documentos...")

print("✅ Inserção concluída com sucesso!")
