# Importações necessárias
from flask import Blueprint, render_template, request, jsonify, session  # Flask e seus componentes
import requests  # Para fazer requisições HTTP
import json  # Para manipulação de dados JSON
import logging  # Para registro de logs, pode ser retirado na produção
import re  # Para manipulação de strings com expressões regulares
from app.config import SATURN_API_URL, SATURN_CLIENT_ID, SATURN_PROJECT_ID, SATURN_SERVICE, SATURN_WEB_SEARCH  # Configurações do chatbot

# Criação de um Blueprint para organizar as rotas
main = Blueprint('main', __name__)

# Configuração básica de logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Rota principal que renderiza a página do chat
@main.route('/')
def index():
    """
    Rota principal que renderiza a página do chat.
    Retorna o template 'chat.html'.
    """
    return render_template('chat.html')

def formatar_texto(texto):
    """
    Formata o texto recebido para exibição no frontend.
    Converte Markdown básico (**, ###, ####, -, 1., \n) em HTML.

    Parâmetros:
        texto (str): O texto a ser formatado.

    Retorna:
        str: O texto formatado em HTML.
    """
    # Substitui **texto** por <strong>texto</strong>
    texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
    # Substitui ### Título por <h3>Título</h3>
    texto = re.sub(r'### (.*?)\n', r'<h3>\1</h3>', texto)
    # Substitui #### Subtítulo por <h4>Subtítulo</h4>
    texto = re.sub(r'#### (.*?)\n', r'<h4>\1</h4>', texto)
    # Substitui - Item por <li>Item</li> e envolve em <ul>
    texto = re.sub(r'- (.*?)\n', r'<li>\1</li>', texto)
    texto = texto.replace('<li>', '<ul><li>').replace('</li>', '</li></ul>')
    # Substitui 1. Passo por <li>Passo</li> e envolve em <ol>
    texto = re.sub(r'\d+\. (.*?)\n', r'<li>\1</li>', texto)
    texto = texto.replace('<li>', '<ol><li>').replace('</li>', '</li></ol>')
    # Substitui \n por <br>
    texto = texto.replace('\n', '<br>')
    return texto

# Rota para processar as mensagens do chat
@main.route('/chat', methods=['POST'])
def chat():
    """
    Rota que processa as mensagens do chat.
    Recebe uma mensagem do usuário, envia para a API do Saturn e retorna a resposta do chatbot.

    Método: POST
    Requisição:
        - JSON com a chave "message" contendo a mensagem do usuário.

    Retorno:
        - JSON com a resposta do chatbot ou uma mensagem de erro.
    """
    data = request.json  # Obtém os dados da requisição em formato JSON
    user_message = data.get("message", "").strip()  # Extrai a mensagem do usuário
    
    # Verifica se a mensagem está vazia
    if not user_message:
        return jsonify({"error": "Mensagem vazia."}), 400
    
    # Recupera o sessionid da sessão do Flask (ou gera um novo)
    session_id = session.get("session_id")
    
    # Prepara o payload para enviar à API do Saturn
    payload = {
        "prompt": user_message,  # Mensagem do usuário
        "service": SATURN_SERVICE,  # Serviço do chatbot
        "clientid": SATURN_CLIENT_ID,  # ID do cliente
        "projectid": SATURN_PROJECT_ID,  # ID do projeto
        "sessionid": session_id,  # ID da sessão
        "websearch": SATURN_WEB_SEARCH  # Configuração de busca na web
    }

    try:
        # Log do payload enviado
        logging.debug(f"Enviando payload para a API do Saturn: {payload}")
        
        # Faz a requisição POST para a API do Saturn
        response = requests.post(SATURN_API_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Lança uma exceção se a requisição falhar

        # Obtém a resposta da API
        api_response = response.json()
        logging.debug(f"Resposta da API do Saturn: {api_response}")

        # Extrai a resposta do chatbot
        if "response" in api_response:
            response_data = json.loads(api_response["response"])  # Converte a resposta em JSON
            bot_message = response_data.get("response", "Erro ao obter resposta do chatbot.")  # Extrai a mensagem do chatbot
        else:
            bot_message = "Erro: Resposta da API inválida."

        # Atualiza o sessionid na sessão do Flask
        if "session-id" in api_response:
            session["session_id"] = api_response["session-id"]

        # Retorna a resposta do chatbot
        return jsonify(bot_message)

    except requests.exceptions.RequestException as e:
        # Log de erro na comunicação com a API
        logging.error(f"Erro na comunicação com a API do Saturn: {str(e)}")
        return jsonify({"error": "Falha na comunicação com a API do Saturn.", "details": str(e)}), 500
    except json.JSONDecodeError as e:
        # Log de erro ao decodificar o JSON da resposta
        logging.error(f"Erro ao decodificar JSON da resposta da API: {str(e)}")
        return jsonify({"error": "Erro ao processar a resposta da API.", "details": str(e)}), 500
    