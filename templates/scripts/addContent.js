document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById('uploadForm');

    uploadForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData();

        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        if (!file) {
            alert("Selecciona un archivo.");
            return;
        }

        formData.append("file", file);
        formData.append("typeData", document.getElementById('content-type').value);
        formData.append("title", document.getElementById('content-title').value);
        formData.append("author", document.getElementById('content-author').value);
        formData.append("price", document.getElementById('content-price').value);
        formData.append("category", document.getElementById('content-category').value);
        formData.append("description", document.getElementById('content-description').value);
        formData.append("extension", file.name.split('.').pop().toLowerCase());

        fetch('/save_content', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en el servidor');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.href = "admi_view.html";
            } else {
                document.getElementById('error-message').textContent = data.message || 'Error al guardar el contenido';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
