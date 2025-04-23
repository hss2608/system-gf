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

document.addEventListener("DOMContentLoaded", () => {
    formatFamilyOnPage();
});

document.querySelectorAll('.familia').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.familia').forEach(i => i.classList.remove('selecionada'));
        this.classList.add('selecionada');
        document.getElementById('visualizar').disabled = false;

        const familyId = this.getAttribute('data-family-id');
        console.log(familyId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = 'familia/visualizar/' + familyId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/bens/familia';
};
