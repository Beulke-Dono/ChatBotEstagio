# Chatbot B&Bar

Este projeto é um chatbot desenvolvido para o **B&Bar**, um bar fictício. O chatbot, chamado **Sebas**, utiliza inteligência artificial para fornecer assistência aos clientes, responder perguntas e fornecer informações sobre o estabelecimento.

---

## **Tecnologias Utilizadas**

- **Frontend**:
  - HTML, CSS e JavaScript.
  - Biblioteca [Marked.js](https://github.com/markedjs/marked) para renderizar Markdown.
- **Backend**:
  - Python com Flask.
  - Integração com a API do [Saturn](https://stec.cx/saturn/studio/api-doc) para processamento de mensagens.

---

### **Arquivos Principais**

1. **[`routes.py`](app/routes.py)**:
   - Contém as rotas do Flask para renderizar a página do chat e processar as mensagens do usuário.
   - Integra-se com a API do Saturn para obter respostas do chatbot.

2. **[`config.py`](app/config.py)**:
   - Armazena as configurações do projeto, como URLs da API e chaves de autenticação.

3. **[`run.py`](run.py)**
   - O arquivo que executa o chatbot. O rode no terminal.
---

## **Como Implementar o Projeto**

### **Pré-requisitos**

- Python 3.13 instalado.
- Credenciais do Saturn: ClientID e ProjectID.

### **Instale os Requerimentos**

- `pip install -r requirements.txt`

### **Configure o `config.py`**

- SATURN_API_URL = "URL_DA_API_DO_SATURN"
- SATURN_CLIENT_ID = "SEU_CLIENT_ID"
- SATURN_PROJECT_ID = "SEU_PROJECT_ID"
- SATURN_SERVICE = "NOME_DO_SERVICO"
- SATURN_WEB_SEARCH = True  # ou False por padrão

### **Chave Secreta (Opcional)**

- No arquivo [`__init__.py`](app/__init__.py) configure sua chave secreta.

---

## **Execute o Projeto**

- `python run.py`
