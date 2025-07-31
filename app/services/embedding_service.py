# TODO: terminar as embbedings
import numpy as np
import logging
from app.services.openai_client import OpenAIClient

class EmbeddingService:
    def __init__(self):
        self.client = OpenAIClient().client

        # Em produção, carregue documentos de um banco ou arquivo
        self.documents = [
            {"id": 1, "content": "Como redefinir a senha de um usuário no sistema."},
            {"id": 2, "content": "Passos para instalar o software no Windows."},
            {"id": 3, "content": "Erro comum: falha na conexão com o banco de dados."}
        ]
        self.embeddings = self._generate_embeddings()

    def _generate_embeddings(self):
        texts = [doc["content"] for doc in self.documents]
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            if not response.data:
                logging.warning("Nenhum embedding retornado para os documentos.")
                return []
            return [e.embedding for e in response.data]
        except Exception as e:
            logging.error(f"Erro ao gerar embeddings dos documentos: {e}")
            return []

    def get_relevant_chunks(self, user_input, top_k=2):
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=[user_input]
            )
            if not response.data:
                logging.warning("Nenhum embedding retornado para a consulta do usuário.")
                return []

            query_embedding = response.data[0].embedding
            similarities = []
            for i, doc_emb in enumerate(self.embeddings):
                sim = self._cosine_similarity(query_embedding, doc_emb)
                similarities.append((self.documents[i]["content"], sim))

            sorted_docs = sorted(similarities, key=lambda x: x[1], reverse=True)
            return [doc for doc, _ in sorted_docs[:top_k]]
        except Exception as e:
            logging.error(f"Erro ao buscar chunks relevantes: {e}")
            return []

    def _cosine_similarity(self, vec1, vec2):
        if vec1 is None or vec2 is None:
            return 0.0
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / (norm1 * norm2))