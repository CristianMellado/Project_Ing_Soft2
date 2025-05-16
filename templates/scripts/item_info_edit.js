document.addEventListener('DOMContentLoaded', function () {
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
                document.getElementById('content-type').value = data.type;
                document.getElementById('content-title').value = data.title;
                document.getElementById('content-author').value = data.author;
                document.getElementById('content-price').value = data.price;
                document.getElementById('content-category').value = data.category;
                document.getElementById('content-description').value = data.description;
                document.getElementById('content-file').value = data.src;
                document.getElementById('content-ext').value = data.extension;
            } else {
                itemDetails.innerHTML = "<p>No se encontró el item.</p>";
            }
        })
        .catch(error => {
            console.error('Error obteniendo el item:', error);
            itemDetails.innerHTML = "<p>Error cargando el contenido.</p>";
        });
});