var data_cache = {
    video: [],
    audio: [],
    image: []
};

function showContent(contentType) {
    document.querySelector('.container').innerHTML = '';

    if (contentType == "image") {
        data_cache.image.forEach(element => {
            createImageContent(element);
        });
    } else if (contentType == "audio") {
        data_cache.audio.forEach(element => {
            createAudioContent(element);
        });
    } else {
        data_cache.video.forEach(element => {
            createVideoContent(element);
        });
    }
}

function createMedia(data, Div) {
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
    buyButton.textContent = 'buy content';

    infoDiv.appendChild(author);
    infoDiv.appendChild(price);
    infoDiv.appendChild(extension);
    infoDiv.appendChild(category);
    infoDiv.appendChild(rating);
    infoDiv.appendChild(description);
    Div.appendChild(infoDiv);
    Div.appendChild(buyButton);
}

function createVideoContent(data) {
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

    createMedia(data, videoDiv);

    var videoContent = document.querySelector('.container');
    videoContent.appendChild(videoDiv);
}

function createImageContent(data) {
    var Div = document.createElement('div');
    Div.className = 'media-item';

    var title = document.createElement('h2');
    title.textContent = data.title;
    Div.appendChild(title);

    var img = document.createElement('img');
    img.src = data.src;
    img.className = "media";
    Div.appendChild(img);

    createMedia(data, Div);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}

function createAudioContent(data) {
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

    createMedia(data, Div);

    var Content = document.querySelector('.container');
    Content.appendChild(Div);
}

document.addEventListener('DOMContentLoaded', function () {
    fetch('/main_view_content')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data_cache = data;
            showContent('image');
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
