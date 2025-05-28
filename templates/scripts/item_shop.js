import {createImageContent, createAudioContent, createVideoContent} from './create_item.js';

document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    const isGift = params.get('gift') === '1';

    const itemDetails = document.querySelector('.container');

    if (!id) {
        itemDetails.innerHTML = "<p>Error: No se proporcionó un ID válido.</p>";
        return;
    }

    fetch('/get_content_by_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
        .then(response => response.json())
        .then(data => {
            if(data) {
                itemDetails.innerHTML = '';
                
                if (data.type == "imagen") {
                    createImageContent(data, 1);
                } else if (data.type == "audio") {
                    createAudioContent(data, 1);
                } else {
                    createVideoContent(data, 1);
                }
            } else {
                itemDetails.innerHTML = "<p>No se encontró el item.</p>";
            }

            if (isGift) {
                const container = document.querySelector('.media-item');
                const label = document.createElement('label');
                label.textContent = 'Usuario destinatario: ';
                const input = document.createElement('input');
                input.type = 'text';
                input.id = 'recipient';
                input.placeholder = 'Nombre de usuario o correo';
                input.style.margin = '10px';

                const sendBtn = document.createElement('button');
                sendBtn.textContent = 'Enviar regalo';
                sendBtn.className = 'send-gift';
                sendBtn.addEventListener('click', () => {
                    const recipient = input.value.trim();
                    if (!recipient) {
                        alert('Debes ingresar un destinatario.');
                        return;
                    }
                    // [RF-0007] envia la peticón al server para verificar y enviar un regalo a un cliente existente.
                    fetch('/gift_content', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            id: id,
                            destinatario: recipient
                        })
                    })
                    .then(res => res.json())
                    .then(response => {
                        if (response.success) {
                            alert("¡Contenido regalado exitosamente!");
                            window.location.href = `user_view.html`;
                        } 
                        else{
                            alert(response.msg);
                        }
                    })
                    .catch(err => {
                        console.error('Error al enviar regalo:', err);
                        alert("Error al conectar con el servidor.");
                    });
                });

                container.appendChild(label);
                container.appendChild(input);
                container.appendChild(sendBtn);
            } 
        })
        .catch(error => {
            console.error('Error obteniendo el item:', error);
            itemDetails.innerHTML = "<p>Error cargando el contenido.</p>";
        });
});
