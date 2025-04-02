document.addEventListener('DOMContentLoaded', function() {
    // Obter todos os elementos de contagem regressiva
    const countdownElements = document.querySelectorAll('.countdownTimer');
    
    // Verificar se existem leilões ativos
    if (countdownElements.length === 0) return;
    
    // Obter as datas de término dos leilões
    const leiloesData = [];
    countdownElements.forEach(element => {
        const leilaoId = element.closest('.timeCount').dataset.leilaoId;
        const dataFim = element.dataset.endTime; // Isso será definido no template
        
        if (dataFim) {
            leiloesData.push({
                element,
                leilaoId,
                endTime: new Date(dataFim).getTime()
            });
        }
    });
    
    // Função para atualizar todos os contadores
    function updateAllCountdowns() {
        const now = new Date().getTime();
        
        leiloesData.forEach(leilao => {
            const distance = leilao.endTime - now;
            
            if (distance < 0) {
                // Leilão expirado
                leilao.element.innerHTML = "Encerrado";
                leilao.element.classList.remove('bg-red-600');
                leilao.element.classList.add('bg-gray-500');
                return;
            }
            
            // Calcular dias, horas, minutos, segundos
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Formatar e exibir
            let displayText = '';
            if (days > 0) displayText += `${days}d `;
            displayText += `${hours.toString().padStart(2, '0')}h ${minutes.toString().padStart(2, '0')}m ${seconds.toString().padStart(2, '0')}s`;
            
            leilao.element.innerHTML = displayText;
            
            // Mudar cor se faltar menos de 1 hora
            if (distance < 3600000) { // 1 hora em ms
                leilao.element.classList.remove('bg-red-600');
                leilao.element.classList.add('bg-yellow-500');
            }
            
            // Mudar cor se faltar menos de 10 minutos
            if (distance < 600000) { // 10 minutos em ms
                leilao.element.classList.remove('bg-yellow-500');
                leilao.element.classList.add('bg-red-600', 'animate-pulse');
            }
        });
    }
    
    // Atualizar imediatamente e depois a cada segundo
    updateAllCountdowns();
    const countdownInterval = setInterval(updateAllCountdowns, 1000);
    
    // Integração com WebSocket para atualizar quando um leilão termina
    const socket = io();
    socket.on('leilao_encerrado', function(data) {
        const leilao = leiloesData.find(l => l.leilaoId === data.leilao_id);
        if (leilao) {
            leilao.element.innerHTML = "Encerrado";
            leilao.element.classList.remove('bg-red-600', 'animate-pulse');
            leilao.element.classList.add('bg-gray-500');
        }
    });
});