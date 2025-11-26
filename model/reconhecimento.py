from pymongo import MongoClient

# Configurações do MongoDB
MONGO_URI = "mongodb+srv://marley:ArrozComCarne999@detectface.clwrmeh.mongodb.net/?appName=DetectFace"  # ajuste se precisar
DB_NAME = "detectface"
COLLECTION_NAME = "faces"

# Conexão com o banco
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def carregar_banco():
    """Carrega todos os alunos do MongoDB."""
    alunos = list(collection.find({}, {"_id": 0}))  # remove o campo _id
    return alunos

def salvar_aluno(aluno):
    """Salva um novo aluno no banco.
    Exemplo de aluno: {"id": 1, "nome": "Kaique", "encoding": "..."}
    """
    collection.insert_one(aluno)

def atualizar_aluno(id_aluno, novos_dados):
    """Atualiza um aluno existente pelo id."""
    collection.update_one({"id": id_aluno}, {"$set": novos_dados})

def deletar_aluno(id_aluno):
    """Remove um aluno pelo id."""
    collection.delete_one({"id": id_aluno})
