function generateNavbar() {
    var header = document.createElement('header');
    var stylevar = document.createElement('link');
    stylevar.href = "/styles/navbar.css";
    stylevar.rel = "stylesheet"; 
    stylevar.type = "text/css";

    var nav = document.createElement('nav');
    var ul = document.createElement('ul');

    var liLogo = document.createElement('li');
    var aLogo = document.createElement('a');
    aLogo.href = 'user_view.html';
    aLogo.textContent = 'DownEz';
    liLogo.appendChild(aLogo);
    ul.appendChild(liLogo);

    var searchLi = document.createElement('li');
    searchLi.classList.add('search-layout');

    var searchContainer = document.createElement('div');
    searchContainer.classList.add('search-container');

    var searchForm = document.createElement('form');
    searchForm.setAttribute('action', '#'); 
    searchForm.setAttribute('method', 'get');
    searchForm.classList.add('search-form');

    var searchInput = document.createElement('input');
    searchInput.setAttribute('type', 'text');
    searchInput.setAttribute('name', 'search');
    searchInput.setAttribute('placeholder', 'Escribe lo que buscas...');
    searchForm.appendChild(searchInput);

    var searchButton = document.createElement('button');
    searchButton.setAttribute('type', 'submit');
    searchButton.textContent = 'Buscar';
    searchForm.appendChild(searchButton);

    var filterContainer = document.createElement('div');
    filterContainer.classList.add('filter-checkboxes');

    var filtros = ['video', 'audio', 'imagen']; // Ya no 'todos'
    filtros.forEach(tipo => {
        var label = document.createElement('label');
        label.classList.add('filter-label');

        var checkbox = document.createElement('input');
        checkbox.setAttribute('type', 'checkbox');
        checkbox.classList.add('filter-checkbox');
        checkbox.dataset.filter = tipo;

        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(tipo.charAt(0).toUpperCase() + tipo.slice(1)));
        filterContainer.appendChild(label);
    });

    searchContainer.appendChild(searchForm);
    searchContainer.appendChild(filterContainer);
    searchLi.appendChild(searchContainer);
    ul.appendChild(searchLi);

    var options = { "Recargas":"#", "Add Content":"addContent.html","Sign out": "login.html"};
    for(var key in options){
        var liOption = document.createElement('li');

        if (key === "Recargas") {
            var btn = document.createElement('button');
            btn.textContent = key;
            btn.id = "recargas-btn";
            liOption.appendChild(btn);
        } else {
            var aOption = document.createElement('a');
            aOption.href = options[key];
            aOption.textContent = key;
            liOption.appendChild(aOption);
        }

        ul.appendChild(liOption);
    }

    nav.appendChild(ul);
    header.appendChild(nav);
    header.appendChild(stylevar);
    document.body.insertBefore(header, document.body.firstChild);

    var resultsContainer = document.createElement('div');
    resultsContainer.setAttribute('id', 'search-results');
    document.body.insertBefore(resultsContainer, header.nextSibling);

    function realizarBusqueda(textoBusqueda) {
        const query = textoBusqueda.trim().toLowerCase();
        const selectedFilters = Array.from(filterContainer.querySelectorAll('.filter-checkbox'))
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.dataset.filter);

        fetch('/search_content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query, filters: selectedFilters })
        })
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                var html = '<div class="result-cards">';
                data.forEach(item => {
                    html += `
                    <div class="result-card">
                        <a href=item_view.html?id=${item.id}><h4>${item.title}</h4></a>
                        <p><strong>Autor:</strong> ${item.author}</p>
                    </div>`;
                });
                html += '</div>';
                resultsContainer.innerHTML = html;
            } else {
                resultsContainer.innerHTML = "<p>No se encontraron resultados.</p>";
            }
        })
        .catch(error => {
            console.error('Error buscando:', error);
            resultsContainer.innerHTML = "<p>Error al buscar.</p>";
        });
    }

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const texto = searchInput.value;
        realizarBusqueda(texto);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    generateNavbar();
});

