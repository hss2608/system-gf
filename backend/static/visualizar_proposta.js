document.addEventListener('DOMContentLoaded', function() {
    const detalhesProposta = document.querySelectorAll('.proposta-visualizacao');

    let idsVistos = new Set();

    detalhesProposta.forEach((detalhe) => {
        const proposalId = detalhe.getAttribute('data-proposal-id');

        if (idsVistos.has(proposalId)) {
            detalhe.style.display = 'none';
        } else {
            idsVistos.add(proposalId);
        }
    });
});