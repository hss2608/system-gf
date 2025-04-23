document.querySelectorAll('.fabricante').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.fabricante').forEach(i => i.classList.remove('selecionada'));
        this.classList.add('selecionada');
        document.getElementById('visualizar').disabled = false;

        const manufacturerId = this.getAttribute('data-manufacturer-id');
        console.log(manufacturerId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = 'fabricante/visualizar/' + manufacturerId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/fabricante';
};
