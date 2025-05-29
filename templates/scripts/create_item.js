
// [RF-0029] Función que renderiza la información de un contenido, ya sea de video, audio, o imagen.
export function createMedia(data, Div, current_role) {
    var infoDiv = document.createElement('div');
    infoDiv.className = 'info';
    infoDiv.style.cursor = 'pointer';

    var author = document.createElement('p');
    author.textContent = 'Autor: ' + data.author;

    var price = document.createElement('p');
    price.textContent = 'Precio: ' + data.price;

    var extension = document.createElement('p');
    extension.textContent = 'Extensión de archivo: ' + data.extension;

    var category = document.createElement('p');
    category.textContent = 'Categoría: ' + data.category;

    var rating = document.createElement('p');
    rating.textContent = 'Nota promedio: ' + data.rating;

    var description = document.createElement('p');
    description.textContent = 'Descripción: ' + data.description;
    
    //var buyButton = document.createElement('button');
    //buyButton.className = 'buy-button';

    //buyButton.dataset.id = data.id;

    infoDiv.addEventListener('click', function () {
        // [RF-0005] envia al servidor la verificaion si puede decargar cierto contenido.
        fetch('/verificate_downloaded_content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: data.id })
        })
        .then(response => response.json())
        .then(respuesta => {
            if (respuesta.success) {
                window.location.href = `item_view.html?id=${data.id}`;
            } 
            else {
                if(current_role=='Cliente'){
                    window.location.href = `item_shop.html?id=${data.id}`;
                }
                
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    infoDiv.appendChild(author);
    infoDiv.appendChild(price);
    infoDiv.appendChild(extension);
    infoDiv.appendChild(category);
    infoDiv.appendChild(rating);
    infoDiv.appendChild(description);
    Div.appendChild(infoDiv);
}

// [RF-0030] Renderización de video de cierto contenido.
export function createVideoContent(data, current_role) {
    var videoDiv = document.createElement('div');
    videoDiv.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    videoDiv.appendChild(title);

    var video = document.createElement('video');
    video.controls = true;
    video.src = data.src;
    video.type = "video/mp4";
    video.textContent = 'Your browser does not support the video element.';
    videoDiv.appendChild(video);

    createMedia(data, videoDiv, current_role);

    var videoContent = document.querySelector('.container');
    videoContent.appendChild(videoDiv);
}

// [RF-0031] Renderización de imagen de cierto contenido.
export function createImageContent(data, current_role) {
    var Div = document.createElement('div');
    Div.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    Div.appendChild(title);

    var img = document.createElement('img');
    img.src = data.src;
    img.className = "media";
    Div.appendChild(img);

    createMedia(data, Div, current_role);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}

// [RF-0032] Renderización de audio de cierto contenido.
export function createAudioContent(data, current_role) {
    var Div = document.createElement('div');
    Div.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    Div.appendChild(title);

    var au = document.createElement('audio');
    au.src = data.src;
    au.controls = true;
    au.className = "media";
    Div.appendChild(au);

    createMedia(data, Div, current_role);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}