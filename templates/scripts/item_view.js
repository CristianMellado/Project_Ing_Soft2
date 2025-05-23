import {createImageContent, createAudioContent, createVideoContent} from './create_item.js';

document.addEventListener('DOMContentLoaded', function () {
    var header = document.createElement('header');
    var scriptAdmi = document.createElement('script');
    var current_role = "usuario";
    scriptAdmi.type = 'text/javascript';
    fetch('/get_user_role')
        .then(response => response.json())
        .then(data => {
                if (data.role === 'Administrador') {
                    scriptAdmi.src = '/scripts/navbar_admi.js';
                    current_role = "Administrador";
                } else if (data.role === 'Cliente') {
                    scriptAdmi.src = '/scripts/navbar_user.js';
                    current_role = "Cliente";
                } else {
                    scriptAdmi.src = '/scripts/navbar.js';
                }
            })
        .catch(error => {
                console.error('Error al verificar rol:', error);
                alert("Error al verificar tu rol.");
    });
    header.appendChild(scriptAdmi);

    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');

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
            if (data) {
                itemDetails.innerHTML = '';
                
                if (data.type == "imagen") {
                    createImageContent(data,0,current_role);
                } else if (data.type == "audio") {
                    createAudioContent(data,0,current_role);
                } else {
                    createVideoContent(data,0,current_role);
                }
            } else {
                itemDetails.innerHTML = "<p>No se encontró el item.</p>";
            }
        })
        .catch(error => {
            console.error('Error obteniendo el item:', error);
            itemDetails.innerHTML = "<p>Error cargando el contenido.</p>";
        });
});