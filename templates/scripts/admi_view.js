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
    
                document.getElementById('close-recargas').addEventListener('click', function () {
                    recargasElement.style.display = 'none';
                });
    
                data.forEach(recarga => {
                    var recargaDiv = document.createElement('div');
                    recargaDiv.classList.add('recarga-item');
                    recargaDiv.innerHTML = `
                        <p><strong>User:</strong> ${recarga.usuario}</p>
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
    }, 100);

});

document.addEventListener('DOMContentLoaded', function () {
    const formBusqueda = document.getElementById('form-busqueda');
    const searchInput = document.getElementById('search-input');
    const checkboxes = document.querySelectorAll('.filtro-tipo');
    const searchResults = document.getElementById('search-results-admi');

    formBusqueda.addEventListener('submit', function (e) {
        e.preventDefault();

        const query = searchInput.value.trim();
        const tipos = Array.from(checkboxes)
            .filter(chk => chk.checked)
            .map(chk => chk.value);

        fetch('/search_info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, tipos })
        })
        .then(res => res.json())
        .then(data => {
            renderizarResultados(data);
        })
        .catch(err => {
            console.error('Error en búsqueda:', err);
        });
    });

    function renderizarResultados(data) {
        searchResults.innerHTML = ''; // Limpiar resultados anteriores
    
        if (data.length === 0) {
            searchResults.innerHTML = '<p>No se encontraron resultados.</p>';
            return;
        }
    
        // Encabezados (opcional, como si fuera tabla)
        const header = document.createElement('div');
        header.className = 'result-header';
        header.innerHTML = `
            <span><strong>ID</strong></span>
            <span><strong>Nombre/Título</strong></span>
            <span><strong>Autor</strong></span>
            <span><strong>Tipo</strong></span>
        `;
        searchResults.appendChild(header);
    
        data.forEach(item => {
            const row = document.createElement('div');
            row.className = 'result-row';
            row.innerHTML = `
                <span>${item.id}</span>
                <span>${item.nombre}</span>
                <span>${item.autor}</span>
                <span>${item.tipo}</span>
            `;
            searchResults.appendChild(row);
        });
    }
    
});