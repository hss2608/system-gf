document.querySelectorAll('.proposta').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.proposta').forEach(i => i.classList.remove('selecionada'));
        this.classList.add('selecionada');
        document.getElementById('visualizar').disabled = false;
        document.getElementById('alterar').disabled = false;
        document.getElementById('imprimir').disabled = false;
        document.getElementById('imprimir_pedido').disabled = false;

        const proposalId = this.getAttribute('data-proposal-id').split('/')[0];
        console.log(proposalId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = '/proposta/visualizar/' + proposalId;
        };
        document.getElementById('alterar').onclick = function() {
            window.location.href = '/proposta/alterar/' + proposalId;
        };
        document.getElementById('imprimir').onclick = function() {
            window.location.href = '/proposta/imprimir/' + proposalId;
        };
        document.getElementById('imprimir_pedido').onclick = function() {
            window.location.href = '/pedido/imprimir/' + proposalId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/proposta';
};
