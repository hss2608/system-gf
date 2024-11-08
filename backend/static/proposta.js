function submitProposalId() {
    fetch('/get_proposal_id')
    .then(response => response.json())
    .then(data => {
        document.getElementById('proposal_id').value = data.proposal_id;
    })
    .catch(error => console.error('Error fetching proposal ID:', error));
}
document.addEventListener('DOMContentLoaded', submitProposalId);

function populateClientData() { //funcao para apresentar os clientes no formulario
    var cpfCnpjInput = $('#cpf_cnpj');
    var clientDataInput = $('#client_data');
    var inputValue = cpfCnpjInput.val();

    if (inputValue) {
        $.ajax({
            type: 'POST',
            url: '/get_client_data',
            data: { cpf_cnpj: inputValue },
            success: function (data) {
                console.log('Received client data:', data);
                if (data && data.success) {
                    var clientData = data.client_data;
                    $('#client_id').val(clientData.client_id || '');
                    $('#company').val(clientData.company || '');
                    $('#contact_name').val(clientData.contact_name || '');
                    $('#phone').val(clientData.phone || '');
                    $('#email').val(clientData.email || '');
                    $('#number_store').val(clientData.number_store || '');

                    console.log('Client Id:', clientData.client_id);
                    console.log('Cpf / Cnpj:', clientData.cpf_cnpj);
                } else {
                    console.error('Error fetching client data:', data.error);
                }
            },
            error: function (error) {
                console.error('Error fetching client data:', error);
            }
        });
    }
}

function populatePaymentCondition() {
    $.ajax({
        type: 'GET',
        url: '/get_payment_condition',
        success: function(data) {
            console.log('Received payment condition:', data);
            if (data && data.success) {
                var paymentCondition = data.payment_condition;
                var selectElement = $('#payment_condition');

                // Limpa as opções anteriores
                selectElement.empty();

                // Popula o select com as novas opções
                paymentCondition.forEach(function(condition) {
                    var formattedCod = condition.cod.toString().padStart(3, '0');
                    var option_text = formattedCod + ' - ' + condition.description;
                    var option = $('<option>').val(condition.cod).text(option_text);
                    selectElement.append(option);
                });

            } else {
                console.error('Error fetching payment condition:', data.error);
            }
        },
        error: function(error) {
            console.error('Error fetching payment condition:', error);
        }
    });
}

// Chama a função ao carregar o documento
$(document).ready(function() {
    populatePaymentCondition();
});

function updateTable(productData) {
    // bloco com condicao para nao ser adicionada uma linha vazia
    if (!productData || Object.keys(productData).length === 0 || !productData.product_code) {
        console.log('Dados do produto inválidos ou faltando... Não adicionando à tabela.');
        return;
    }

    var tableBody = $('#product_table_body');
    var existingRow = tableBody.find('tr[data-product="' + productData.product_code + '"]');
        // atualizando uma nova linha
    if (existingRow.length > 0) {
        existingRow.find('.product_id_placeholder').text(productData.product_id || '');
        existingRow.find('.description_placeholder').text(productData.description || '');
        existingRow.find('.type_placeholder').text(productData.type || '');
        existingRow.find('.add_description_placeholder').text(productData.add_description || '');
        existingRow.find('.quantity_placeholder').html('<input type="number" name="quantity[]" class="quantity_input" onchange="updatePrice(this)">');
        existingRow.find('.unit_price_placeholder').html('<input type="text" name="unit_price[]" class="unit_price_input" onchange="updatePrice(this)">');
        existingRow.find('.price_placeholder').text(calculatePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        existingRow.find('.extra_hours_placeholder').html('<input type="text" name="extra_hours[]" class="extra_hours_input">');
        existingRow.find('.rental_hours_placeholder').html('<input type="text" name="rental_hours[]" class="rental_hours_input">');
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-product="' + productData.product_code + '">');
        newRow.append('<td class="product_id_placeholder">' + productData.product_id + '</td>');
        newRow.append('<td class="product_code_placeholder">' + productData.product_code + '</td>');
        newRow.append('<td class="description_placeholder">' + productData.description + '</td>');
        newRow.append('<td class="type_placeholder">' + productData.type + '</td>');
        newRow.append('<td class="add_description_placeholder">' + productData.add_description + '</td>');
        newRow.append('<td class="quantity_placeholder"><input type="number" name="quantity[]" class="quantity_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="unit_price_placeholder"><input type="text" name="unit_price[]" class="unit_price_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="price_placeholder"></td>');
        newRow.append('<td class="extra_hours_placeholder"><input type="text" name="extra_hours[]" class="extra_hours_input"></td>');
        newRow.append('<td class="rental_hours_placeholder"><input type="text" name="rental_hours[]" class="rental_hours_input"></td>');
        // adicionando botão excluir
        var deleteButton = $('<button onclick="removeProduct(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
}

function calculatePrice(row) {
    var periodDays = parseInt($('#period_days').val()) || 0;
    var quantity = parseInt($(row).find('.quantity_input').val()) || 0;
    var unitPrice = parseFloat($(row).find('.unit_price_input').val()) || 0;
    var total = ((quantity * unitPrice) * periodDays);
    return total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function updatePrice(input) {
    var row = $(input).closest('tr');
    var totalPrice = calculatePrice(row);
    row.find('.price_placeholder').text(totalPrice);
    updateTotalValue();
    updatePricesForAllProducts();
}

function populateProductData() { //funcao para apresentar os produtos no formulario
    var productCodeInput = $('#product_code');

    var inputValue = productCodeInput.val();

    if (inputValue) {
        $.ajax({
            type: 'POST',
            url: '/get_product_data',
            data: { product_code: inputValue },
            success: function (data) {
                console.log('Received product data:', data);
                if (data && data.success) {
                    var productData = data.product_data;

                    $('#product_id').val(productData.product_id);
                    $('#product_code').val(productData.product_code);
                    $('#description').val(productData.description);
                    $('#type').val(productData.type);
                    $('#add_description').val(productData.add_description);
                    $('#quantity').val(productData.qauntity);
                    $('#unit_price').val(productData.unit_price);
                    $('#price').val(productData.price);
                    $('#extra_hours').val(productData.extra_hours);
                    $('#rental_hours').val(productData.rental_hours);

                    console.log('Product Id:', productData.product_id);
                    console.log('Product Code:', productData.product_code);
                    console.log('Description:', productData.description);
                    console.log('Type:', productData.type);
                    console.log('Add Description:', productData.add_description);
                    console.log('Quantity:', $('.quantity_input').val());
                    console.log('Unit_price:', $('.unit_price_input').val());
                    console.log('Price:', calculatePrice());
                    console.log('Extra_hours:', $('.extra_hours_input').val());
                    console.log('Rental_hours:', $('.rental_hours_input').val());

                    updateTable(productData);
                    updateTotalValue();
                    updatePricesForAllProducts();
                    productCodeInput.val('');
                } else {
                    console.error('Error fetching product data:', data.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error fetching product data:', error),
                console.error('AJAX Request Error:', status, error);
            }
        });
    }
}

function updatePeriodDays() {
    var startDateInput = document.getElementById('start_date');
    var endDateInput = document.getElementById('end_date');
    var periodDaysInput = document.getElementById('period_days');

    if (startDateInput.value && endDateInput.value) {
        var startDateParts = startDateInput.value.split('/');
        var endDateParts = endDateInput.value.split('/');

        var startDate = new Date(
            parseInt(startDateParts[2]),
            parseInt(startDateParts[1]) - 1,
            parseInt(startDateParts[0])
        );

        var endDate = new Date(
            parseInt(endDateParts[2]),
            parseInt(endDateParts[1]) -1,
            parseInt(endDateParts[0])
        );

        var timeDifference = Math.abs(endDate.getTime() - startDate.getTime());
        var periodDays = Math.ceil(timeDifference / (1000 * 3600 * 24));

        periodDaysInput.value = periodDays;
    } else {
        periodDaysInput.value = '';
    }
    console.log(periodDays);

    updatePricesForAllProducts()
}

function updateTotalValue() {
    var totalValueProducts = 0;
    $('#product_table_body tr').each(function() {
        var priceText = $(this).find('.price_placeholder').text().replace('R$', '').replace(/\./g, '').replace(',', '.');
        var price = parseFloat(priceText);
        if (!isNaN(price)) {
            totalValueProducts += price;
        }
    });

    var totalValueServices = 0;
    $('#service_table_body tr').each(function() {
        var servicePriceText = $(this).find('.service_price_placeholder').text().replace('R$', '').replace(/\./g, '').replace(',', '.');
        var totalPrice = parseFloat(servicePriceText);
        totalValueServices += isNaN(totalPrice) ? 0 : totalPrice;
    });

    var totalValue = totalValueProducts + totalValueServices;
    $('#value').val(totalValue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}

function removeProduct(row) {
    $(row).remove();
    updateTotalValue();
}

function updatePricesForAllProducts() {
    $('#product_table_body tr').each(function() {
        var row = $(this);
        var totalPrice = calculatePrice(row);
        row.find('.price_placeholder').text(totalPrice);
    });
    updateTotalValue();
}

// funcoes tabela ressarcimentos
function populateServiceData() {
    var codInput = $('#cod');
    var inputValue = codInput.val();

    if (inputValue) {
        $.ajax({
            type: 'POST',
            url: '/get_service_data',
            data: { cod: inputValue },
            success: function(data) {
                console.log('Received service data:', data);
                if (data && data.success) {
                    var serviceData = data.service_data;

                    $('#refund_id').val(serviceData.refund_id);
                    $('#cod').val(serviceData.cod);
                    $('#descript').val(serviceData.descript);
                    $('#service_quantity').val(serviceData.service_quantity);
                    $('#service_unit_price').val(serviceData.service_unit_price);
                    $('#service_price').val(serviceData.service_price);

                    console.log('Refund ID:', serviceData.refund_id);
                    console.log('Cod:', serviceData.cod);
                    console.log('Description:', serviceData.descript);
                    console.log('Service Quantity:', $('.service_quantity_input').val());
                    console.log('Service Unit price:', $('.service_unit_price_input').val());
                    console.log('Service price:', $('.service_price_input').val());

                    updateTableService(serviceData);
                    updateTotalValue();
                    updatePricesForAllServices();
                    codInput.val('');
                } else {
                    console.error('Error fetching service data:', data.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error fetching service data:', error),
                console.error('AJAX Request Error:', status, error);
            }
        });
    }
}

function updateTableService(serviceData) {
    // bloco com condicao para nao ser adicionada uma linha vazia
    if (!serviceData || Object.keys(serviceData).length === 0 || !serviceData.cod) {
        console.log('Dados do serviço inválidos ou faltando... Não adicionando à tabela.');
        return;
    }

    var tableBody = $('#service_table_body');
    var existingRow = tableBody.find('tr[data-service="' + serviceData.cod + '"]');
        // atualizando uma nova linha
    if (existingRow.length > 0) {
        existingRow.find('cod_placeholder').text(serviceData.cod || '');
        existingRow.find('descript_placeholder').text(serviceData.descript || '');
        existingRow.find('service_quantity_placeholder').html('<input type="number" name="service_quantity[]" class="service_quantity_input">');
        existingRow.find('service_unit_price_placeholder').html('<input type="text" name="service_unit_price[]" class="service_unit_price_input" onchange="updateServicePrice(this)">');
        existingRow.find('service_price_placeholder').text(calculateServicePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-service="' + serviceData.cod + '">');
        newRow.append('<td class="cod_placeholder">' + serviceData.cod + '</td>');
        newRow.append('<td class="descript_placeholder">' + serviceData.descript + '</td>');
        newRow.append('<td class="service_quantity_placeholder"><input type="number" name="service_quantity[]" class="service_quantity_input"></td>');
        newRow.append('<td class="service_unit_price_placeholder"><input type="text" name="service_unit_price[]" class="service_unit_price_input" onchange="updateServicePrice(this)"></td>');
        newRow.append('<td class="service_price_placeholder"></td>');
        // adicionando botao excluir
        var deleteButton = $('<button onclick="removeService(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
    updateTotalValue();
}

function calculateServicePrice(row) {
    var serviceQuantity = parseInt($(row).find('.service_quantity_input').val()) || 0;
    var serviceUnitPrice = parseFloat($(row).find('.service_unit_price_input').val()) || 0;
    return (serviceQuantity * serviceUnitPrice); //.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function updateServicePrice(input) {
    var row = $(input).closest('tr');
    var priceCell = row.find('.service_price_placeholder');
    var totalPrice = calculateServicePrice(row);
    priceCell.text(totalPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    updateTotalValue();
    updatePricesForAllServices();
}

function removeService(row) {
    $(row).remove();
    updateTotalValue();
    updatePricesForAllServices();
}

function updatePricesForAllServices() {
    $('#service_table_body tr').each(function() {
        var row = $(this);
        var totalPrice = calculateServicePrice(row);
        row.find('.service_price_placeholder').text(totalPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    });
    updateTotalValue();
}

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('proposal-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        submitProposal();
    });
});

function submitProposal() {
    var proposalData = {
        proposal_id: $('#proposal_id').val(),
        client_id: $('#client_id').val(),
        company: $('#company').val(),
        cpf_cnpj: $('#cpf_cnpj').val(),
        contact_name: $('#contact_name').val(),
        phone: $('#phone').val(),
        email: $('#email').val(),
        number_store: $('#number_store').val(),
        status: $('#status').val(),
        delivery_date: $('#delivery_date').val(),
        withdrawal_date: $('#withdrawal_date').val(),
        start_date: $('#start_date').val(),
        end_date: $('#end_date').val(),
        period_days: $('#period_days').val(),
        payment_condition: $('#payment_condition').val(),
        delivery_address: $('#delivery_address').val(),
        validity: $('#validity').val(),
        observations: $('#observations').val(),
        oenf_obs: $('#oenf_obs').val(),
        value: $('#value').val(),
    };

    proposalData.products = collectProducts();

    proposalData.services = collectServices();

    console.log('Proposal Data:', proposalData);
    $.ajax({
        url: '/submit_proposal',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(proposalData),
        success: function(response) {
            console.log('Proposta enviada com sucesso:', response);
        },
        error: function(error) {
            console.error('Erro ao enviar proposta:', error);
        }
    });
}

function collectProducts() {
    var products = [];
    $('#product_table_body tr' || '').each(function() {
        var product = {
            product_id: $(this).find('.product_id_placeholder').text(),
            product_code: $(this).find('.product_code_placeholder').text(),
            description: $(this).find('.description_placeholder').text(),
            type: $(this).find('.type_placeholder').text(),
            quantity: $(this).find('.quantity_input').val(),
            unit_price: $(this).find('.unit_price_input').val(),
            price: $(this).find('.price_placeholder').text(),
            add_description: $(this).find('.add_description_placeholder').text(),
            extra_hours: $(this).find('.extra_hours_input').val(),
            rental_hours: $(this).find('.rental_hours_input').val()
        };
        products.push(product);
    });
    return products;
    console.log('Products:', products);
}

function collectServices() {
    var services = [];
    $('#service_table_body tr').each(function() {
        var service = {
            cod: $(this).find('.cod_placeholder').text(),
            descript: $(this).find('.descript_placeholder').text(),
            service_quantity: $(this).find('.service_quantity_input').val(),
            service_unit_price: $(this).find('.service_unit_price_input').val(),
            service_price: $(this).find('.service_price_placeholder').text()
        };
        services.push(service);
    });
    return services;
}

document.addEventListener('DOMContentLoaded', function() {
    $('#product_table_body tr').each(function() {
        var isRowEmpty = !$.trim($(this).find('.product_code_placeholder').text());
        if (isRowEmpty) {
            $(this).remove();
        }
    });

    $('#service_table_body tr').each(function() {
        var isRowEmpty = !$.trim($(this).find('.cod_placeholder').text());
        if (isRowEmpty) {
            $(this).remove();
        }
    });
})

document.getElementById('proposal-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    fetch('/proposta', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/lista_propostas';
        } else {
            alert('Erro ao cadastrar proposta.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});
