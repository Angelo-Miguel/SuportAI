import numpy as np
import logging
import json
from app.services.openai_client import OpenAIClient
from app.database.db_connection import MySQLConnection


class EmbeddingService:
    def __init__(self):
        self.client = OpenAIClient().client
        self.db = MySQLConnection()

    def store_embedding(self, document_id, content, embedding):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO document_embeddings (document_id, content, embedding) VALUES (%s, %s, %s)",
                (document_id, content, json.dumps(embedding)),
            )
            conn.commit()
        except Exception as e:
            logging.error(f"Erro ao salvar embedding: {e}")
        finally:
            cursor.close()
            conn.close()

    def load_embeddings(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT document_id, content, embedding FROM document_embeddings"
            )
            results = cursor.fetchall()
            documents = []
            embeddings = []
            for row in results:
                documents.append({"id": row["document_id"], "content": row["content"]})
                embeddings.append(json.loads(row["embedding"]))
            return documents, embeddings
        except Exception as e:
            logging.error(f"Erro ao carregar embeddings: {e}")
            return [], []
        finally:
            cursor.close()
            conn.close()

    def generate_and_store_embedding(self, document_id, content):
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small", input=[content]
            )
            if response.data:
                embedding = response.data[0].embedding
                self.store_embedding(document_id, content, embedding)
        except Exception as e:
            logging.error(f"Erro ao gerar e salvar embedding: {e}")

    def get_relevant_chunks(self, user_input, top_k=2):
        try:
            documents, embeddings = self.load_embeddings()
            if not documents or not embeddings:
                logging.warning("Nenhum embedding encontrado no banco.")
                return []

            response = self.client.embeddings.create(
                model="text-embedding-3-small", input=[user_input]
            )
            if not response.data:
                logging.warning(
                    "Nenhum embedding retornado para a consulta do usuário."
                )
                return []

            query_embedding = response.data[0].embedding
            similarities = []
            for i, doc_emb in enumerate(embeddings):
                sim = self._cosine_similarity(query_embedding, doc_emb)
                similarities.append((documents[i]["content"], sim))

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
