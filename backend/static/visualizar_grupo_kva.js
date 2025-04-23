function formatKvaGroupId(kvaGroupId) {
    return kvaGroupId.toString().padStart(3, '0');
}

function formatKvaGroupIdOnPage() {
    const kvaGroupIdElements = document.querySelectorAll('.kva-group-id');

    kvaGroupIdElements.forEach((element) => {
        const rawValue = element.textContent.trim();
        const formattedValue = formatKvaGroupId(rawValue);
        element.textContent = formattedValue;
    });
}

function formatfamilyId(familyId) {
    return familyId.toString().padStart(3, '0');
}

function formatFamilyOnPage() {
    const familyIdElement = document.querySelectorAll('.family-id');

    familyIdElement.forEach((element) => {
        const rawValue = element.textContent.trim();
        const formattedValue = formatfamilyId(rawValue);
        element.textContent = formattedValue;
    });
}

function formatUnitValue() {
    const unitValues = document.querySelectorAll('.unit-value');
    unitValues.forEach(unitValue => {
        const value = parseFloat(unitValue.textContent.replace(',', '.').replace(/[^\d.-]/g, ''));
        const formattedValue = value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        unitValue.textContent = formattedValue;
    });
}

function formatQuantities() {
    const quantityElements = document.querySelectorAll('.quantity');

    quantityElements.forEach(quantityElement => {
        const value = parseFloat(quantityElement.textContent);

        const formattedValue = value.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });

        quantityElement.textContent = formattedValue;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    formatKvaGroupIdOnPage();
    formatFamilyOnPage();
    formatUnitValue();
    formatQuantities();

    const detalhesGrupoKva = document.querySelectorAll('.grupo-visualizacao');

    let idsVistos = new Set();

    detalhesGrupoKva.forEach((detalhe) => {
        const groupId = detalhe.getAttribute('data-group-id');

        if (idsVistos.has(groupId)) {
            detalhe.style.display = 'none';
        } else {
            idsVistos.add(groupId);
        }
    });
});
