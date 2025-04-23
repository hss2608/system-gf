document.addEventListener('DOMContentLoaded', function() {
    const detalhesFabricante = document.querySelectorAll('.fabricante-visualizacao');

    let idsVistos = new Set();

    detalhesFabricante.forEach((detalhe) => {
        const manufacturerId = detalhe.getAttribute('data-manufacturer-id');

        if (idsVistos.has(manufacturerId)) {
            detalhe.style.display = 'none';
        } else {
            idsVistos.add(manufacturerId);
        }
    });
});
