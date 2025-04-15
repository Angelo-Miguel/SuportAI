from g4f.client import Client

client = Client()

def chat_with_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente de suporte para TI. Responda com soluções simples e diretas que um usuário final que não entenda do assunto possa seguir. Caso não consiga transfira a conversa para o agente humano."},
            {"role": "user", "content": prompt}
        ],
        web_search=False
    )
    return response.choices[0].message.content

# Loop de conversa
while True:
    user_input = input("Você: ")
    if user_input.lower() in ["sair", "exit", "quit"]:
        break
    response = chat_with_openai(user_input)
    print("Bot:", response)
