document.getElementById('wifiForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const ssid = formData.get('ssid');
    const password = formData.get('password');
    const security = formData.get('security');

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(formData),
    })
    .then(response => response.blob())
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        const qrcodeImage = document.getElementById('qrcodeImage');
        const qrcodeContainer = document.getElementById('qrcodeContainer');

        qrcodeImage.src = imageUrl;
        qrcodeContainer.classList.remove('hidden');

        // Botão de download
        const downloadButton = document.getElementById('downloadButton');
        downloadButton.onclick = () => {
            const link = document.createElement('a');
            link.href = imageUrl;
            link.download = 'wifi_qrcode.png';
            link.click();
        };
    })
    .catch(error => console.error('Erro:', error));
});

// Notifica o servidor quando a guia é fechada
window.addEventListener('beforeunload', function() {
    fetch('/fechar_guia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    });
});