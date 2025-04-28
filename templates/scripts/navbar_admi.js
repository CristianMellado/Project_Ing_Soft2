function generateNavbar() {
    var header = document.createElement('header');
    var stylevar = document.createElement('link');
    stylevar.href = "/styles/navbar.css";
    stylevar.rel = "stylesheet"; 
    stylevar.type = "text/css";

    var nav = document.createElement('nav');
    var ul = document.createElement('ul');

    // Opción "YouEz"
    var liYouEz = document.createElement('li');
    var aYouEz = document.createElement('a');
    aYouEz.href = 'admi_view.html';
    aYouEz.textContent = 'YouEz';
    liYouEz.appendChild(aYouEz);
    ul.appendChild(liYouEz);


    var options = {"Delete Content":"deleteContent.html",
    "Add Content":"addContent.html", 
    "Clients":"clients.html", 
    "confirm orders":"clientsMoney.html", 
    "Sign out": "login.html"};
    for(var key in options){
        var liInformes = document.createElement('li');
        var aInformes = document.createElement('a');
        aInformes.href = options[key];
        aInformes.textContent = key;    
        liInformes.appendChild(aInformes);
        ul.appendChild(liInformes);
    };

    nav.appendChild(ul);
    header.appendChild(nav);
    header.appendChild(stylevar);

    document.body.insertBefore(header, document.body.firstChild);
}

document.addEventListener('DOMContentLoaded', function () {
    generateNavbar();
});
