function sendMessage() {
    const user_id = document.getElementsByName('user_id')[0].value;
    const message = document.getElementsByName('message')[0].value;

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: user_id,
            message: message,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert('mensagem enviada com sucesso!');
    })
    .catch(error => {
        alert('A mensagem não foi enviada');
    });
    
    return false; // Evita o envio padrão do formulário
}

function deleteMessage() {
    const messageIdToDelete = document.getElementById('message-id-to-delete').value;

    fetch(`/delete_message/${messageIdToDelete}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        alert('Mensagem apagada com sucesso!');
    })
    .catch(error => {
        alert('Erro ao apagar a mensagem. Por favor, tente novamente.');
    });
}

function viewAllMessages() {
    const userIdToViewMessages = document.getElementById('user-id-to-view-messages').value;

    fetch(`/get_all_messages/${userIdToViewMessages}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(messages => {
        const allMessagesContainer = document.getElementById('allMessagesContainer');
        allMessagesContainer.innerHTML = '';

        messages.forEach(msg => {
            allMessagesContainer.innerHTML += `<p>ID da Mensagem: ${msg['ID da Mensagem']}, Mensagem: ${msg['Mensagem']}</p>`;
        });

        // Abre o modal
        openModal('messageModal');
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao obter todas as mensagens. Por favor, tente novamente.');
    });
}

function viewUnreadMessages() {
    const userIdToViewUnreadMessages = document.getElementById('user-id-to-view-unread-messages').value;

    fetch(`/get_messages_unread/${userIdToViewUnreadMessages}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(messages => {
        const allMessagesContainer = document.getElementById('allMessagesContainer');
        allMessagesContainer.innerHTML = '';

        messages.forEach(msg => {
            allMessagesContainer.innerHTML += `<p>ID da Mensagem: ${msg['ID da Mensagem']}, Mensagem: ${msg['Mensagem']}</p>`;
        });

        // Abre o modal
        openModal('messageModal');
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao obter mensagens não lidas. Por favor, tente novamente.');
    });
}


function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

function closePopup(popupId) {
    var popup = document.getElementById(popupId);
    var overlay = document.querySelector('.overlay');

    popup.style.display = 'none';
    overlay.style.display = 'none';
}

function openModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'block';
}