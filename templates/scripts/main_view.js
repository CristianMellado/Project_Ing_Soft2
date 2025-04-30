import {createImageContent, createAudioContent, createVideoContent} from './create_item.js';

var data_cache = [];

function showContent(contentType) {
    document.querySelector('.container').innerHTML = '';

    data_cache.forEach(element => {
        if(element.type==contentType){
            if (element.type == "imagen") {
                createImageContent(element);
            } else if (element.type == "audio") {
                createAudioContent(element);
            } else {
                createVideoContent(element);
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const tops = ['imagen','audio','video'];
    tops.forEach(i => {
        const boton = document.getElementById(i+"-top");
        boton.addEventListener('click', () => showContent(i));
    })

    fetch('/main_view_content')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data_cache = data;
            console.log(data);
            showContent('imagen');
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
