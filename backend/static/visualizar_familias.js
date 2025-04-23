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

document.addEventListener('DOMContentLoaded', function() {
    formatFamilyOnPage();
});

document.addEventListener('DOMContentLoaded', function() {
    const detalhesFamilia = document.querySelectorAll('.familia-visualizacao');

    let idsVistos = new Set();

    detalhesFamilia.forEach((detalhe) => {
        const familyId = detalhe.getAttribute('data-family-id');

        if (idsVistos.has(familyId)) {
            detalhe.style.display = 'none';
        } else {
            idsVistos.add(familyId);
        }
    });
});

