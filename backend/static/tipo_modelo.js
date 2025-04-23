function populateManufacturer() {
    $.ajax({
        type: 'GET',
        url: '/get_manufacturer',
        success: function(data) {
            console.log('Received manufacturer:', data);
            if (data && data.success) {
                var manufacturers = data.manufacturer;
                var selectElement = $('#manufacturer_id');
                // selectElement.empty();
                selectElement.append($('<option>').val('').text('Fabricantes...'));

                manufacturers.forEach(function(fabricante) {
                    console.log('Fabricante: ', fabricante);
                    var optionText = fabricante.acronym + ' | ' + fabricante.description;
                    var option = $('<option>').val(fabricante.manufacturer_id).text(optionText);

                    selectElement.append(option);
                });
            } else {
                console.error('Error fetching manufacturer:', data.error);
            }
        },
        error: function(error) {
            console.error('Error fetching manufacturer:', error);
        }
    });
}

function populateKvaGroup() {
    $.ajax({
        type: 'GET',
        url: '/get_kva_group',
        success: function(data) {
            console.log('Received kva group:', data);
            if (data && data.success) {
                var groups = data.kva_group;
                var selectElement = $('#kva_group_id');
                // selectElement.empty();
                selectElement.append($('<option>').val('').text('Grupos de KVA...'));

                groups.forEach(function(grupo) {
                    console.log('Grupo de KVA: ', grupo);
                    var optionText = grupo.kva_group_description;
                    var option = $('<option>').val(grupo.kva_group_id).text(optionText);

                    selectElement.append(option);
                });
            } else {
                console.error('Error fetching kva group:', data.error);
            }
        },
        error: function(error) {
            console.error('Error fetching kva group:', error);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    populateManufacturer();
    populateKvaGroup();
});

document.getElementById('model-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/modelo', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_modelos';
        } else {
            alert('Erro ao cadastrar tipo de modelo.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});
