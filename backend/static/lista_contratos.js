document.querySelectorAll('.contrato').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.contrato').forEach(i => i.classList.remove('selecionado'));
        this.classList.add('selecionado');
        document.getElementById('visualizar').disabled = false;
        document.getElementById('alterar').disabled = false;
        document.getElementById('imprimir').disabled = false;
        document.getElementById('custos_parada').disabled = false

        const contractId = this.getAttribute('data-contract-id').split('/')[0];
        const proposalElement = document.getElementById('proposal-id');
        const proposalId = proposalElement.textContent.trim();
        console.log(contractId)
        console.log(proposalId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = '/contrato/visualizar/' + contractId + '/' + proposalId;
        };
        document.getElementById('alterar').onclick = function() {
            window.location.href = '/contrato/alterar/' + contractId + '/' + proposalId;
        };
        document.getElementById('imprimir').onclick = function() {
            window.location.href = '/contrato/imprimir/' + contractId + '/' + proposalId;
        };
        document.getElementById('custos_parada').onclick = function() {
            window.location.href = '/custos_parada/' + contractId + '/' + proposalId;
        };
    });
});
