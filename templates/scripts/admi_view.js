// [RF-0015] envía una cadena de texto para buscarla en los contenidos y usuarios existentes.
document.addEventListener('DOMContentLoaded', function () {
    const formBusqueda = document.getElementById('form-busqueda');
    const searchInput = document.getElementById('search-input');
    const checkboxes = document.querySelectorAll('.filtro-tipo');
    const searchResults = document.getElementById('search-results-admi');

    formBusqueda.addEventListener('submit', function (e) {
        e.preventDefault();

        const query = searchInput.value.trim();
        if (query === '') {
            searchResults.innerHTML = "<p>Ingrese búsqueda.</p>";
            return;
        }

        const filters = Array.from(checkboxes)
            .filter(chk => chk.checked)
            .map(chk => chk.value);

        fetch('/search_info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, filters })
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
            <span><strong>Autor/Email</strong></span>
            <span><strong>Tipo/Estado</strong></span>
        `;
        searchResults.appendChild(header);
    
        data.forEach(item => {
            const row = document.createElement('a');
            if(item.type!='cliente' && item.type!='ex-cliente' && item.type!='administrador'){
                row.href = `item_info_edit.html?id=${item.id}`;
            }
            else{
                row.href = `user_info.html?id=${item.id}`;
            }
            row.className = 'result-row';
            row.innerHTML = `
                <span>${item.id}</span>
                <span>${item.title}</span>
                <span>${item.author}</span>
                <span>${item.type}</span>
            `;
            searchResults.appendChild(row);
        });
    }
    
});