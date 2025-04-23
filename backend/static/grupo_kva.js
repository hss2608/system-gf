function populateFamily() {
    $.ajax({
        type: 'GET',
        url: '/get_assets_family',
        success: function(data) {
            console.log('Received assets family:', data);
            if (data && data.success) {
                var families = data.assets_family;
                var selectElement = $('#family_id');
                // selectElement.empty();
                selectElement.append($('<option>').val('').text('Famílias...'));

                families.forEach(function(family) {
                    console.log('Familia: ', family);
                    var formattedId = family.family_id.toString().padStart(3, '0');
                    var optionText = formattedId + ' ' + family.family_description;
                    var option = $('<option>').val(family.family_id).text(optionText);

                    selectElement.append(option);
                });
            } else {
                console.error('Error fetching assets family:', data.error);
            }
        },
        error: function(error) {
            console.error('Error fetching assets family:', error);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    populateFamily();
});

document.getElementById('group-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const unitValueInput = document.getElementById('unit_value');
    let unitValue = unitValueInput.value;
    unitValue = unitValue.replace(/\./g, '').replace(',', '.');
    unitValueInput.value = unitValue;

    var formData = new FormData(this);
    fetch('/grupo/kva', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_grupos_kva';
        } else {
            alert('Erro ao cadastrar grupos de KVA.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});

