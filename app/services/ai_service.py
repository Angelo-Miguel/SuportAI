# app/service/ai_service.py
from g4f.client import Client
from app.database.db_connection import MySQLConnection

# Classe dos servicos da IA
class IaService():
    def __init__(self):
        # FIXME: self.db = MySQLConnection() conflito de usar singleton e threads
        self.client = Client()
        # Prompts da IA
        self.transfer_trigger = "estou transferindo seu atendimento para um agente humano"
        self.prompt_base_template = (
            "Prompt (siga todas as instruções com atenção):\n"
            "Você é uma Inteligência Artificial especializada em suporte técnico de TI.\n"
            "Seu objetivo é auxiliar usuários leigos, com linguagem simples, objetiva e empática.\n\n"

            "### Etapas obrigatórias do atendimento:\n"
            "1. Sempre inicie com uma **triagem inicial**, fazendo apenas **uma pergunta por vez**, como:\n"
            "   - O que está acontecendo?\n"
            "   - Há quanto tempo o problema ocorre?\n"
            "   - Houve alguma mudança recente no sistema ou equipamento?\n\n"

            "2. Apresente apenas **uma solução por vez** e aguarde a resposta do usuário antes de continuar.\n\n"

            "3. Avalie constantemente a situação. Se notar **qualquer um** dos sinais abaixo:\n"
            "   - O problema for muito **complexo**,\n"
            "   - O usuário demonstrar que **não entende de TI**, ou\n"
            "   - O usuário solicitar a transferência,\n"
            "então você deve **interromper o atendimento** imediatamente e dizer (sem alterar a frase):\n"
            "**'A partir deste momento, estou transferindo seu atendimento para um agente humano.'**\n"
            "Depois disso, **não ofereça mais nenhuma solução.**\n"
        )
        self.prompt_warning_2 = (
            "\n⚠️ Atenção: já foram realizadas 2 tentativas de solução sem sucesso.\n"
            "Você tem **mais uma única chance** de resolver o problema antes de transferir.\n"
            "Se não tiver certeza da solução, prefira aprofundar a triagem com perguntas mais detalhadas para facilitar a análise do técnico.\n"
        )
        self.prompt_final_transfer = (
            "\n🚨 Atenção: foram feitas 3 ou mais tentativas de solução sem sucesso.\n"
            "A partir de agora, você **deve encerrar seu atendimento imediatamente** e dizer exatamente:\n"
            "**'A partir deste momento, estou transferindo seu atendimento para um agente humano.'**\n"
            "Depois disso, **não ofereça mais nenhuma resposta técnica.**\n"
        )
        self.prompt_general_reminder = (
            "\nLembre-se: se o número de tentativas falhas for **igual ou superior a 3**, "
            "ou se identificar que o problema é complexo ou que o usuário é leigo, "
            "você deve transferir o atendimento conforme instruído acima.\n"
        )
        
    def chat_with_ai(self, prompt, ticket_id):
        history, attempt_count = self.recovery_history(ticket_id)

        # TODO: terminar o prompt
        self.base_prompt = self.prompt_base_template
        match attempt_count:
            case 2:
                self.base_prompt += self.prompt_warning_2
            case 3 | 4 | 5:  # garantindo que mais de 3 transfere
                self.base_prompt += self.prompt_final_transfer
            case _:
                self.base_prompt += self.prompt_general_reminder
            
        messages = [{"role": "system", "content": self.base_prompt}]

        if history:
            history.pop()  # Remove a última mensagem do histórico 
            # troca a role de ia para assistent para a IA perceber que é o historico
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
        conn = MySQLConnection().get_connection()  # cria nova conexão para cada thread #HACK: conflito singleton e threads
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                'SELECT message, role FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC',
                (ticket_id,)
            )
            results = cursor.fetchall()
           
            if results:
                # Conta a quantidade de tentativas da IA
                attempt_count = sum(1 for row in results if row['role'] == 'ai') or 0 # type: ignore # HACK
                formatted_results = [
                    {
                        "role": "system" if row['role'] == 'ai' else row['role'], # type: ignore # HACK
                        "content": row['message']  # type: ignore # HACK
                    }
                    for row in results
                ]
                return formatted_results, attempt_count
            
            return None, None
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close() 