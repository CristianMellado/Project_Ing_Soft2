document.getElementById("content-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const contentType = document.getElementById("content-type").value.trim();
    const fileInput = document.getElementById("fileInput").files[0];
    const title = document.getElementById("content-title").value.trim();
    const author = document.getElementById("content-author").value.trim();
    const price = document.getElementById("content-price").value.trim();
    const category = document.getElementById("content-category").value.trim();
    const description = document.getElementById("content-description").value.trim();

    if (!fileInput || !title || !author || !price || !category || !description) {
        alert("Por favor, completa todos los campos sin dejar espacios en blanco.");
        return;
    }

    // Validar que el precio sea un número positivo válido
    if (isNaN(price) || Number(price) < 0) {
        alert("Por favor, ingresa un precio válido (número positivo).");
        return;
    }

    const formData = new FormData(this);

    fetch("/save_content", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Contenido guardado");
            window.location.href = "admi_view.html";
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error("Error:", err));
});