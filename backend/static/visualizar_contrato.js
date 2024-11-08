document.addEventListener('DOMContentLoaded', function() {
    const detalhesContrato = document.querySelectorAll('.contrato-visualizacao');

    let idsVistos = new Set();

    detalhesContrato.forEach((detalhe) => {
        const contractId = detalhe.getAttribute('data-contract-id');

        if (idsVistos.has(contractId)) {
            detalhe.style.display = 'none';
        } else {
            idsVistos.add(contractId);
        }
    });
});
