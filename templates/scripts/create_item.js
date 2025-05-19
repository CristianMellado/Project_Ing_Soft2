
export function createMedia(data, Div, shop) {
    var infoDiv = document.createElement('div');
    infoDiv.className = 'info';

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

    var buyButton = document.createElement('button');
    buyButton.className = 'buy-button';

    buyButton.textContent = 'Descargar';
    if(shop==1)
        buyButton.textContent = 'Pagar';

    buyButton.dataset.id = data.id;
    buyButton.addEventListener('click', function () {
        if(shop == 1){
            fetch('/pagarContenido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: data.id})
            })
            .then(response => response.json())
            .then(respuesta => {
                console.log(respuesta);
                if (respuesta.success) {
                    alert("CONTENIDO COMPRADO EXITOSAMENTE :D");
                    window.location.href = `item_view.html?id=${data.id}`;
                } else {
                    alert("NO TIENE SALDO SUFICIENTE D:");
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        else{
            fetch('/verificate_downloaded_content', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ id: data.id})
                })
            .then(response => response.json())
            .then(respuesta => {
                if (respuesta.success) {
                    alert("CONTENIDO DESCARGADO :D");
                    //window.location.href = `item_view.html?id=${data.id}`;
                } else {
                    window.location.href = `item_shop.html?id=${data.id}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    infoDiv.appendChild(author);
    infoDiv.appendChild(price);
    infoDiv.appendChild(extension);
    infoDiv.appendChild(category);
    infoDiv.appendChild(rating);
    infoDiv.appendChild(description);
    Div.appendChild(infoDiv);
    Div.appendChild(buyButton);
}

export function createVideoContent(data, shop) {
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

    createMedia(data, videoDiv, shop);

    var videoContent = document.querySelector('.container');
    videoContent.appendChild(videoDiv);
}

export function createImageContent(data, shop) {
    var Div = document.createElement('div');
    Div.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    Div.appendChild(title);

    var img = document.createElement('img');
    img.src = data.src;
    img.className = "media";
    Div.appendChild(img);

    createMedia(data, Div, shop);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}

export function createAudioContent(data, shop) {
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

    createMedia(data, Div, shop);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}