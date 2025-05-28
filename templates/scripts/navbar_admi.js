function generateNavbar() {
    var href_logo="#";
    fetch('/get_user_role')
            .then(response => response.json())
            .then(data => {
                if (data.role === 'Administrador') {
                    href_logo = 'admi_view.html';
                } else if (data.role === 'Cliente') {
                    href_logo = 'user_view.html';
                } else {
                    //alert("Sesión inválida o no identificada.");
                    //console.log("Sesión inválida o no identificada.");
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Error al verificar rol:', error);
                //alert("Error al verificar tu rol.");
                window.location.href = '/';
    });
    var header = document.createElement('header');
    var stylevar = document.createElement('link');
    stylevar.href = "/styles/navbar.css";
    stylevar.rel = "stylesheet"; 
    stylevar.type = "text/css";

    var stylevar2 = document.createElement('link');
    stylevar2.href = "/styles/recargas_admi.css";
    stylevar2.rel = "stylesheet"; 
    stylevar2.type = "text/css";

    var nav = document.createElement('nav');
    var ul = document.createElement('ul');

    var liLogo = document.createElement('li');
    var btnLogo = document.createElement('button');
    btnLogo.textContent = 'DownEz';
    btnLogo.id = 'logo-btn';
    btnLogo.addEventListener('click', function () {
        window.location.href = href_logo;
    });
    liLogo.appendChild(btnLogo);
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

    var clearButton = document.createElement('button');
    clearButton.setAttribute('type', 'button');
    clearButton.textContent = '✖';
    clearButton.classList.add('clear-search-btn');
    searchForm.appendChild(clearButton);
    clearButton.addEventListener('click', function () {
        searchInput.value = '';
        resultsContainer.innerHTML = '';
        filterContainer.querySelectorAll('.filter-checkbox').forEach(cb => cb.checked = false);
    });
    

    var filterContainer = document.createElement('div');
    filterContainer.classList.add('filter-checkboxes');

    var filtros = ['video', 'audio', 'imagen','author']; 
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

    var options = { "Recargas":"#", "Agregar Contenido":"addContent.html","Sign out": "login.html"};
    for(var key in options){
        var liOption = document.createElement('li');

        if (key === "Recargas") {
            var btn = document.createElement('button');
            btn.textContent = key;
            btn.id = "recargas-btn";
            liOption.appendChild(btn);
        } else if (key === "Sign out") {
            var signOutBtn = document.createElement('button');
            signOutBtn.id = "logout-btn";
            signOutBtn.textContent = key;
            signOutBtn.addEventListener('click', function () {
                fetch('/logout_account', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = 'login.html';
                    } else {
                        alert('Error al cerrar sesión');
                        window.location.href = '/';
                    }
                })
                .catch(error => {
                    console.error('Error durante logout:', error);
                    alert('Error al cerrar sesión');
                    window.location.href = '/';
                });
            });
            liOption.appendChild(signOutBtn);
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
    header.appendChild(stylevar2);
    document.body.insertBefore(header, document.body.firstChild);

    var resultsContainer = document.createElement('div');
    resultsContainer.setAttribute('id', 'search-results');
    document.body.insertBefore(resultsContainer, header.nextSibling);

    // [RF-0014] envia una cadena de texto para buscarla en los contenidos existentes.
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
                        <a href=item_view_admi.html?id=${item.id}><h4>${item.title}</a>(${item.type})</h4>
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

        if (texto.trim() === '') {
            resultsContainer.innerHTML = "<p>Ingrese búsqueda.</p>";
            return;
        }

        realizarBusqueda(texto);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    generateNavbar();
});

document.addEventListener('DOMContentLoaded', function () {

    if (!document.getElementById('recargas-container')) {
        var recargasContainer = document.createElement('div');
        recargasContainer.id = 'recargas-container';
        recargasContainer.style.display = 'none';
        document.body.appendChild(recargasContainer);
    }

    // [RF-0013] obtiene del servidor las solicitudes de saldo pendientes de los clientes.
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

    // [RF-0012] El Administrador aprueba la solicitud de saldo de un cliente.
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