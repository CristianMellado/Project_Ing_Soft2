document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');

    const itemDetails = document.querySelector('#user-info');

    if (!id) {
        itemDetails.innerHTML = "<p>Error: No se proporcionó un ID válido.</p>";
        return;
    }

    fetch('/get_user_by_id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
        .then(response => response.json())
        .then(data => {
            if (data) {
                itemDetails.innerHTML = `
                <p><strong>Usuario:</strong> ${data.username}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>ID:</strong> ${id}</p>
                <p><strong>saldo:</strong> ${data.saldo}</p>
                <p><strong>Estado cuenta:</strong> ${data.estado}</p>
            `;
                
            } else {
                itemDetails.innerHTML = "<p>No se encontró el item.</p>";
            }
        })
        .catch(error => {
            console.error('Error obteniendo el item:', error);
            itemDetails.innerHTML = "<p>Error cargando el contenido.</p>";
        });


    const downloadsList = document.getElementById("downloads-list");

    fetch("/get_user_downloads_info", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(res => res.json())
    .then(data => {
        if (data.length === 0) {
            downloadsList.innerHTML = '<li>No hay contenidos descargados.</li>';
            return;
        }

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerHTML = `
                        <a href=item_view.html?id=${item.id}><h4>${item.title}</a>
                        (${item.type})</h4>
                        <p><strong>Autor:</strong> ${item.author} | <strong>Puntuación:</strong> ${item.rating}</p>
            `;
            downloadsList.appendChild(li);
        });
    })
    .catch(err => {
        downloadsList.innerHTML = '<li style="color:red">Error al cargar contenidos.</li>';
        console.error(err);
    });

});