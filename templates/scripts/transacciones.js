document.addEventListener('DOMContentLoaded', function () {
    const searchResults = document.getElementById('search-results-admi');
    const actionButton = document.getElementById('option-action');
    const selectOption = document.getElementById("content-filter");
    
    
    // [RF-0197] Solicita y envia a renderiza el top ranking de clientes con más descargas.
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
    
    function renderizarGenerico(data) {
        searchResults.innerHTML = '';

        if (!data || data.length === 0) {
            searchResults.innerHTML = '<p>No hay datos disponibles.</p>';
            return;
        }

        const keys = Object.keys(data[0]);

        const header = document.createElement('div');
        header.className = 'result-header';
        header.innerHTML = keys.map(k => `<span><strong>${k}</strong></span>`).join('');
        searchResults.appendChild(header);

        data.forEach(item => {
            const row = document.createElement('div');
            row.className = 'result-row';
            row.innerHTML = keys.map(k => `<span>${item[k]}</span>`).join('');
            searchResults.appendChild(row);
        });
    }
    
});


