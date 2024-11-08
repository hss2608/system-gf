document.querySelectorAll('.cliente').forEach(item => {

    item.addEventListener('click', function() {
        document.querySelectorAll('.cliente').forEach(i => i.classList.remove('selecionado'));
        this.classList.add('selecionado');
        document.getElementById('visualizar').disabled = false;
        document.getElementById('alterar').disabled = false;

        const clientId = this.getAttribute('data-client-id');
        console.log(clientId);

        document.getElementById('visualizar').onclick = function() {
            window.location.href = '/cliente/visualizar/' + clientId;
        };
        document.getElementById('alterar').onclick = function() {
            window.location.href = '/cliente/alterar/' + clientId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/cadastro';
};
