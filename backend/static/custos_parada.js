function parseBRDecimal(value) {
    const cleaned = value.replace(/\./g, '').replace(',', '.').trim();
    const number = parseFloat(cleaned);
    return isNaN(number) ? 0 : number;
}

function toBRL(value) {
    return 'R$ ' + value.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function atualizarTotaisSubLocacao() {
    let totalMaquinas = 0;
    let totalAcessorios = 0;

    $('#sub_body tr').each(function () {
       const valMaquina = $(this).find('td:nth-child(10) .editable-cell').text();
       const valAcessorio = $(this).find('td:nth-child(11) .editable-cell').text();

       totalMaquinas += parseBRDecimal(valMaquina);
       totalAcessorios += parseBRDecimal(valAcessorio);
    });

    $('#sub_total_value_machines').val(toBRL(totalMaquinas));
    $('#sub_total_value_accessories').val(toBRL(totalAcessorios));
}

function configurarEventosSubLocacao() {
    $('#sub_body .editable-cell').on('input', function () {
        atualizarTotaisSubLocacao();
    });
}

function atualizarTotaisFrete() {
    let totalFretes = 0;
    let totalFreteTerceiro = 0;

    $('#freight_body tr').each(function () {
       const valFreteTerceiro = $(this).find('td:nth-child(11) .editable-cell').text();
       const valFrete = $(this).find('td:nth-child(12) .editable-cell').text();

       totalFreteTerceiro += parseBRDecimal(valFreteTerceiro);
       totalFretes += parseBRDecimal(valFrete);
    });

    $('#freight_total_value').val(toBRL(totalFretes));
    $('#freight_total_value_third').val(toBRL(totalFreteTerceiro));
}

function configurarEventosFrete() {
    $('#freight_body .editable-cell').on('input', function () {
        atualizarTotaisFrete();
    });
}

function atualizarTotaisCustoOp() {
    let totalAlimEstadia = 0;
    let totalCustoOp = 0;

    $('#op_cost_body tr').each(function () {
       const valAlimEstadia = $(this).find('td:nth-child(13) .editable-cell').text();
       const valCustoOp = $(this).find('td:nth-child(14) .editable-cell').text();

       totalAlimEstadia += parseBRDecimal(valAlimEstadia);
       totalCustoOp += parseBRDecimal(valCustoOp);
    });

    $('#op_cost_total_value_food_stay').val(toBRL(totalAlimEstadia));
    $('#op_cost_total_value').val(toBRL(totalCustoOp));
}

function configurarEventosCustosOp() {
    $('#op_cost_body .editable-cell').on('input', function () {
        atualizarTotaisCustoOp();
    });
}

$(document).ready(function () {
    atualizarTotaisSubLocacao();
    configurarEventosSubLocacao();
    atualizarTotaisFrete();
    configurarEventosFrete();
    atualizarTotaisCustoOp();
    configurarEventosCustosOp();
});

function collectSubsLoc() {
    var subs = [];
    $('#sub_body tr' || '').each(function() {
        const sub_description = $(this).find('td:nth-child(3) .editable-cell').text().trim();

        if (!sub_description) return;

        var sub = {
            stop_cost_sub_id: $(this).find('input[name="stop_cost_sub_id"]').val(),
            contract_id: $(this).find('input[name="contract_id"]').val(),
            sub_description: $(this).find('td:nth-child(3) .editable-cell').text(),
            sub_supplier: $(this).find('td:nth-child(4) .editable-cell').text(),
            sub_note: $(this).find('td:nth-child(5) .editable-cell').text(),
            sub_initial_period: $(this).find('td:nth-child(6) .editable-cell').text(),
            sub_final_period: $(this).find('td:nth-child(7) .editable-cell').text(),
            sub_rental_days: $(this).find('td:nth-child(8) .editable-cell').text(),
            sub_daily_value: $(this).find('td:nth-child(9) .editable-cell').text(),
            sub_value_machine: $(this).find('td:nth-child(10) .editable-cell').text(),
            sub_value_accessory: $(this).find('td:nth-child(11) .editable-cell').text(),
            sub_total_value_machines: $('#sub_total_value_machines').val(),
            sub_total_value_accessories: $('#sub_total_value_accessories').val()
        };
        subs.push(sub);
    });
    return subs;
}

function collectFreights() {
    var freights = [];
    $('#freight_body tr' || '').each(function() {
        const freight_day = $(this).find('td:nth-child(3) .editable-cell').text().trim();

        if (!freight_day) return;

        var freight = {
            stop_cost_freight_id: $(this).find('input[name="stop_cost_freight_id"]').val(),
            contract_id: $(this).find('input[name="contract_id"]').val(),
            freight_day: $(this).find('td:nth-child(3) .editable-cell').text(),
            freight_driver: $(this).find('td:nth-child(4) .editable-cell').text(),
            freight_finality: $(this).find('td:nth-child(5) .editable-cell').text(),
            freight_own_third: $(this).find('td:nth-child(6) .editable-cell').text(),
            freight_initial_km: $(this).find('td:nth-child(7) .editable-cell').text(),
            freight_final_km: $(this).find('td:nth-child(8) .editable-cell').text(),
            freight_total_km: $(this).find('td:nth-child(9) .editable-cell').text(),
            freight_cost_km: $(this).find('td:nth-child(10) .editable-cell').text(),
            freight_value_third: $(this).find('td:nth-child(11) .editable-cell').text(),
            freight_value: $(this).find('td:nth-child(12) .editable-cell').text(),
            freight_total_value: $('#freight_total_value').val(),
            freight_total_value_third: $('#freight_total_value_third').val()
        };
        freights.push(freight);
    });
    return freights;
}

function collectOpCost() {
    var ops = [];
    $('#op_cost_body tr' || '').each(function() {
        const op_cost_day = $(this).find('td:nth-child(3) .editable-cell').text().trim();

        if (!op_cost_day) return;

        var op = {
            stop_cost_op_cost_id: $(this).find('input[name="stop_cost_op_cost_id"]').val(),
            contract_id: $(this).find('input[name="contract_id"]').val(),
            op_cost_day: $(this).find('td:nth-child(3) .editable-cell').text(),
            op_cost_tec_driver: $(this).find('td:nth-child(4) .editable-cell').text(),
            op_cost_initial_hours: $(this).find('td:nth-child(5) .editable-cell').text(),
            op_cost_final_hours: $(this).find('td:nth-child(6) .editable-cell').text(),
            op_cost_hours: $(this).find('td:nth-child(7) .editable-cell').text(),
            op_cost_value_hours: $(this).find('td:nth-child(8) .editable-cell').text(),
            op_cost_extra_hours: $(this).find('td:nth-child(9) .editable-cell').text(),
            op_cost_value_ex_hours: $(this).find('td:nth-child(10) .editable-cell').text(),
            op_cost_total_value_ex_hours: $(this).find('td:nth-child(11) .editable-cell').text(),
            op_cost_food_stay: $(this).find('td:nth-child(12) .editable-cell').text(),
            op_cost_value: $(this).find('td:nth-child(13) .editable-cell').text(),
            op_cost_total_value: $('#op_cost_total_value').val(),
            op_cost_total_value_food_stay: $('#op_cost_total_value_food_stay').val()
        };
        ops.push(op);
    });
    return ops;
}

function submitStopCost() {
    var stopCostData = {};
    stopCostData.sub = collectSubsLoc();
    stopCostData.freight = collectFreights();
    stopCostData.op_cost = collectOpCost();

    console.log('Stop Cost Data:', stopCostData);
    fetch('/submit_stop_cost', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(stopCostData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Custos de Parada atualizados e salvos com sucesso");
            window.location.href = "/lista_contratos";
        } else {
            alert("Erro: " + data.error);
        }
    })
    .catch(error => {
        console.error('Erro ao salvar custos de parada:', error);
        alert("Erro interno. Tente novamente.")
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('stop_cost_sub_form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        submitStopCost();
    });
});
