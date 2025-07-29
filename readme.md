> [!WARNING]
> Este repositório está em desenvolvimento ativo (Work in Progress). Mudanças frequentes podem ocorrer.

# Suport AI - Sistema de Atendimento Técnico com IA
Este projeto é uma aplicação web desenvolvida em Flask para gerenciamento de chamados técnicos, integrando uma Inteligência Artificial para triagem inicial e suporte ao usuário. O sistema permite cadastro, login, abertura de tickets, chat em tempo real via Socket.IO e transferência automática para agentes humanos quando necessário.

## Funcionalidades

- Cadastro e autenticação de usuários
- Dashboard para visualização de chamados
- Abertura de novos tickets
- Chat em tempo real para atendimento
- Triagem inicial automatizada por IA (OpenAI)
- Transferência automática para agente humano após tentativas falhas
- Avaliação do atendimento

## Estrutura do Projeto

.\
├── main.py\
├── requirements.txt\
├── .env\
├── app/\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ├── controllers/        # Rotas e lógica de controle\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ├── database/           # Conexão e migrações do banco\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ├── models/             # Modelos de dados (ORM)\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ├── services/           # Regras de negócio, IA, helpers\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    ├── static/             # Arquivos acessíveis publicamente\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    │&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ├── css/            # Estilos (style.css, reset.css, etc.)\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    │&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ├── font/           # Fontes personalizadas (.woff, .ttf, \etc.)\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    │&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   ├── img/            # Imagens do projeto\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    │&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   └── js/             # Scripts JS\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    └── templates/          # Arquivos HTML renderizados (Jinja2)\

## Instalação

1. Clone o repositório:
      ```sh
      git clone https://github.com/Angelo-Miguel/SuportAI.git
      cd SuportAI

2. Instale as dependências:
      ```sh
      pip install -r requirements.txt

3. Configure o arquivo .env com as variáveis do banco de dados e da OpenAI:
      ```sh
      HOST_DB=localhost
      USER_DB=seu_usuario
      PASSWORD_DB=sua_senha
      PORT_DB=3306
      DATABASE_DB=nome_do_banco
      SECRET_KEY=sua_secret_key
      OPENAI_API_KEY=sua_openai_key
      FLASK_HOST=0.0.0.0
      FLASK_PORT=5000
      DEBUG=True

4. Execute a aplicação:
      ```sh
      python [main.py](http://_vscodecontentref_/1)
      
## Tecnologias Utilizadas
- Python 3.11+
- Flask
- Flask-SocketIO
- MySQL
- OpenAI API
- HTML, CSS, JavaScript

## Colaboradores
<table>
  <tr>
      <td align="center">
      <a href="https://github.com/Angelo-Miguel" title="GitHub de Angelo Miguel Santa Rosa">
        <img src="https://avatars.githubusercontent.com/u/127904294?v=4" width="100px;" alt="Foto do Angelo Miguel Santa Rosa no GitHub"/><br>
        <sub>
          <b>Angelo Miguel</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Gustavo-Trento123" title="GitHub de Gustavo Natan Trento">
        <img src="https://avatars.githubusercontent.com/u/127904295?v=4" width="100px;" alt="Foto do Gustavo Natan Trento no GitHub"/><br>
        <sub>
          <b>Gustavo Natan Trento</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## Licença
Este projeto é apenas para fins acadêmicos.

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.
