document.getElementById('client-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/cadastro', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_clientes';
        } else {
            alert('Erro ao cadastrar cliente.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});