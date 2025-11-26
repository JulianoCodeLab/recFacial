from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Config Mongo
MONGO_URI = "uri"
client = MongoClient(MONGO_URI)
db = client["db_name"]
collection = db["collection_name"]

# Quantidade total e número de threads
TOTAL = 5000
THREADS = 50             # 50 leituras simultâneas
POR_THREAD = TOTAL // THREADS

def ler_blocos(skip_qtd):
    """Lê um bloco de registros para simular carga."""
    docs = list(collection.find({}, {"_id": 0}).skip(skip_qtd).limit(POR_THREAD))
    return len(docs)

print(f"Iniciando teste com {THREADS} leituras simultâneas ({TOTAL} docs)...")

start = time.time()

futures = []
with ThreadPoolExecutor(max_workers=THREADS) as executor:
    for i in range(THREADS):
        skip = i * POR_THREAD
        futures.append(executor.submit(ler_blocos, skip))

total_lido = 0
for future in as_completed(futures):
    total_lido += future.result()

fim = time.time()

print(f"\n Total lido: {total_lido}")
print(f" Tempo total: {fim - start:.2f} segundos")
