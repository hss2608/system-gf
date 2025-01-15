document.addEventListener('DOMContentLoaded', function() {
    updateTotalValue();
});

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
                    $('#quantity').val(productData.quantity);
                    $('#unit_price').val(productData.unit_price);
                    $('#price').val(productData.price);
                    $('#extra_hours').val(productData.extra_hours);
                    $('#rental_hours').val(productData.rental_hours);

                    console.log('Product Id:', productData.product_id);
                    console.log('Product Code:', productData.product_code);
                    console.log('Description:', productData.description);
                    console.log('Quantity:', $('.quantity_input').val());
                    console.log('Unit_price:', $('.unit_price_input').val());
                    console.log('Price:', calculatePrice());
                    console.log('Extra_hours:', $('.extra_hours_input').val());
                    console.log('Rental_hours:', $('.rental_hours_input').val());

                    updateTable(productData);
                    updateTotalValue();
                    //updatePricesForAllProducts();
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
        existingRow.find('.product_code_placeholder').text(productData.product_code || '');
        existingRow.find('.description_placeholder').text(productData.description || '');
        existingRow.find('.quantity_placeholder').html('<input type="number" name="quantity" class="quantity_input" onchange="updatePrice(this)">');
        existingRow.find('.unit_price_placeholder').html('<input type="text" name="unit_price" class="unit_price_input" onchange="updatePrice(this)">');
        existingRow.find('.price_placeholder').text(calculatePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        existingRow.find('.extra_hours_placeholder').html('<input type="text" name="extra_hours" class="extra_hours_input">');
        existingRow.find('.rental_hours_placeholder').html('<input type="text" name="rental_hours]" class="rental_hours_input">');
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-product="' + productData.product_code + '">');
        newRow.append('<td class="product_id_placeholder">' + productData.product_id + '</td>');
        newRow.append('<td class="product_code_placeholder">' + productData.product_code + '</td>');
        newRow.append('<td class="description_placeholder">' + productData.description + '</td>');
        newRow.append('<td class="quantity_placeholder"><input type="number" name="quantity" class="quantity_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="unit_price_placeholder"><input type="text" name="unit_price" class="unit_price_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="price_placeholder">' + calculatePrice(newRow).toLocaleString('pt-BR', { style:'currency', currency: 'BRL' }) + '</td>');
        newRow.append('<td class="extra_hours_placeholder"><input type="text" name="extra_hours" class="extra_hours_input"></td>');
        newRow.append('<td class="rental_hours_placeholder"><input type="text" name="rental_hours" class="rental_hours_input"></td>');
        // adicionando botão excluir
        var deleteButton = $('<button class="codigos_excluir" onclick="removeProduct(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
    updateTotalValue()
    // updatePricesForAllProducts();
}

function removeProduct(row) {
    $(row).remove();
    updateTotalValue();
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
    //updatePricesForAllProducts();
}


function updatePricesForAllProducts() {
    $('#product_table_body tr').each(function() {
        var row = $(this);
        var totalPrice = calculatePrice(row);
        row.find('.price_placeholder').text(totalPrice);
    });
    updateTotalValue();
}

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
                    // updatePricesForAllServices();
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
        var deleteButton = $('<button class="codigos_excluir" onclick="removeService(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
    updateTotalValue();
}

function removeService(row) {
    $(row).remove();
    updateTotalValue();
    // updatePricesForAllServices();
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
    // updatePricesForAllServices();
}

function updatePricesForAllServices() {
    $('#service_table_body tr').each(function() {
        var row = $(this);
        var totalPrice = calculateServicePrice(row);
        row.find('.service_price_placeholder').text(totalPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
    });
    updateTotalValue();
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

// impede que seja criada uma linha vazia nas respectivas tabelas
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

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('edit_proposal_form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        submitProposal();
    });
});

function submitProposal() {
    var proposalData = {
        proposal_id: $('#proposal_id').val().split('/')[0].substring(0, 5),
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
        delivery_address: $('#delivery_address').val(),
        delivery_bairro: $('#delivery_bairro').val(),
        delivery_municipio: $('#delivery_municipio').val(),
        delivery_uf: $('#delivery_uf').val(),
        delivery_cep: $('#delivery_cep').val(),
        observations: $('#observations').val(),
        oenf_obs: $('#oenf_obs').val(),
        value: $('#value').val(),
    };

    proposalData.products = collectProducts();

    proposalData.services = collectServices();

    console.log('Proposal Data:', proposalData);
    $.ajax({
        url: '/submit_edit_proposal',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(proposalData),
        success: function(response) {
            console.log('Proposta enviada com sucesso:', response);
            if (response.success) {
                if (response.tarefas && response.tarefas.length > 0) {
                    alert('Proposta aprovada e atualizada com sucesso!');
                    response.tarefas.forEach(function(tarefa) {
                        console.log('Tarefa:',  tarefa.message);
                    });
                }
            } else {
                alert('Erro ao atualizar a proposta: ' + response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('Erro ao enviar proposta:', error);
            alert('Erro ao enviar a proposta.');
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
            quantity: $(this).find('.quantity_input').length ? $(this).find('.quantity_input').val() : $(this).find('.quantity_placeholder').text(),
            unit_price: $(this).find('.unit_price_input').length ? $(this).find('.unit_price_input').val() : $(this).find('.unit_price_placeholder').text(),
            price: $(this).find('.price_placeholder').text(),
            extra_hours: $(this).find('.extra_hours_input').length ? $(this).find('.extra_hours_input').val() : $(this).find('.extra_hours_placeholder').text(),
            rental_hours: $(this).find('.rental_hours_input').length ? $(this).find('.rental_hours_input').val() : $(this).find('.rental_hours_placeholder').text()
        };
        products.push(product);
    });
    console.log('Products:', products);
    return products;
}

function collectServices() {
    var services = [];
    $('#service_table_body tr').each(function() {
        var service = {
            cod: $(this).find('.cod_placeholder').text(),
            descript: $(this).find('.descript_placeholder').text(),
            service_quantity: $(this).find('.service_quantity_input').length ? $(this).find('.service_quantity_input').val() : $(this).find('.service_quantity_placeholder').text(),
            service_unit_price: $(this).find('.service_unit_price_input').length ? $(this).find('.service_unit_price_input').val() : $(this).find('.service_unit_price_placeholder').text(),
            service_price: $(this).find('.service_price_placeholder').text()
        };
        services.push(service);
    });
    return services;
}
