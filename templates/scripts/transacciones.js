document.addEventListener('DOMContentLoaded', function () {
    const searchResults = document.getElementById('search-results-admi');
    const actionButton = document.getElementById('option-action');
    const selectOption = document.getElementById("content-filter");

    // [RF-0197] Solicita y renderiza datos genéricos de tablas según tipo seleccionado
    actionButton.addEventListener('click', () => {
        const selected = selectOption.value;

        if (!selected) return;

        fetch('/get_transacciones_generales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tipo: selected })
        })
        .then(res => res.json())
        .then(data => renderizarGenerico(data))
        .catch(err => {
            console.error('Error en transacción general:', err);
            searchResults.innerHTML = "<p>Error al obtener datos.</p>";
        });
    });

    // [RF-0198] Renderiza una tabla genérica usando encabezados y datos en filas
    function renderizarGenerico(data) {
        searchResults.innerHTML = '';

        if (!data || !data.labels || !data.rows || data.rows.length === 0) {
            searchResults.innerHTML = '<p>No hay datos disponibles.</p>';
            return;
        }

        const labels = data.labels;
        const rows = data.rows;

        // Encabezados
        const header = document.createElement('div');
        header.className = 'result-header';
        header.innerHTML = labels.map(label => `<span><strong>${label}</strong></span>`).join('');
        searchResults.appendChild(header);

        // Filas de datos
        rows.forEach(fila => {
            const row = document.createElement('div');
            row.className = 'result-row';
            row.innerHTML = fila.map(cell => `<span>${cell}</span>`).join('');
            searchResults.appendChild(row);
        });
    }
});