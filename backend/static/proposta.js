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
                if (data && data.success) {
                    var clientData = data.client_data;
                    $('#company').val(clientData.company || '');
                    $('#contact_name').val(clientData.contact_name || '');
                    $('#phone').val(clientData.phone || '');
                    $('#email').val(clientData.email || '');
                    $('#number_store').val(clientData.number_store || '');
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


function updateTable(productData) {
    var tableBody = $('#product_table_body');
    var existingRow = tableBody.find('tr[data-product="' + productData.product_code + '"]');
        // atualizando uma nova linha
    if (existingRow.length > 0) {
        existingRow.find('.description_placeholder').text(productData.description || '');
        existingRow.find('.type_placeholder').text(productData.type || '');
        existingRow.find('.add_description_placeholder').text(productData.add_description || '');
        existingRow.find('.unit_price_placeholder').html('<input type="text" name="unit_price" class="unit_price_input" onchange="updatePrice(this)">');
        existingRow.find('.price_placeholder').text(calculatePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-product="' + productData.product_code + '">');
        newRow.append('<td class="product_code_placeholder">' + productData.product_code + '</td>');
        newRow.append('<td class="description_placeholder">' + productData.description + '</td>');
        newRow.append('<td class="type_placeholder">' + productData.type + '</td>');
        newRow.append('<td class="add_description_placeholder">' + productData.add_description + '</td>');
        newRow.append('<td class="unit_price_placeholder"><input type="text" name="unit_price" class="unit_price_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="price_placeholder">' + calculatePrice(newRow).toLocaleString('pt-BR', { style:'currency', currency: 'BRL' }) + '</td>');
        // adicionando botão excluir
        var deleteButton = $('<button onclick="removeProduct(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
}

function calculatePrice(row) {
    var periodDays = parseInt($('#period_days').val()) || 0;
    var unitPrice = parseFloat($('.unit_price_input').val()) || 0;
    return (unitPrice * periodDays).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function updatePrice(input) {
    var row = $(input).closest('tr');
    var priceCell = row.find('.price_placeholder');
    priceCell.text(calculatePrice());
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

                    console.log('Product Code:', productData.product_code);
                    console.log('Description:', productData.description);
                    console.log('Type:', productData.type);
                    console.log('Add Description:', productData.add_description);
                    console.log('unit_price:', $('.unit_price_input').val());
                    console.log('price:', calculatePrice());

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
        var price = parseFloat($(this).find('.price_placeholder').text().replace('R$', '').replace(',', '.'));
        if (!isNaN(price)) {
            totalValueProducts += price;
        }
    });

    var totalValueServices = 0;
    $('#service_table_body tr').each(function() {
        var serviceDays = parseInt($(this).find('.service_days_input').val()) || 0;
        var serviceUnitPrice = parseFloat($(this).find('.service_unit_price_input').val()) || 0;
        var totalPrice = (serviceDays * serviceUnitPrice);
        $(this).find('.service_price_placeholder').text(totalPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        totalValueServices += totalPrice;
    });

    var totalValue = totalValueProducts + totalValueServices;
    $('#value').val(totalValue.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
}

function removeProduct(row) {
    $(row).remove();
    updateTotalValue();
}

function updatePricesForAllProducts() {
    var periodDays = parseInt($('#period_days').val()) || 0;
    $('#product_table_body tr').each(function() {
        var row = $(this);
        var unitPrice = parseFloat(row.find('.unit_price_input').val()) || 0;
        var totalPrice = (unitPrice * periodDays).toFixed(2);
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

                    console.log('Cod:', serviceData.cod);
                    console.log('Description:', serviceData.descript);

                    updateTableService(serviceData);
                    updateTotalValue();
                    updatePricesForAllServices();
                    codInput.val('');
                } else {
                    console.error('Error fetching service data:', data.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error fetching product data:', error),
                console.error('AJAX Request Error:', status, error);
            }
        });
    }
}

function updateTableService(serviceData) {
    var tableBody = $('#service_table_body');
    var existingRow = tableBody.find('tr[data-service="' + serviceData.cod + '"]');
        // atualizando uma nova linha
    if (existingRow.length > 0) {
        existingRow.find('cod_placeholder').text(serviceData.cod || '');
        existingRow.find('descript_placeholder').text(serviceData.descript || '');
        existingRow.find('service_days_placeholder').html('<input type="number" name="service_days" class="service_days_input">');
        existingRow.find('service_unit_price_placeholder').html('<input type="text" name="service_unit_price" class="service_unit_price_input" onchange="updateServicePrice(this)">');
        existingRow.find('service_price_placeholder').text(calculateServicePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-service="' + serviceData.cod + '">');
        newRow.append('<td class="cod_placeholder">' + serviceData.cod + '</td>');
        newRow.append('<td class="descript_placeholder">' + serviceData.descript + '</td>');
        newRow.append('<td class="service_days_placeholder"><input type="number" name="service_days" class="service_days_input"></td>');
        newRow.append('<td class="service_unit_price_placeholder"><input type="text" name="service_unit_price" class="service_unit_price_input" onchange="updateServicePrice(this)"></td>');
        newRow.append('<td class="service_price_placeholder"></td>');
        // adicionando botao excluir
        var deleteButton = $('<button onclick="removeService(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
    updateTotalValue();
}

function calculateServicePrice(row) {
    var serviceDays = parseInt($(row).find('.service_days_input').val()) || 0;
    var serviceUnitPrice = parseFloat($(row).find('.service_unit_price_input').val()) || 0;
    return (serviceDays * serviceUnitPrice); //.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
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

        submitProposalForm();
    });
});

function submitProposalForm() {
    const formData = new FormData(document.getElementById('proposal-form'));

    fetch('/proposta', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.success) {
            window.location.href = '/success';
        } else {
            alert('Failed to submit proposal form. Please try again.');
        }
    })

    .catch(error => {
        console.error(error);
        alert('An error occured while submitting the proposal form. Please try again later.');
    });
}
