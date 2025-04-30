document.addEventListener("DOMContentLoaded", () => {
    const userInfoDiv = document.getElementById("user-info");
    const userList = document.getElementById("user-list");
    const requestBalanceBtn = document.getElementById("request-balance-btn");
    const closeAccountBtn = document.getElementById("close-account-btn");
    const balanceForm = document.getElementById("balance-form");
    const submitBalanceBtn = document.getElementById("submit-balance");

    fetch("/user_data")
        .then(res => res.json())
        .then(data => {
            console.log(data);
            userInfoDiv.innerHTML = `
                <p><strong>Usuario:</strong> ${data.username}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>ID:</strong> ${data.id}</p>
            `;

    
            const items = ["Contenido A", "Contenido B", "Contenido C"];
            items.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                li.style.cursor = "pointer";
                li.addEventListener("click", () => alert(`Has seleccionado: ${item}`));
                userList.appendChild(li);
            });
        })
        .catch(err => {
            userInfoDiv.innerHTML = "<p style='color:red'>Error al cargar datos del usuario.</p>";
            console.error(err);
        });

    requestBalanceBtn.addEventListener("click", () => {
        balanceForm.style.display = balanceForm.style.display === "none" ? "block" : "none";
    });

    submitBalanceBtn.addEventListener("click", () => {
        const tarjeta = document.getElementById("tarjeta").value;
        const cantidad = parseFloat(document.getElementById("cantidad").value);
        const cardType = document.getElementById("card_type").value;

        if (!tarjeta || isNaN(cantidad) || cantidad <= 0) {
            alert("Complete todos los campos correctamente.");
            return;
        }

        fetch("/request_balance", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ tarjeta, cantidad,cardType })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert("Saldo solicitado con éxito.");
                    balanceForm.style.display = "none";
                } else {
                    alert(data.message);
                }
            })
            .catch(err => {
                alert("Ocurrió un error al procesar la solicitud.");
                console.error(err);
            });
    });

    closeAccountBtn.addEventListener("click", () => {
        if (confirm("¿Estás seguro de cerrar tu cuenta?")) {
            fetch("/close_account", { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert("Cuenta cerrada correctamente.");
                        window.location.href = "/";
                    } else {
                        alert("No se pudo cerrar la cuenta.");
                    }
                })
                .catch(err => {
                    alert("Error al cerrar la cuenta.");
                    console.error(err);
                });
        }
    });
});
