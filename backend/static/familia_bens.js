document.getElementById('family-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/bens/familia', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_familias';
        } else {
            alert('Erro ao cadastrar familia de bens.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});