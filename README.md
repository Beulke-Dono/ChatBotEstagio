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

---

## **Como o Chatbot Foi Treinado**

O chatbot **Sebas** foi treinado utilizando três tipos de abordagem:

1. **`system`**:
   - Define o comportamento geral do chatbot, incluindo sua personalidade, tom de voz e diretrizes. Inclui também informações básicas sobreo B&Bar.
   - Exemplo:
     ```markdown
     Você é um atendente do B&Bar, seu nome é Sebas. Seja sempre educado, use emojis e fale de forma formal.
     ```

2. **`training`**:
   - Contém exemplos de perguntas e respostas para treinar o chatbot.
   - Exemplo:
     ```markdown
     Cliente: Que horas é o happy hour?
     Sebas: Nosso happy hour é das 18:00 às 20:00, com drinks especiais por apenas R$ 15,00. 🍸😉
     ```

3. **`data`**:
   - Inclui parágrafos de resposta associados a palavras-chave.
   - Exemplo:
     ```markdown
     # Happy Hour
     - Palavras-chave: happy hour, promoção, desconto
     - Resposta: Nosso happy hour é das 18:00 às 20:00, com drinks especiais por apenas R$ 15,00. 🍸😉
     ```

Esses arquivos são processados pela API do Saturn, que utiliza modelos de linguagem para gerar respostas contextualizadas.

---

## **Como o Front-end se Comunica com a API**

O front-end do chatbot se comunica com o backend (Flask) através de requisições HTTP. Aqui está o fluxo de comunicação:

1. **Envio da Mensagem**:
   - Quando o usuário digita uma mensagem e pressiona "Enviar", o JavaScript faz uma requisição POST para a rota `/chat` no backend.
   - Exemplo de requisição:
     ```javascript
     fetch("/chat", {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify({ message: "Que horas é o happy hour?" })
     });
     ```

2. **Processamento no Backend**:
   - O backend recebe a mensagem, formata o texto (se necessário) e envia um payload para a API do Saturn.
   - Exemplo de payload:
     ```json
     {
         "prompt": "Que horas é o happy hour?",
         "service": "SATURN_SERVICE",
         "clientid": "SATURN_CLIENT_ID",
         "projectid": "SATURN_PROJECT_ID",
         "sessionid": "abcde"
     }
     ```

3. **Resposta da API**:
   - A API do Saturn processa a mensagem e retorna uma resposta.
   - O backend formata a resposta e a envia de volta ao front-end.
   - Exemplo de resposta:
     ```json
     "Nosso happy hour é das 18:00 às 20:00, com drinks especiais por apenas R$ 15,00. 🍸😉"
     ```

4. **Exibição no Front-end**:
   - O front-end exibe a resposta no chat, convertendo Markdown em HTML (se necessário) e rolando a tela para a parte inferior.

---

## **Como Testar o Chatbot**

Para testar o chatbot, siga os passos abaixo:

- Abra o link [http://127.0.0.1:5000] (após a execução do código) no navegador e interaja com o botão no canto inferior direito da tela.
- Um front-end se abrirá com um input de texto.
- Faça perguntas como:
  - "Que horas é o happy hour?"
  - "Onde fica o B&Bar?"
  - "Vocês têm opções sem álcool?"

As respostas devem precisas.
Tente outras perguntas e verifique as repostas do chatbot. Ele está configurado para não responder, se não puder.

## **Probelmas Esperados**

- O chatbot responde a perguntas que fogem do conexto do bar fictício (e.g. "pode fazer um botão azul em html?", será respondido).
