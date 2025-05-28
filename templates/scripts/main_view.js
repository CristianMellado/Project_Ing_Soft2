import {createImageContent, createAudioContent, createVideoContent} from './create_item.js';

var data_cache = [];

// [RNF-0017] funcion que envia la renderización de un contenido para renderizarlo en imagen, video, o audio.
function showContent(contentType, shop, current_role) {
    document.querySelector('.container').innerHTML = '';

    data_cache.forEach(element => {
        if(element.type==contentType){
            if (element.type == "imagen") {
                createImageContent(element,shop, current_role);
            } else if (element.type == "audio") {
                createAudioContent(element,shop, current_role);
            } else {
                createVideoContent(element,shop, current_role);
            }
        }
    });
}

// [RF-0016] solicita al servidor los contenidos más descargados.
document.addEventListener('DOMContentLoaded', function () {
    var current_role = "usuario";

    fetch('/get_user_role')
        .then(response => response.json())
        .then(data => {
            const scriptAdmi = document.createElement('script');
            scriptAdmi.type = 'text/javascript';

            if (data.role === 'Administrador') {
                scriptAdmi.src = '/scripts/navbar_admi.js';
                current_role = "Administrador";
            } else if (data.role === 'Cliente') {
                scriptAdmi.src = '/scripts/navbar_user.js';
                current_role = "Cliente";
            } else {
                scriptAdmi.src = '/scripts/navbar.js';
            }

            // ✅ Agregar el script al body (o al head) solo después de asignar src
            document.head.appendChild(scriptAdmi);
        })
        .catch(error => {
            console.error('Error al verificar rol:', error);
            // Si quieres puedes cargar el navbar por defecto
            const fallbackScript = document.createElement('script');
            fallbackScript.src = '/scripts/navbar.js';
            document.head.appendChild(fallbackScript);
    });


    const tops = ['imagen','audio','video'];
    tops.forEach(i => {
        const boton = document.getElementById(i+"-top");
        boton.addEventListener('click', () => showContent(i, 0, current_role));
    })

    fetch('/top_content_downloaded')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data_cache = data;
            console.log(data);
            showContent('imagen', 0, current_role);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
