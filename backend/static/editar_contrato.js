document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('edit_contract_form');

    form.addEventListener('submit', function(event) {

        var contractIdValue = document.getElementById('contract_id').value;
        var contractNumber = contractIdValue.split('/')[0];

        document.getElementById('contract_id').value = contractNumber;

        event.preventDefault();

        submitContract();
    });
});

function submitContract() {
    var contractData = {
        contract_id: $('#contract_id').val(),
        contract_type: $('#contract_type').val(),
        contract_status: $('#contract_status').val(),
        address_obs: $('#address_obs').val(),
        contract_comments: $('#contract_comments').val()
    };

    console.log('Contract Data:', contractData);
    $.ajax({
        url: '/submit_edit_contract',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(contractData),
        success: function(response) {
            console.log('Contrato enviado com sucesso:', response);

            if (response.success) {
                if (response.redirect_url) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Contrato Atualizado!',
                        text: 'O contrato foi atualizado com sucesso.',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        window.location.href = response.redirect_url;
                    });
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'Contrato Atualizado!',
                        text: 'O contrato atualizado com sucesso.',
                        confirmButtonText: 'OK',
                        timer: 3000
                    });
                }
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Erro!',
                    text: 'Não foi possível atualizar o contrato: ' + response.message,
                    confirmButtonText: 'Tente Novamente'
                });
            }
        },
        error: function(error) {
            console.error('Erro ao enviar contrato:', error);
        }
    });
}
