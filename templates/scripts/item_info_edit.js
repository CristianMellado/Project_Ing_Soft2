// [RF-0010] Se envia datos editados de un contenido, en forma de tipo binario y json de un contenido al servidor.
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const fileNameSpan = document.getElementById("file-name");
    const previewContainer = document.getElementById("preview-container");

    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    // Si hay ID, obtener datos del contenido para edición
    if (id) {
        fetch('/get_content_by_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                document.getElementById('content-type').value = data.type;
                document.getElementById('content-title').value = data.title;
                document.getElementById('content-author').value = data.author;
                document.getElementById('content-price').value = data.price;
                document.getElementById('content-category').value = data.category;
                document.getElementById('content-description').value = data.description;
                console.log(data.estado);
                document.getElementById("send-eliminar").textContent = data.estado=="desactivado" ? "Restaurar" : "Eliminar";

                // Mostrar preview del contenido existente
                previewContainer.innerHTML = "";
                const contentType = data.type;
                if (contentType === "imagen") {
                    const img = document.createElement("img");
                    img.src = data.src;
                    img.style.maxWidth = "300px";
                    img.style.maxHeight = "300px";
                    previewContainer.appendChild(img);
                } else if (contentType === "video") {
                    const video = document.createElement("video");
                    video.src = data.src;
                    video.controls = true;
                    video.style.maxWidth = "300px";
                    previewContainer.appendChild(video);
                } else if (contentType === "audio") {
                    const audio = document.createElement("audio");
                    audio.src = data.src;
                    audio.controls = true;
                    previewContainer.appendChild(audio);
                }

                // Opcional: mostrar nombre del archivo cargado
                fileNameSpan.textContent = "Archivo cargado: " + data.title;
            } else {
                previewContainer.innerHTML = "<p>No se encontró el item.</p>";
            }
        })
        .catch(error => {
            console.error('Error obteniendo el item:', error);
            previewContainer.innerHTML = "<p>Error cargando el contenido.</p>";
        });
    }

    // Mostrar vista previa cuando se selecciona un archivo nuevo
    fileInput.addEventListener("change", function () {
        const file = this.files[0];
        previewContainer.innerHTML = "";
        const contentType = document.getElementById("content-type");

        if (file) {
            fileNameSpan.textContent = file.name;
            document.getElementById("content-title").value = file.name.trim();
            const fileType = file.type;
            const url = URL.createObjectURL(file);

            if (fileType.startsWith("image/")) {
                contentType.value = "imagen";
                const img = document.createElement("img");
                img.src = url;
                img.style.maxWidth = "300px";
                img.style.maxHeight = "300px";
                previewContainer.appendChild(img);

            } else if (fileType.startsWith("video/")) {
                contentType.value = "video";
                const video = document.createElement("video");
                video.src = url;
                video.controls = true;
                video.style.maxWidth = "300px";
                previewContainer.appendChild(video);

            } else if (fileType.startsWith("audio/")) {
                contentType.value = "audio";
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

    // Enviar formulario
    document.getElementById("content-form").addEventListener("submit", function (e) {
        e.preventDefault();

        const contentType = document.getElementById("content-type").value.trim();
        const fileInput = document.getElementById("fileInput").files[0];
        const title = document.getElementById("content-title").value.trim();
        const author = document.getElementById("content-author").value.trim();
        const price = document.getElementById("content-price").value.trim();
        const category = document.getElementById("content-category").value.trim();
        const description = document.getElementById("content-description").value.trim();
        const fileInputV = document.getElementById("fileInput");

        if (!id || !title || !author || !price || !category || !description) {
            alert("Por favor, completa todos los campos sin dejar espacios en blanco.");
            return;
        }

        if (isNaN(price) || Number(price) < 0) {
            alert("Por favor, ingresa un precio válido (número positivo).");
            return;
        }

        const formData = new FormData(this);
        if (id) {
            formData.append("id", id);
        }

        if (!fileInputV.files || fileInputV.files.length === 0) {
            console.log("No se ha subido ningún archivo.");
            //alert(1);
            //formData.append("changes", false);
        }
        // else{
        //     formData.append("changes", true);
        // }

        fetch("/update_content", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Contenido guardado");
                window.location.href = "admi_view.html";
            } else {
                alert(data.message || "Error al guardar el contenido.");
            }
        })
        .catch(err => console.error("Error:", err));
    });

    del_button(id);
    button_info_promos();

    // Agregar promoción (redireccionar o mostrar un modal, tú eliges)
    document.getElementById("btn-agregar-promo").addEventListener("click", () => {
        const form = document.getElementById("form-agregar-promo");
        form.style.display = form.style.display === "none" ? "block" : "none";
    });

    // Usar promoción
    document.getElementById("btn-usar-promo").addEventListener("click", function () {
        designar_promocion(id);
    });
});


// [RF-0150] Función que controla el estado del botón eliminar o restaurar contenido.
function del_button(id){
    let isDeleted = false;

    document.getElementById("send-eliminar").addEventListener("click", function () {
        if (!id) {
            alert("No hay un contenido cargado para eliminar/restaurar.");
            return;
        }

        fetch("/update_content_state", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id: id})
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                isDeleted = data.estado || false;
                document.getElementById("send-eliminar").textContent = isDeleted ? "Restaurar" : "Eliminar";
                alert(data.message || (isDeleted ? "Contenido eliminado" : "Contenido restaurado"));
            } else {
                alert(data.message || "Error en la operación.");
            }
        })
        .catch(err => {
            console.error("Error:", err);
            alert("Error de conexión con el servidor.");
        });
    });    
}

// [RF-0156] Funcion que hace un get de todas las promociones disponibles.
function button_info_promos(){
    const promoBtn = document.getElementById("send-promocion");
    const promoContainer = document.getElementById("promocion-container");
    const promoSelect = document.getElementById("promo-select");

    promoBtn.addEventListener("click", function () {
        // Mostrar/ocultar el menú
        promoContainer.style.display = promoContainer.style.display === "none" ? "block" : "none";

        // Solicitar promociones actuales
        fetch("/get_promociones")  // Tu endpoint debe devolver un JSON con una lista de promociones
            .then(res => res.json())
            .then(data => {
                // Limpiar y rellenar el select
                promoSelect.innerHTML = `<option value="">Selecciona una promoción</option>`;
                data.forEach(promo => {
                    const option = document.createElement("option");
                    option.value = promo.id;
                    option.textContent = `${promo.titulo_de_descuento} - Descuento: ${Math.round(promo.descuento * 100)}%`;
                    promoSelect.appendChild(option);
                });
            })
            .catch(err => {
                console.error("Error cargando promociones:", err);
                alert("Error al obtener promociones.");
            });
    });    
}

// [RF-0167] Función que asigna cierta promoción a un contenido.
function designar_promocion(id){
    const promoSelect = document.getElementById("promo-select");
    const selectedPromoId = promoSelect.value;
    if (!selectedPromoId) {
        alert("Selecciona una promoción para usar.");
        return;
    }

    if (!id) {
        alert("Primero guarda el contenido para poder asignarle una promoción.");
        return;
    }

    fetch("/asignar_promocion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id_contenido: id, id_promocion: selectedPromoId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert("Promoción asignada correctamente.");
        } else {
            alert(data.message || "Error al asignar promoción.");
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Error al comunicar con el servidor.");
    });    
}