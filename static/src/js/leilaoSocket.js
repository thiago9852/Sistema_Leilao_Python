document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    
    // Enviar novo lance
    document.querySelectorAll('.enviar-lance-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const leilaoId = this.dataset.leilaoId;
            const valorInput = this.querySelector('.lance-valor-input');
            let valor = parseFloat(valorInput.value.replace(',', '.'));

            if (!valor || isNaN(valor) || valor <= 0) {
                alert('Por favor, insira um valor válido para o lance.');
                return;
            }

            console.log("Enviando novo lance:", {
                leilao_id: leilaoId,
                valor: valor,
                usuario_id: currentUserId,
                lamport_clock: currentLamportClock
            });

            // envia para servidor
            socket.emit('novo_lance', {
                leilao_id: leilaoId,
                valor: valor,
                usuario_id: currentUserId,
                lamport_clock: currentLamportClock
            }, (response) => {
                if (response && response.error) {
                    alert(response.error);
                } else {
                    valorInput.value = '';
                    console.log("Lance enviado com sucesso");
                }
            });
        });
    });

    // Ouvir atualizações
    socket.on('atualizacao_lance', function (data) {
        console.log("Atualização recebida:", data);

        const leilaoId = data.leilao_id;
        const maiorLance = data.maior_lance;
        const usuarioNome = data.usuario_nome;

        // Atualiza os cards do leilão com os novos valores
        document.querySelectorAll(`.socket[data-leilao-id="${leilaoId}"]`).forEach(card => {
            const valorElement = card.querySelector('.current-bid-value');
            const userElement = card.querySelector('.current-bid-user');

            if (valorElement) {
                valorElement.textContent = `R$ ${maiorLance.toFixed(2).replace('.', ',')}`;
            }
            if (userElement) {
                userElement.textContent = usuarioNome ? `Por: ${usuarioNome}` : "Sem lances ainda";
            }
        });

        // Exibir notificação temporária
        showSocketNotification();
    });

    socket.on('erro_lance', function(data) {
        console.error("Erro:", data.message);
        alert(data.message);
    });
});