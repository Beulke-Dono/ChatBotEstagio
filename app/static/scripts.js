// Aguarda o carregamento completo do DOM antes de executar o código
document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.getElementById("chat-container");
    const chatToggleButton = document.getElementById("chat-toggle-button");
    const closeChatButton = document.getElementById("close-chat-button");

    // Função para alternar a visibilidade do chat
    function toggleChat() {
        chatContainer.classList.toggle("visible");
        // Rola para a parte inferior ao abrir o chat
        if (chatContainer.classList.contains("visible")) {
            scrollToBottom();
        }
    }

    // Abrir/fechar o chat ao clicar no botão redondo
    chatToggleButton.addEventListener("click", toggleChat);

    // Fechar o chat ao clicar no botão de fechar
    closeChatButton.addEventListener("click", toggleChat);

    // Enviar mensagem ao pressionar Enter no campo de entrada
    document.getElementById("user-message").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Função para rolar o chat para a parte inferior
    function scrollToBottom() {
        const chatBox = document.getElementById("chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Rola para a parte inferior ao carregar a página (para exibir a mensagem inicial)
    scrollToBottom();
});

// Função para enviar uma mensagem
async function sendMessage() {
    let userMessage = document.getElementById("user-message").value.trim();
    let chatBox = document.getElementById("chat-box");
    let sendButton = document.getElementById("send-button");
    let buttonText = document.getElementById("button-text");
    let buttonSpinner = document.getElementById("button-spinner");

    if (!userMessage) {
        return; // Sai da função se a mensagem estiver vazia
    }

    // Adiciona a mensagem do usuário ao chat
    appendMessage("Você", userMessage);
    document.getElementById("user-message").value = "";

    // Exibir spinner e desativar botão
    buttonText.style.display = "none";
    buttonSpinner.style.display = "block";
    sendButton.disabled = true;
    sendButton.style.cursor = "wait";

    try {
        // Faz uma requisição POST para a rota /chat com a mensagem do usuário
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }) // Converte a mensagem para JSON
        });

        // Verifica se a resposta da requisição foi bem-sucedida
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`); // Lança um erro se a resposta não for OK
        }

        // Converte a resposta para JSON
        let botMessage = await response.json();

        // Adiciona a resposta do chatbot ao chat
        appendMessage("Sebas", botMessage);

    } catch (error) {
        // Adiciona uma mensagem de erro ao chat em caso de falha na comunicação
        appendMessage("Erro", `Falha na comunicação (${error.message}).`);
    } finally {
        // Restaurar botão após resposta do chatbot
        buttonText.style.display = "block";
        buttonSpinner.style.display = "none";
        sendButton.disabled = false;
        sendButton.style.cursor = "pointer";
    }
}

// Função para adicionar uma mensagem ao chat
function appendMessage(sender, message) {
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");

    // Converte Markdown para HTML usando Marked.js
    let formattedMessage = marked.parse(message);

    // Define o conteúdo do elemento da mensagem com o nome do remetente e a mensagem formatada
    messageElement.innerHTML = `<strong>${sender}:</strong> ${formattedMessage}`;
    chatBox.appendChild(messageElement);

    // Rola o chat para a parte inferior após adicionar a mensagem
    scrollToBottom();
}

// Função para rolar o chat para a parte inferior
function scrollToBottom() {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}