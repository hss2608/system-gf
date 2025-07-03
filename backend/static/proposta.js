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
        existingRow.find('.volts_placeholder').html('<input type="text" name="volts[]" class="volts_input" onchange="handleVoltsChange(this)">');
        existingRow.find('.rental_hours_placeholder').html('<input type="text" name="rental_hours[]" class="rental_hours_input">');
        existingRow.find('.unit_price_placeholder').html('<input type="text" name="unit_price[]" class="unit_price_input" onchange="updatePrice(this)">');
        existingRow.find('.discount_placeholder').html('<input type="text" name="discount[]" class="discount_input">');
        existingRow.find('.price_placeholder').text(calculatePrice(existingRow).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
        existingRow.find('.extra_hours_placeholder').html('<input type="text" name="extra_hours[]" class="extra_hours_input">');
        // adicionando uma nova linha
    } else {
        var newRow = $('<tr data-product="' + productData.product_code + '">');
        newRow.append('<td class="product_id_placeholder">' + productData.product_id + '</td>');
        newRow.append('<td class="product_code_placeholder">' + productData.product_code + '</td>');
        newRow.append('<td class="description_placeholder">' + productData.description + '</td>');
        newRow.append('<td class="type_placeholder">' + productData.type + '</td>');
        newRow.append('<td class="add_description_placeholder">' + productData.add_description + '</td>');
        newRow.append('<td class="quantity_placeholder"><input type="number" name="quantity[]" class="quantity_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="volts_placeholder"><input type="text" name="volts[]" class="volts_input" onchange="handleVoltsChange(this)"></td>');
        newRow.append('<td class="rental_hours_placeholder"><input type="text" name="rental_hours[]" class="rental_hours_input" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="unit_price_placeholder"><input type="text" name="unit_price[]" class="unit_price_input" value="' + (productData.unit_price || '') + '" onchange="updatePrice(this)"></td>');
        newRow.append('<td class="discount_placeholder"><input type="text" name="discount[]" class="discount_input" value="0%" onfocus="formatDiscountOnFocus(this)" onblur="formatDiscountOnBlur(this)"></td>');
        newRow.append('<td class="price_placeholder"></td>');
        newRow.append('<td class="extra_hours_placeholder"><input type="text" name="extra_hours[]" class="extra_hours_input" value="' + (productData.extra_hours || '') + '"></td>');

        // adicionando botão excluir
        var deleteButton = $('<button class="codigos_excluir" onclick="removeProduct(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
}

function getFixedUnitPrice(kva) {
    if (kva === 0) return "";
    if (kva <= 25) return 91;
    if (kva <= 30) return 101;
    if (kva <= 40) return 101;
    if (kva <= 50) return 110;
    if (kva <= 70) return 136;
    if (kva <= 90) return 154;
    if (kva <= 120) return 154;
    if (kva <= 150) return 193;
    if (kva <= 165) return 215;
    if (kva <= 190) return 271;
    if (kva <= 210) return 312;
    if (kva <= 260) return 312;
    if (kva <= 310) return 343;
    if (kva <= 330) return 369;
    if (kva <= 380) return 388;
    if (kva <= 405) return 477;
    if (kva <= 450) return 504;
    if (kva <= 500) return 535;
    if (kva <= 600) return 742;
    if (kva == 10006) return 115;
    if (kva == 20030) return 138;
}

function extractKvaFromProductCode(code) {
    let kvaStr;

    if (code.startsWith('081')) {
        kvaStr = code.substring(3, 7); // Geradores
    } else {
        kvaStr = code.substring(2, 7); // Torres de iluminação
    }

    return parseInt(kvaStr, 10);
}


function calcularExtraHours(kva, unitPrice) {
    if (kva === 0 || kva >= 601) return "";

    const bruto = unitPrice / 8;
    const arredondado = Math.round(bruto * 100) / 100;

    return arredondado.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatDiscountOnFocus(input) {
    input.value = input.value.replace('%', '').replace(',', '.').trim();
}

function formatDiscountOnBlur(input) {
    let rawValue = parseFloat(input.value.replace('%', '').replace(',', '.').trim());
    if (isNaN(rawValue) || rawValue < 0) rawValue = 0;
    if (rawValue > 100) rawValue = 100;

    input.value = rawValue.toLocaleString('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }) + '%';

    const row = $(input).closest('tr');
    const totalPrice = calculatePrice(row);
    row.find('.price_placeholder').text(totalPrice.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }));
}

function calculatePrice(row) {
    const quantity = parseFloat($(row).find('.quantity_input').val()) || 0;
    const periodDays = parseFloat($('#period_days').val()) || 0;
    const rentalHours = parseFloat($(row).find('.rental_hours_input').val()) || 0;

    // Detecta se é torre de iluminação
    const productCode = $(row).find('.product_code_placeholder').text();
    const kva = extractKvaFromProductCode(productCode);
    const isTorreIluminacao = (kva === 10006 || kva === 20030);

    // Desconto
    let discountText = $(row).find('.discount_input').val() || "0";
    let desconto = parseFloat(
        discountText.replace('%', '').replace(',', '.')
    ) || 0;

    let precoBase = 0;

    if (isTorreIluminacao) {
        // Para torres: usa o unit_price direto
        let unitPriceText = $(row).find('.unit_price_input').val() || "0";
        let unitPrice = parseFloat(
            unitPriceText.replace('R$', '').replace(/\./g, '').replace(',', '.')
        ) || 0;

        precoBase = quantity * periodDays * unitPrice;
    } else {
        // Para geradores: usa valor por hora (extra_hours)
        let extraHoursText = $(row).find('.extra_hours_input').val() || "0";
        let valorPorHora = parseFloat(
            extraHoursText.replace('R$', '').replace(/\./g, '').replace(',', '.')
        ) || 0;

        precoBase = quantity * periodDays * rentalHours * valorPorHora;
    }

    // Aplicar desconto
    let precoFinal = desconto > 0 ? precoBase - (precoBase * (desconto / 100)) : precoBase;

    return precoFinal;
}


function updatePrice(input) {
    var row = $(input).closest('tr');
    var totalPrice = calculatePrice(row);
    row.find('.price_placeholder').text(totalPrice.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }));
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
                    $('#quantity').val(productData.quantity);
                    $('#volts').val(productData.volts);
                    $('#rental_hours').val(productData.rental_hours);
                    $('#unit_price').val(productData.unit_price);
                    $('#price').val(productData.price);
                    $('#extra_hours').val(productData.extra_hours);

                    console.log('Product Id:', productData.product_id);
                    console.log('Product Code:', productData.product_code);
                    console.log('Description:', productData.description);
                    console.log('Type:', productData.type);
                    console.log('Add Description:', productData.add_description);
                    console.log('Quantity:', $('.quantity_input').val());
                    console.log('Volts:', $('.volts_input').val());
                    console.log('Rental_hours:', $('.rental_hours_input').val());
                    console.log('Unit_price:', $('.unit_price_input').val());
                    console.log('Price:', calculatePrice());
                    console.log('Extra_hours:', $('.extra_hours_input').val());

                    const kva = extractKvaFromProductCode(productData.product_code);
                    const fixedPrice = getFixedUnitPrice(kva);
                    console.log("KVA extraído:", kva);
                    console.log("Preço fixo definido:", fixedPrice);

                    if (typeof fixedPrice === 'number') {
                        productData.unit_price = fixedPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
                        console.log("Preço formatado:", productData.unit_price);
                    } else {
                        alert(fixedPrice);
                        productData.unit_price = "R$ 0,00";
                    }

                    const numericPrice = typeof fixedPrice === 'number' ? fixedPrice : 0;

                    const extraHours = calcularExtraHours(kva, numericPrice);
                    productData.extra_hours = extraHours;
                    console.log("Hora Extra: ", extraHours);

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
        var priceText = $(this).find('.price_placeholder').text();
        var sanitized = priceText.replace(/\s/g, '').replace('R$', '').replace(/\./g, '').replace(',', '.');
        var price = parseFloat(sanitized);
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

    var totalValueAccessories = 0;
    $('#accessories_table_body tr').each(function () {
        var accPriceText = $(this).find('.accessories_price_placeholder').text().replace('R$', '').replace(/\./g, '').replace(',', '.');
        var totalAccessory = parseFloat(accPriceText);
        totalValueAccessories += isNaN(totalAccessory) ? 0 : totalAccessory;
    });

    var totalValue = totalValueProducts + totalValueServices + totalValueAccessories;
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
        row.find('.price_placeholder').text(totalPrice.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }));
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
                    $('#discount').val(serviceData.discount);
                    $('#km').val(serviceData.km);
                    $('#service_price').val(serviceData.service_price);

                    console.log('Refund ID:', serviceData.refund_id);
                    console.log('Cod:', serviceData.cod);
                    console.log('Description:', serviceData.descript);
                    console.log('Service Quantity:', $('.service_quantity_input').val());
                    console.log('Service Unit price:', $('.service_unit_price_input').val());
                    console.log('Discount:', $('.discount_input').val());
                    console.log('KM:', $('.km_input').val());
                    console.log('Service price:', $('.service_price_input').val());

                    const refundCod = parseInt(serviceData.cod);
                    const fixedServicePrice = getFixedServiceUnitPrice(refundCod);

                    if (typeof fixedServicePrice === 'number') {
                        serviceData.service_unit_price = fixedServicePrice.toLocaleString('pt-BR', {
                            style: 'currency',
                            currency: 'BRL'
                        });
                    } else {
                        serviceData.service_unit_price = "R$ 0,00";
                    }

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
        newRow.append('<td class="service_quantity_placeholder"><input type="number" name="service_quantity[]" class="service_quantity_input" value="' + (serviceData.service_quantity || 0) + '"></td>');
        newRow.append('<td class="service_unit_price_placeholder"><input type="text" name="service_unit_price[]" class="service_unit_price_input" value="' + (serviceData.service_unit_price || 'R$ 0,00') + '" onchange="updateServicePrice(this)"></td>');
        newRow.append('<td class="discount_service_placeholder"><input type="text" name="discount[]" class="discount_service_input" value="' + (serviceData.discount || '0%') + '" onfocus="formatDiscountOnFocus(this)" onblur="formatDiscountServiceOnBlur(this)"></td>');
        newRow.append('<td class="km_placeholder"><input type="number" name="km[]" class="km_input" value="' + (serviceData.km || 0) + '" onchange="updateServicePrice(this)"></td>');
        newRow.append('<td class="service_price_placeholder"></td>');
        // adicionando botao excluir
        var deleteButton = $('<button class="codigos_excluir" onclick="removeService(this.parentNode.parentNode)">Excluir</button>');
        newRow.append($('<td>').append(deleteButton));

        tableBody.append(newRow);
    }
    updateTotalValue();
}

function getFixedServiceUnitPrice(refund) {
    if (refund === 0) return "";
    if (refund == 1) return 9.2;
    if (refund >= 2) return 0;
}

function formatDiscountServiceOnBlur(input) {
    let rawValue = parseFloat(input.value.replace('%', '').replace(',', '.').trim());
    if (isNaN(rawValue) || rawValue < 0) rawValue = 0;
    if (rawValue > 100) rawValue = 100;

    input.value = rawValue.toLocaleString('pt-BR', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }) + '%';

    const row = $(input).closest('tr');
    const totalPrice = calculateServicePrice(row);
    row.find('.service_price_placeholder').text(totalPrice.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }));
}

function calculateServicePrice(row) {
    const serviceQuantity = parseInt($(row).find('.service_quantity_input').val()) || 0;

    let unitPriceText = $(row).find('.service_unit_price_input').val() || "0";
    let serviceUnitPrice = parseFloat(unitPriceText.replace('R$', '').replace(/\./g, '').replace(',', '.')) || 0;

    const km = parseFloat($(row).find('.km_input').val()) || 0;

    let discountText = $(row).find('.discount_service_input').val() || "0";
    let discount = parseFloat(discountText.replace('%', '').replace(',', '.')) || 0;

    let cod = parseInt($(row).find('.cod_placeholder').text());

    let basePrice = 0;

    if (cod === 1) {
        if (km === 0) return 0;

        if (km < 31) {
            // Fórmula alternativa para até 30 km
            const fator1 = 92.6925;
            const fator2 = 4.639;
            basePrice = fator1 * fator2 * serviceQuantity * 2;
        } else {
            // Fórmula padrão para 31 km ou mais
            basePrice = serviceQuantity * serviceUnitPrice * km * 2;
        }
    } else {
        basePrice = serviceQuantity * serviceUnitPrice;
    }
    console.log("Base Price: ", basePrice);

    let finalPrice = discount > 0 ? basePrice - (basePrice * (discount / 100)) : basePrice;

    return finalPrice;
}

function updateServicePrice(input) {
    const row = $(input).closest('tr');
    const price = calculateServicePrice(row);
    row.find('.service_price_placeholder').text(price.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }));
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

function getAccessoryDescription(kva, volts) {
    if (!kva || !volts) return "";

    if (kva <= 25 && volts == 440) return "CABO 16 mm² pp";
    if (kva <= 50 && volts == 220) return "CABO 25 mm² pp";
    if (kva <= 50 && volts == 440) return "CABO 16 mm² pp";
    if (kva <= 80 && volts == 220) return "CABO 70 mm²";
    if (kva <= 80 && volts == 380) return "CABO 25 mm² pp";
    if (kva <= 80 && volts == 440) return "CABO 16 mm² pp";
    if (kva <= 110 && volts == 220) return "CABO 95 mm²";
    if (kva <= 110 && volts == 380) return "CABO 50 mm²";
    if (kva <= 110 && volts == 440) return "CABO 25 mm² pp";
    if (
        kva <= 165 || kva <= 230 || kva <= 250 || kva <= 320 ||
        kva <= 405 || kva <= 450 || kva <= 500 || kva <= 600 ||
        kva <= 900 || kva <= 1000
    ) {
        return "CABO 120 mm²";
    }

    return "ACESSÓRIO PADRÃO"
}

function  handleVoltsChange(input) {
    const row = $(input).closest('tr');
    const productCode = row.find('.product_code_placeholder').text();
    const kva = extractKvaFromProductCode(productCode);
    const volts = parseInt($(input).val());
    const quantity = parseInt(row.find('.quantity_input').val()) || 0;

    if (!kva || !volts) return;

    const description = getAccessoryDescription(kva, volts);
    const quantityAccessory = getAccessoryQuantity(kva, volts);
    addAccessoryRow({
        description,
        quantity: quantity,
        quantityAccessory,
        kva,
        volts });
}

function addAccessoryRow(data) {
    const tableBody = $('#accessories_table_body');
    const newRow = $('<tr>').attr('data-quantity', data.quantity || 0);

    newRow.append('<td class="accessories_description_placeholder">' + data.description + '</td>');
    newRow.append('<td class="accessories_quantity_placeholder"><input type="text" class="accessories_quantity_input" value="' + (data.quantityAccessory || '') + '"></td>');
    newRow.append('<td class="meters_placeholder"><input type="number" class="meters_input"></td>');
    newRow.append('<td class="accessories_unit_price_placeholder"><input type="text" class="accessories_unit_price_input"></td>');
    newRow.append('<td class="accessories_days_placeholder"><input type="text" class="accessories_days_input" readonly');
    newRow.append('<td class="items_meters_placeholder"><input type="text" class="items_meters_input"></td>');
    newRow.append('<td class="accessories_discount_placeholder"><input type="text" class="accessories_discount_input" value="0%"></td>');
    newRow.append('<td class="accessories_price_placeholder"></td>');

    var deleteButton = $('<button class="codigos_excluir" onclick="removeAccessory(this.parentNode.parentNode)">Excluir</button>');
    newRow.append($('<td>').append(deleteButton));

    tableBody.append(newRow);
}

function getAccessoryQuantity(kva, volts) {
    if (!kva || !volts) return "";

    if (kva <= 25 && volts == 440) return "01 pp";
    if (kva <= 50 && volts == 220) return "01 pp";
    if (kva <= 50 && volts == 440) return "01 pp";
    if (kva <= 80 && volts == 220) return "01/fase";
    if (kva <= 80 && volts == 380) return "01 pp";
    if (kva <= 80 && volts == 440) return "01 pp";
    if (kva <= 110 && volts == 220) return "01/fase";
    if (kva <= 110 && volts == 380) return "01/fase";
    if (kva <= 110 && volts == 440) return "01 pp";
    if (kva <= 165 && volts == 220) return "01/fase";
    if (kva <= 165 && volts == 380) return "01/fase";
    if (kva <= 165 && volts == 440) return "01/fase";
    if (kva <= 230 && volts == 220) return "01/fase";
    if (kva <= 230 && volts == 380) return "01/fase";
    if (kva <= 230 && volts == 440) return "01/fase";
    if (kva <= 250 && volts == 220) return "02/fase";
    if (kva <= 250 && volts == 380) return "01/fase";
    if (kva <= 250 && volts == 440) return "01/fase";
    if (kva <= 320 && volts == 220) return "03/fase";
    if (kva <= 320 && volts == 380) return "02/fase";
    if (kva <= 320 && volts == 440) return "02/fase";
    if (kva <= 405 && volts == 220) return "04/fase";
    if (kva <= 405 && volts == 380) return "03/fase";
    if (kva <= 405 && volts == 440) return "02/fase";
    if (kva <= 450 && volts == 220) return "04/fase";
    if (kva <= 450 && volts == 380) return "02/fase";
    if (kva <= 450 && volts == 440) return "02/fase";
    if (kva <= 500 && volts == 220) return "05/fase";
    if (kva <= 500 && volts == 380) return "03/fase";
    if (kva <= 500 && volts == 440) return "02/fase";
    if (kva <= 600 && volts == 220) return "06/fase";
    if (kva <= 600 && volts == 380) return "03/fase";
    if (kva <= 600 && volts == 440) return "02/fase";
    if (kva <= 900 && volts == 220) return "08/fase";
    if (kva <= 900 && volts == 380) return "05/fase";
    if (kva <= 900 && volts == 440) return "04/fase";
    if (kva <= 1000 && volts == 220) return "10/fase";
    if (kva <= 1000 && volts == 380) return "05/fase";
    if (kva <= 1000 && volts == 440) return "04/fase";

    return "QUANTIDADE PADRÃO";
}

function getAccessoryUnitPrice(description) {
    if (!description) return 0;

    const mapa = {
        "CABO 240 mm²": 0.77,
        "CABO 185 mm²": 0.57,
        "CABO 150 mm²": 5.00,
        "CABO 120 mm²": 0.38,
        "CABO 95 mm²": 0.30,
        "CABO 70 mm²": 0.22,
        "CABO 50 mm²": 0.16,
        "CABO 35 mm² pp": 0.47,
        "CABO 25 mm² pp": 0.34,
        "CABO 16 mm² pp": 0.22
    };

    return mapa[description] || 0;
}

function parseAccessoryQuantity(quantityText) {
    if (!quantityText) return 0;

    const mapa = {
        "01 pp": 1,
        "01/fase": 1,
        "02/fase": 2,
        "03/fase": 3,
        "04/fase": 4,
        "05/fase": 5,
        "06/fase": 6,
        "08/fase": 8,
        "10/fase": 10
    };

    return mapa[quantityText] || 0;
}

function calculateItemsMeters(description, meters, quantity, quantityText) {
    if (!description || !meters || !quantity || !quantityText) return "";

    const lowBitolas = ["16 mm² pp", "25 mm² pp", "35 mm² pp"];
    const parsedQuantity = parseAccessoryQuantity(quantityText);

    const fator = lowBitolas.includes(description) ? 1 : 4;

    return parsedQuantity * meters * quantity * fator;
}

const manualAccessoriesList = [
    "Quadro QTM 250A",
    "Quadro QTM 400A",
    "Quadro QTM 600A",
    "Quadro QTM 1000A",
    "Quadro QTM 1200A",
    "Quadro QTM 1600A",
    "Quadro QTA 150A",
    "Quadro QTA 250A",
    "Quadro QTA 400A",
    "Quadro QTA 600A",
    "Quadro QTA 800A",
    "Quadro QTA 1000A",
    "Quadro QTA 1250A",
    "Quadro QTA 1600A",
    "Quadro QTA 2000A",
    "Caixa intermediaria barramento",
    "Protetor passa cabos",
    "Extintor sem carretinha",
    "Bandeja captadora de oleo pequena",
    "Bandeja captadora de oleo media",
    "Bandeja captadora de oleo grande"
];

function getFixedManualAccessoryPrice(description) {
    const mapa = {
        "Quadro QTM 250A": 18.20,
        "Quadro QTM 400A": 25.40,
        "Quadro QTM 600A": 35.10,
        "Quadro QTM 1000A": 49.60,
        "Quadro QTM 1200A": 65.20,
        "Quadro QTM 1600A": 81.00,
        "Quadro QTA 150A": 37.00,
        "Quadro QTA 250A": 52.00,
        "Quadro QTA 400A": 77.00,
        "Quadro QTA 600A": 110.00,
        "Quadro QTA 800A": 120.00,
        "Quadro QTA 1000A": 165.00,
        "Quadro QTA 1250A": 208.00,
        "Quadro QTA 1600A": 250.00,
        "Quadro QTA 2000A": 285.00,
        "Caixa intermediaria barramento": 16.00,
        "Protetor passa cabos": 8.50,
        "Extintor sem carretinha": 3.45,
        "Bandeja captadora de oleo pequena": 9.70,
        "Bandeja captadora de oleo media": 12.20,
        "Bandeja captadora de oleo grande": 18.80
    };

    return mapa[description] || 0;
}


function addManualAccessory() {
    const selected = document.getElementById('manualAccessorySelect').value;
    if (!selected) return;

    const tableBody = $('#accessories_table_body');
    const newRow = $('<tr>').attr('data-manual', 'true');

    newRow.append('<td class="accessories_description_placeholder">' + selected + '</td>');
    newRow.append('<td class="accessories_quantity_placeholder"><input type="number" class="accessories_quantity_input"></td>');
    newRow.append('<td class="meters_placeholder"></td>');
    newRow.append('<td class="accessories_unit_price_placeholder"><input type="text" class="accessories_unit_price_input" readonly></td>');
    newRow.append('<td class="accessories_days_placeholder"><input type="number" class="accessories_days_input"></td>');
    newRow.append('<td class="items_meters_placeholder"></td>');
    newRow.append('<td class="accessories_discount_placeholder"><input type="text" class="accessories_discount_input" value="0%"></td>');
    newRow.append('<td class="accessories_price_placeholder"></td>');

    const deleteBtn = $('<button class="codigos_excluir" onclick="removeAccessory(this.parentNode.parentNode)">Excluir</button>');
    newRow.append($('<td>').append(deleteBtn));

    const fixedUnitPrice = getFixedManualAccessoryPrice(selected);
    newRow.find('.accessories_unit_price_input').val(fixedUnitPrice.toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }));

    tableBody.append(newRow);
}

function calculateAccessoryPrice(row) {
    const isManual = row.attr('data-manual') === 'true';

    const unitPriceText = row.find('.accessories_unit_price_input').val() || "0";
    const unitPrice = parseFloat(unitPriceText.replace('R$', '').replace(/\./g, '').replace(',', '.')) || 0;

    const discountText = row.find('.accessories_discount_input').val() || "0";
    const discount = parseFloat(discountText.replace('%', '').replace(',', '.')) || 0;

    const days = parseFloat(row.find('.accessories_days_input').val()) || 0;

    let base = 0;

    if (isManual) {
        const quantity = parseFloat(row.find('.accessories_quantity_input').val()) || 0;
        if (!quantity || !unitPrice || !days) return 0;
        base = quantity * unitPrice * days;
    } else {
        const items = parseFloat(row.find('.items_meters_input').val()) || 0;
        if (!items || !unitPrice || !days) return 0;
        base = items * unitPrice * days;
    }

    const final = discount > 0 ? base - (base * (discount / 100)) : base;

    return Math.round(final * 100) / 100;
}

function updateAccessoryPrice(input) {
    const row = $(input).closest('tr');
    const price = calculateAccessoryPrice(row);

    row.find('.accessories_price_placeholder').text(price.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }));

    updateTotalValue();
}

function removeAccessory(row) {
    $(row).remove();
    updateTotalValue();
}


document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('proposal-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        submitProposal();
    });

    $(document).on('input', '.quantity_input, .rental_hours_input, .unit_price_input, .extra_hours_input, .discount_input', function () {
        updatePrice(this);
    });

    $(document).on('input', '.service_unit_price_input, .km_input, .service_quantity_input, .discount_service_input', function () {
        updateServicePrice(this);
    });

    $(document).on('input', '.meters_input', function () {
        const row = $(this).closest('tr');

        const quantityText = row.find('.accessories_quantity_input').val();
        const meters = parseFloat($(this).val()) || 0;
        const description = row.find('.accessories_description_placeholder').text().trim();
        const periodDays = parseInt($('#period_days').val()) || 0;
        const quantity = parseInt(row.attr('data-quantity')) || 0;

        if (!quantityText || !meters || !description || !quantity) return;

        const unitValue = getAccessoryUnitPrice(description);

        // Formatar e preencher o campo accessories_unit_price
        row.find('.accessories_unit_price_input').val(unitValue.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }));

        row.find('.accessories_days_input').val(periodDays);

        const itemsResult = calculateItemsMeters(description, meters, quantity, quantityText);
        row.find('.items_meters_input').val(itemsResult);

        updateAccessoryPrice(this);
    });

    $(document).on('input', '.accessories_quantity_input, .accessories_unit_price_input, .accessories_discount_input, .items_meters_input, .accessories_days_input', function () {
        updateAccessoryPrice(this);
    });

    const select = document.getElementById('manualAccessorySelect');
    manualAccessoriesList.forEach(function (item) {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        select.appendChild(option);
    });

    tinymce.init({
      selector: '#observations',
      menubar: false,
      height: 800,
      language: 'pt_BR',
      language_url: 'https://cdn.tiny.cloud/1/8wtxfoo5se51jl9zmlz4obivgwepjmxh88vtkopcqk3iuntr/tinymce/6/langs/pt_BR.js', // suporte opcional em português
      plugins: 'lists link table wordcount',
      toolbar: 'undo redo | styles | bold italic underline | forecolor backcolor | alignleft aligncenter alignright | bullist numlist outdent indent | link table | wordcount'
    });
});

function submitProposal() {

    const btn = document.querySelector('#submit-button');
    btn.disabled = true;
    btn.textContent = 'Salvando...';

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
        delivery_bairro: $('#delivery_bairro').val(),
        delivery_municipio: $('#delivery_municipio').val(),
        delivery_cep: $('#delivery_cep').val(),
        delivery_uf: $('#delivery_uf').val(),
        validity: $('#validity').val(),
        observations: tinymce.get('observations').getContent().trim(),
        oenf_obs: $('#oenf_obs').val().trim(),
        value: $('#value').val(),
    };
    proposalData.products = collectProducts();
    proposalData.services = collectServices();
    proposalData.accessories = collectAccessories();

    console.log('Proposal Data:', proposalData);
    fetch('/submit_proposal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(proposalData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Proposta salva com sucesso!");
            window.location.href = "/lista_propostas"; // redireciona após salvar
        } else {
            alert("Erro: " + data.error);
        }
    })
    .catch(error => {
        console.error('Erro ao enviar proposta:', error);
        alert("Erro interno. Tente novamente.");
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
            volts: $(this).find('.volts_input').val(),
            rental_hours: $(this).find('.rental_hours_input').val(),
            unit_price: $(this).find('.unit_price_input').val(),
            discount: $(this).find('.discount_input').val().trim(),
            price: $(this).find('.price_placeholder').text(),
            add_description: $(this).find('.add_description_placeholder').text(),
            extra_hours: $(this).find('.extra_hours_input').val(),
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
            service_unit_price: $(this).find('.service_unit_price_input').text(),
            discount: $(this).find('.discount_service_input').val().trim(),
            km: $(this).find('.km_input').val(),
            service_price: $(this).find('.service_price_placeholder').text()
        };
        services.push(service);
    });
    return services;
    console.log('Services: ', services);
}

function collectAccessories() {
    var accessories = [];

    $('#accessories_table_body tr').each(function () {
        var row = $(this);
        var isManual = row.attr('data-manual') === 'true';

        var description = row.find('.accessories_description_placeholder').text().trim();
        var quantity = row.find('.accessories_quantity_input').val()?.trim() || '';
        var unit_price = row.find('.accessories_unit_price_input').val()?.trim() || '';
        var discount = row.find('.accessories_discount_input').val()?.trim() || '';
        var days = row.find('.accessories_days_input').val()?.trim() || '';
        var price = row.find('.accessories_price_placeholder').text()?.trim() || '';

        if (isManual) {
            accessories.push({
                accessories_description: description,
                accessories_quantity: quantity,
                meters: 0,  // não se aplica
                accessories_unit_price: unit_price,
                accessories_days: days,
                items_meters: 0, // não se aplica
                accessories_discount: discount,
                accessories_price: price
            });
        } else {
            var meters = row.find('.meters_input').val()?.trim() || '';
            var items_meters = row.find('.items_meters_input').val()?.trim() || '';

            accessories.push({
                accessories_description: description,
                accessories_quantity: quantity,
                meters: meters,
                accessories_unit_price: unit_price,
                accessories_days: days,
                items_meters: items_meters,
                accessories_discount: discount,
                accessories_price: price
            });
        }
    });
    return accessories;
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

    $('#accessories_table_body tr').each(function() {
        var isRowEmpty = !$.trim($(this).find('.accessories_description_placeholder').text());
        if (isRowEmpty) {
            $(this).remove();
        }
    });
})
