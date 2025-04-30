document.addEventListener('DOMContentLoaded', function () {
    var nameInput = document.getElementById('name');
    var emailInput = document.getElementById('email');
    var password = document.getElementById('password');
    var repeatPassword = document.getElementById('repeat-password');
    var errorMessage = document.getElementById('error-message');
    var submitButton = document.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    
    function checkEmptyFields() {
        if (nameInput.value === "" || emailInput.value === "" || password.value === "" || repeatPassword.value === "") {
            submitButton.disabled = true;
        } else {
            submitButton.disabled = false;
        }
    }

    function validateName() {
        var namePattern = /^[a-zA-Z]+$/; // Patrón para nombres que solo contienen letras

        if (!namePattern.test(nameInput.value)) {
            errorMessage.textContent = "Por favor, ingresa un nombre válido sin espacios";
            submitButton.disabled = true;
        } else {
            errorMessage.textContent = "";
            checkEmptyFields();
        }
    }

    function validateEmail() {
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Patrón para direcciones de correo electrónico válidas

        if (!emailPattern.test(emailInput.value)) {
            errorMessage.textContent = "Por favor, ingresa una dirección de correo electrónico válida";
            submitButton.disabled = true;
        } else {
            errorMessage.textContent = "";
            checkEmptyFields();
        }
    }

    function validatePasswords() {
        if (password.value !== repeatPassword.value) {
            errorMessage.textContent = "Las contraseñas no coinciden";
            submitButton.disabled = true;
        } else {
            errorMessage.textContent = "";
            checkEmptyFields();
        }
    }

    repeatPassword.addEventListener('input', validatePasswords);
    nameInput.addEventListener('input', validateName);
    emailInput.addEventListener('input', validateEmail);
    checkEmptyFields();
    
    var form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var name = document.getElementById('name').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;

        var requestData = {
            name: name,
            password: password,
            email: email
        };

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/register');
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function() {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                if(responseData.success)
                    window.location.href = "login.html";
                else{
                    errorMessage.textContent = "Ya existe un usuario con ese nombre de cuenta.";
                }
            } else {
                alert('Hubo un error al enviar la solicitud.');
            }
        };

        xhr.onerror = function() {
            console.error('Error de red al intentar enviar la solicitud.');
        };

        xhr.send(JSON.stringify(requestData));
    });
});
