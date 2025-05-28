
export function createMedia(data, Div, shop, current_role) {
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
    buyButton.textContent = (shop == 1) ? 'Pagar' : 'Descargar';
    buyButton.dataset.id = data.id;

    buyButton.addEventListener('click', function () {
        if (shop == 1) {
            fetch('/pagarContenido', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: data.id })
            })
            .then(response => response.json())
            .then(respuesta => {
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
        } else {
            // [RF-0005] envia al servidor la verificaion si puede decargar cierto contenido.
            fetch('/verificate_downloaded_content', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: data.id })
            })
            .then(response => response.json())
            .then(respuesta => {
                if (respuesta.success) {
                    alert("CONTENIDO DESCARGADO :D");
                    descargarContenido(data.id, data.title);
                    // console.log(respuesta);
                    // console.log(current_role);
                    if (!respuesta.hasRated && current_role=='Cliente') {
                        showRatingPrompt(data.id);
                        // console.log(2);
                    } 
                    // else {
                    //     window.location.href = `item_view.html?id=${data.id}`;
                    // }
                } else {
                    if(current_role=='Cliente')
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
    if(shop!=1 && current_role === "Cliente"){
        var giftButton = document.createElement('button');
        giftButton.textContent = 'Regalar';
        giftButton.className = 'gift-button';
        giftButton.style.marginLeft = '10px';
        giftButton.addEventListener('click', function () {
            window.location.href = `item_shop.html?id=${data.id}&gift=1`;
        });

        Div.appendChild(giftButton);
        console.log("gift");
    }
}

// [RF-0008] solicita y registra una puntuación para cierto contenido.
function showRatingPrompt(contentId) {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0, 0, 0, 0.6)';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = 1000;

    const modal = document.createElement('div');
    modal.style.background = 'white';
    modal.style.padding = '20px';
    modal.style.borderRadius = '10px';
    modal.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
    modal.style.textAlign = 'center';

    const message = document.createElement('p');
    message.textContent = '¿Deseas calificar este contenido? (Opcional)';
    
    const input = document.createElement('input');
    input.type = 'number';
    input.min = 1;
    input.max = 10;
    input.placeholder = 'Ingresa una puntuación del 1 al 5';
    input.style.margin = '10px';

    const sendButton = document.createElement('button');
    sendButton.textContent = 'Enviar';
    sendButton.style.margin = '5px';

    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Cancelar';
    cancelButton.style.margin = '5px';

    sendButton.addEventListener('click', () => {
        const score = parseFloat(input.value);
        if (isNaN(score) || score < 1 || score > 10) {
            alert("La puntuación debe ser un número entre 1 y 10.");
            return;
        }

        fetch('/rate_content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: contentId, score: score })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("¡Gracias por tu puntuación!");
            } else {
                alert("Hubo un error al enviar tu puntuación.");
            }
            document.body.removeChild(overlay);
            //window.location.href = `item_view.html?id=${contentId}`;
        })
        .catch(err => {
            alert("Error al calificar.");
            console.error(err);
        });
    });

    cancelButton.addEventListener('click', () => {
        document.body.removeChild(overlay);
        //window.location.href = `item_view.html?id=${contentId}`;
    });

    modal.appendChild(message);
    modal.appendChild(input);
    modal.appendChild(sendButton);
    modal.appendChild(cancelButton);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
}

// [RF-0006] pide el contenido al servidor y descarga el contenido en el dispositivo.
function descargarContenido(id,name) {
    fetch('/download_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("No se pudo descargar el archivo");
        }
        return response.blob();
    })
    .then(blob => {
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;

        // Esto es solo temporal si no tienes el nombre desde JS.
        //a.download = "contenido_" + id;
        a.download = name;

        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(downloadUrl);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error al descargar el archivo");
    });
}

export function createVideoContent(data, shop, current_role) {
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

    createMedia(data, videoDiv, shop, current_role);

    var videoContent = document.querySelector('.container');
    videoContent.appendChild(videoDiv);
}

export function createImageContent(data, shop, current_role) {
    var Div = document.createElement('div');
    Div.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    Div.appendChild(title);

    var img = document.createElement('img');
    img.src = data.src;
    img.className = "media";
    Div.appendChild(img);

    createMedia(data, Div, shop, current_role);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}

export function createAudioContent(data, shop, current_role) {
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

    createMedia(data, Div, shop, current_role);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}