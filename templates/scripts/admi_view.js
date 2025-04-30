document.addEventListener('DOMContentLoaded', function () {

    if (!document.getElementById('recargas-container')) {
        var recargasContainer = document.createElement('div');
        recargasContainer.id = 'recargas-container';
        recargasContainer.style.display = 'none';
        document.body.appendChild(recargasContainer);
    }

    function obtenerRecargas() {
        fetch('/get_recargas') 
            .then(response => response.json())
            .then(data => {
                const recargasElement = document.getElementById('recargas-container');
                recargasElement.innerHTML = '<button id="close-recargas">X</button>';

                data.forEach(recarga => {
                    var recargaDiv = document.createElement('div');
                    recargaDiv.classList.add('recarga-item');
                    recargaDiv.innerHTML = `
                        <p><strong>User Id:</strong> ${recarga.usuario}</p>
                        <p><strong>Monto:</strong> $${recarga.monto}</p>
                        <button class="aceptar-recarga" data-id="${recarga.id_recarga}">Aceptar</button>
                    `;
                    recargasElement.appendChild(recargaDiv);
                });

                var aceptarButtons = document.querySelectorAll('.aceptar-recarga');
                aceptarButtons.forEach(button => {
                    button.addEventListener('click', function () {
                        const recargaId = button.getAttribute('data-id');
                        aceptarRecarga(recargaId);
                    });
                });
            })
            .catch(error => {
                console.error('Error al obtener recargas:', error);
            });
    }

    function aceptarRecarga(id_recarga) {
        fetch(`/accept_recarga`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({id_recarga})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Recarga aceptada con éxito');
                obtenerRecargas(); 
            } else {
                alert('Error al aceptar la recarga');
            }
        })
        .catch(error => {
            console.error('Error al aceptar recarga:', error);
        });
    }

    setTimeout(() => {
        const recargasBtn = document.getElementById('recargas-btn');
        const recargasContainer = document.getElementById('recargas-container');

        if (recargasBtn) {
            recargasBtn.addEventListener('click', function () {
                obtenerRecargas();
                if (recargasContainer) {
                    recargasContainer.style.display = 'block';
                }
            });
        }

        const closeBtn = document.getElementById('close-recargas');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                if (recargasContainer) {
                    recargasContainer.style.display = 'none';
                }
            });
        }
    }, 100);

});
