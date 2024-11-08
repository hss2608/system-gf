// manipula a geração do contract id
function submitContractId() {
    fetch('/get_contract_id')
    .then(response => response.json())
    .then(data => {
        document.getElementById('contract_id').value = data.contract_id;
    })
    .catch(error => console.error('Error fetching contract ID:', error));
}
document.addEventListener('DOMContentLoaded', submitContractId);
    
function populateProposalData() {
    var proposalIdInput = $('#proposal_id');
    var inputValue = proposalIdInput.val();

    if (inputValue) {
        $.ajax({
            type: 'GET',
            url: '/get_proposal_data',
            data: { proposal_id: inputValue },
            success: function (data) {
                console.log('Receive proposal data:', data);
                if (data && data.success) {
                    var proposalData = data.proposal_data;
                    $('#proposal_id').val(proposalData.proposal_id || '');
                    $('#client_id').val(proposalData.client_id || '');
                    $('#start_contract').val(proposalData.start_date || '');
                    $('#end_contract').val(proposalData.end_date || '');
                    $('#contract_days').val(proposalData.period_days || '');
                    $('#delivery_address').val(proposalData.delivery_address || '');
                    $('#value').val(proposalData.value || '');

                    console.log('Client Id:', proposalData.client_id);
                } else {
                    console.error('Error fetching proposal data:', data.error);
                }
            },
            error: function (error) {
                console.error('Error fetching proposal data:', error);
            }
        });
    }
}

function populateClientProposalData() {
    var clientIdInput = $('#client_id');
    var inputValue = clientIdInput.val();

    if (inputValue) {
        $.ajax({
            type: 'POST',
            url: '/get_client_proposal_data',
            data: { client_id: inputValue },
            success: function (data) {
                console.log('Receive client proposal data:', data);
                if (data && data.success) {
                    var clientProposalData = data.client_proposal_data;
                    $('#corporate_name').val(clientProposalData.corporate_name || '');
                    $('#company_address').val(clientProposalData.company_address || '');
                    $('#cpf_cnpj').val(clientProposalData.cpf_cnpj || '');
                    $('#state_registration').val(clientProposalData.state_registration || '');
                    $('#contact_name').val(clientProposalData.contact_name || '');
                    $('#phone').val(clientProposalData.phone || '');
                    $('#billing_address').val(clientProposalData.billing_address || '');
                } else {
                    console.error('Error fetching client proposal data:', data.error);
                }
            },
            error: function (error) {
                console.error('Error fetching client proposal data:', error);
            }
        });
    }
}

function updateContractDays() {
    var startContractInput = document.getElementById('start_contract');
    var endContractInput = document.getElementById('end_contract');
    var contractDaysInput = document.getElementById('contract_days');

    if (startContractInput.value && endContractInput.value) {
        var startContractParts = startContractInput.value.split('/');
        var endContractParts = endContractInput.value.split('/');

        var startContract = new Date(
            parseInt(startContractParts[2]),
            parseInt(startContractParts[1]) - 1,
            parseInt(startContractParts[0])
        );

        var endContract = new Date(
            parseInt(endContractParts[2]),
            parseInt(endContractParts[1]) -1,
            parseInt(endContractParts[0])
        );

        var timeDifference = Math.abs(endContract.getTime() - startContract.getTime());
        var contractDays = Math.ceil(timeDifference / (1000 * 3600 * 24));

        contractDaysInput.value = contractDays;
    } else {
        contractDaysInput.value = '';
    }
    console.log(contractDays);

    // updatePricesForAllProducts()
}

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('contract-form');

    form.addEventListener('submit', function(event) {

        // Extracts just the contract number from the 'contract_id' input value
        var contractIdValue = document.getElementById('contract_id').value;
        var contractNumber = contractIdValue.split('/')[0]; // Assuming the format is "number/month/year"

        // Updates the 'contract_id' input to only contain the contract number
        document.getElementById('contract_id').value = contractNumber;

        // Submits the form programmatically after updating the contract_id value
        // this.submit();
        event.preventDefault();

        submitContract();

    });
});

function submitContract() {
    var contractData = {
        contract_id: $('#contract_id').val(),
        proposal_id: $('#proposal_id').val(),
        date_issue: $('#date_issue').val(),
        start_contract: $('#start_contract').val(),
        end_contract: $('#end_contract').val(),
        contract_days: $('#contract_days').val(),
        contract_type: $('#contract_type').val(),
        contract_status: $('#contract_status').val(),
        address_obs: $('#address_obs').val(),
        observations: $('#observations').val(),
        oenf_obs: $('#oenf_obs').val(),
        contract_comments: $('#contract_comments').val(),
        value: $('#value').val(),
    };

    console.log('Contract Data:', contractData);
    $.ajax({
        url: '/submit_contract',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(contractData),
        success: function(response) {
            console.log('Contrato enviado com sucesso:', response);
        },
        error: function(error) {
            console.error('Erro ao enviar contrato:', error);
        }
    });
}
