document.getElementById('manufacturer-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/fabricante', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_fabricantes';
        } else {
            alert('Erro ao cadastrar fabricantes');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});
