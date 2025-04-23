function formatModelId(modelId) {
    return modelId.toString().padStart(3, '0');
}

function formatModelIdOnPage() {
    const modelIdElements = document.querySelectorAll('.kva-model-id');

    modelIdElements.forEach((element) => {
        const rawValue = element.textContent.trim();
        const formattedValue = formatModelId(rawValue);
        element.textContent = formattedValue;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    formatModelIdOnPage();
});

document.querySelectorAll('.modelo').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.modelo').forEach(i => i.classList.remove('selecionada'));
        this.classList.add('selecionada');
        document.getElementById('visualizar').disabled = false;

        const modelId = this.getAttribute('data-model-id');
        console.log(modelId)
        document.getElementById('visualizar').onclick = function() {
            window.location.href = 'modelo/visualizar/' + modelId;
        };
    });
});

document.getElementById('incluir').onclick = function () {
    window.location.href = '/modelo';
};
