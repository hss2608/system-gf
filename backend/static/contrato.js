function populateProposalData() {
    var proposalIdInput = $('#proposal_id');
    var inputValue = proposalIdInput.val();

    if (inputValue) {
        $.ajax({
            type: 'POST',
            url: '/get_proposal_data',
            data: { proposal_id: inputValue },
            success: function (data) {
                console.log('Receive proposal data:', data);
                if (data && data.success) {
                    var proposalData = data.proposal_data;
                    $('#proposal_id').val(proposalData.proposal_id || '');
                    $('#client_id').val(proposalData.client_id || '');
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
