function formatClientId(clientId) {
    return clientId.toString().padStart(6, '0');
}

function formatClientIdOnPage() {
    // Seleciona todos os elementos com a classe 'client-id'
    const elements = document.querySelectorAll('.client-id');

    elements.forEach((element) => {
        const rawValue = element.value || element.textContent.trim();
        const formattedValue = formatClientId(rawValue);

        if (element.tagName === 'INPUT') {
            element.value = formattedValue;
        } else {
            element.textContent = formattedValue;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    formatClientIdOnPage();

    tinymce.init({
        selector: '#observations',
        height: 300,
        menubar: false,
        language: 'pt_BR',
        language_url: 'https://cdn.tiny.cloud/1/8wtxfoo5se51jl9zmlz4obivgwepjmxh88vtkopcqk3iuntr/tinymce/6/langs/pt_BR.js', // suporte opcional em português
        plugins: 'lists link table wordcount',
        toolbar: 'undo redo | bold italic underline | fontsizeselect | forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist | removeformat',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
        setup: function (editor) {
            editor.on('init', function () {
                if (proposta && proposta.observations) {
                    editor.setContent(proposta.observations);
                }
            });
        }
    });
});
