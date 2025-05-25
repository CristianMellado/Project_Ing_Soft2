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

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const fileNameSpan = document.getElementById("file-name");
    const previewContainer = document.getElementById("preview-container");

    fileInput.addEventListener("change", function () {
        const file = this.files[0];
        previewContainer.innerHTML = ""; // Limpiar previews anteriores
        const contentType = document.getElementById("content-type");

        if (file) {
            fileNameSpan.textContent = file.name;
            document.getElementById("content-title").value = file.name.trim();
            const fileType = file.type;
            const url = URL.createObjectURL(file);

            if (fileType.startsWith("image/")) {
                contentType.value="imagen";
                const img = document.createElement("img");
                img.src = url;
                img.alt = "Vista previa";
                img.style.maxWidth = "300px";
                img.style.maxHeight = "300px";
                previewContainer.appendChild(img);

            } else if (fileType.startsWith("video/")) {
                contentType.value="video";
                const video = document.createElement("video");
                video.src = url;
                video.controls = true;
                video.style.maxWidth = "300px";
                previewContainer.appendChild(video);

            } else if (fileType.startsWith("audio/")) {
                contentType.value="audio";
                const audio = document.createElement("audio");
                audio.src = url;
                audio.controls = true;
                previewContainer.appendChild(audio);

            } else {
                previewContainer.textContent = "Tipo de archivo no compatible para vista previa.";
            }

        } else {
            fileNameSpan.textContent = "Ningún archivo seleccionado";
        }
    });
});