function formatKvaGroupId(kvagroupId) {
    return kvagroupId.toString().padStart(3, '0');
}

function formatKvaGroupIdOnPage() {
    const kvagroupIdElements = document.querySelectorAll('.kva-group-id');

    kvagroupIdElements.forEach((element) => {
        const rawValue = element.textContent.trim();
        const formattedValue = formatKvaGroupId(rawValue);
        element.textContent = formattedValue;
    });
}

function formatfamilyId(familyId) {
    return familyId.toString().padStart(3, '0');
}

function formatFamilyOnPage() {
    const familyIdElements = document.querySelectorAll('.family-id');

    familyIdElements.forEach((element) => {
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

document.addEventListener("DOMContentLoaded", () => {
    formatKvaGroupIdOnPage();
    formatFamilyOnPage();
    formatUnitValue();
    formatQuantities();
});

document.querySelectorAll('.grupo').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.grupo').forEach(i => i.classList.remove('selecionada'));
        this.classList.add('selecionada');
        document.getElementById('visualizar').disabled = false;

        const kvagroupId = this.getAttribute('data-group-id');
        console.log(kvagroupId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = 'grupo/visualizar/' + kvagroupId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/grupo/kva';
};
