function generateNavbar() {
    var header = document.createElement('header');
    var stylevar = document.createElement('link');
    stylevar.href = "/styles/navbar.css";
    stylevar.rel = "stylesheet"; 
    stylevar.type = "text/css";

    var nav = document.createElement('nav');
    var ul = document.createElement('ul');

    // Opción "DownEz"
    var liYouEz = document.createElement('li');
    var aYouEz = document.createElement('a');
    aYouEz.href = 'user_view.html';
    aYouEz.textContent = 'DownEz';
    liYouEz.appendChild(aYouEz);
    ul.appendChild(liYouEz);

    // Barra de búsqueda
    var searchLi = document.createElement('li');
    var searchForm = document.createElement('form');
    searchForm.setAttribute('action', '#'); 
    searchForm.setAttribute('method', 'get');
    searchForm.setAttribute('class', "search-form");

    var searchInput = document.createElement('input');
    searchInput.setAttribute('type', 'text');
    searchInput.setAttribute('name', 'search');
    searchInput.setAttribute('placeholder', 'Type your preference...');
    searchForm.appendChild(searchInput);

    var searchButton = document.createElement('button');
    searchButton.setAttribute('type', 'submit');
    searchButton.textContent = 'Search';
    searchForm.appendChild(searchButton);

    searchLi.appendChild(searchForm);
    ul.appendChild(searchLi);

    var options = {"Account":"account.html","CashCar":"CashCar.html","Notifications":"notification.html", "Sign out": "login.html"};
    for(var key in options){
        var liInformes = document.createElement('li');
        var aInformes = document.createElement('a');
        aInformes.href = options[key];
        aInformes.textContent = key;    
        liInformes.appendChild(aInformes);
        ul.appendChild(liInformes);
    }

    nav.appendChild(ul);
    header.appendChild(nav);
    header.appendChild(stylevar);
    document.body.insertBefore(header, document.body.firstChild);

    // Crear contenedor para resultados
    var resultsContainer = document.createElement('div');
    resultsContainer.setAttribute('id', 'search-results');
    document.body.insertBefore(resultsContainer, header.nextSibling);


    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); 
        var query = searchInput.value.trim().toLowerCase();
        if (!query) {
            resultsContainer.innerHTML = "<p>Ingresa algo para buscar.</p>";
            return;
        }

        fetch('/search_content')
            .then(response => response.json())
            .then(data => {
                var allContent = [];
                for (let type in data) {
                    allContent = allContent.concat(data[type]);
                }

                var filtered = allContent.filter(item => 
                    item.title.toLowerCase().includes(query) || 
                    item.author.toLowerCase().includes(query)
                );

                if (filtered.length > 0) {
                    var html = '<h3>Resultados de búsqueda:</h3><ul>';
                    filtered.forEach(item => {
                        html += `<li><a><strong>${item.title}</strong> - ${item.author}</a></li>`;
                    });
                    html += '</ul>';
                    resultsContainer.innerHTML = html;
                } else {
                    resultsContainer.innerHTML = "<p>No se encontraron resultados.</p>";
                }
            })
            .catch(error => {
                console.error('Error buscando:', error);
                resultsContainer.innerHTML = "<p>Error al buscar.</p>";
            });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    generateNavbar();
});
