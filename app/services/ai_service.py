# TODO: colocar rollback e close conn nas funções
from g4f.client import Client
from app.database.db_connection import MySQLConnection

class IaService():
    def __init__(self):
        self.client = Client()
        self.transfer_trigger = "estou transferindo seu atendimento para um agente humano"
        
    def chat_with_ai(self, prompt, ticket_id):
        history, attempt_count = self.recovery_history(ticket_id)  # type: ignore

        # TODO: terminar o prompt
        base_prompt = (
            f"Prompt (siga exatamente todas as instruções abaixo): "
            f"Você é uma IA de suporte técnico em TI. "
            f"Sua função é atender usuários com pouco ou nenhum conhecimento técnico, "
            f"oferecendo ajuda clara, simples e objetiva."
            f"Etapas do atendimento:"
            f"1. Sempre inicie com uma triagem inicial, fazendo apenas **uma pergunta por vez**, como:"
            f"   - O que está acontecendo?"
            f"   - Há quanto tempo o problema ocorre?"
            f"   - Houve alguma mudança recente no sistema ou equipamento?"
            f"2. Apresente apenas **uma solução por vez** e aguarde a resposta do usuário antes de continuar."
            f"3. Se ocorrer **qualquer uma** das situações abaixo:"
            f"   - O problema for muito *complexo*"
            f"   - O usuário demonstrar que **não entende de TI**"
            f"   - O usuário pedir para ser transferido"
            f"Então, informe educadamente e diga exatamente o seguinte (sem alterações na frase):"
            f"**'A partir deste momento, estou transferindo seu atendimento para um agente humano.'**"
            f"Não ofereça mais soluções."
        )
        # TODO: melhorar os ifs
        if attempt_count >= 2 and attempt_count < 3:
            base_prompt += (
                f"\nAtenção: já foram realizadas {attempt_count} tentativas de solução sem sucesso. Você so tem mais uma chance de tentar resolver antes de transferir para um técnico"
                f"Portanto, você deve ser preciso, ou apenas faça mais perguntas para a triagem, para ajudar o técnico "
            )
        elif attempt_count >= 3:
            base_prompt += (
                f"\nAtenção: já foram realizadas {attempt_count} tentativas de solução sem sucesso. "
                f"Portanto, você deve imediatamente encerrar seu atendimento e dizer exatamente a seguinte frase ao usuário "
                f"(sem nenhuma modificação): **'A partir deste momento, estou transferindo seu atendimento para um agente humano.'**. "
                f"Não ofereça mais soluções."
            )
        else:
            base_prompt += (
                f"\nLembre-se: se o número de tentativas da IA ({attempt_count}) for maior ou igual a 3, "
                f"ou se o usuário não entender de TI, O usuário pedir para ser transfirido, você deve transferir o atendimento conforme instruído acima."
            )

        messages = [{"role": "system", "content": base_prompt}]

        if history:
            history.pop()  # Remove a última mensagem do histórico
            
            corrected_history = []
            for msg in history:
                role = msg["role"]
                if role == "ai":
                    role = "assistant"
                corrected_history.append({"role": role, "content": msg["content"]})
            
            messages.extend(corrected_history)

        messages.append({"role": "user", "content": prompt})

        print("IA message:", messages) # DEBUG
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,  # type: ignore
            web_search=False
        )

        response_text = response.choices[0].message.content
        print("Resposta IA:", response_text) # DEBUG

        # Detecta se a IA transferiu o chamado
        should_transfer = self.transfer_trigger in response_text.lower()
        print("Transferir para humano?", should_transfer) # DEBUG

        return response_text, should_transfer
    
    @staticmethod
    def recovery_history(ticket_id):
        conn = MySQLConnection().get_connection()  # cria nova conexão para cada thread
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                'SELECT message, role FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC',
                (ticket_id,)
            )
            results = cursor.fetchall()
           
            if results:
                attempt_count = sum(1 for row in results if row['role'] == 'ai') or 0 # type: ignore
                formatted_results = [
                    {
                        "role": "system" if row['role'] == 'ai' else row['role'], # type: ignore
                        "content": row['message']  # type: ignore
                    }
                    for row in results
                ]
                return formatted_results, attempt_count

        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close() 