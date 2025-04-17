document.getElementById("registroForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const nombre = document.getElementById("nombre").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value;
    const confirmar = document.getElementById("confirmarContrasena").value;
  
    if (!nombre || !usuario || !contrasena || !confirmar) {
      alert("Por favor completa todos los campos.");
      return;
    }
  
    if (contrasena !== confirmar) {
      alert("Las contraseñas no coinciden.");
      return;
    }
  
    const nuevoUsuario = {
      nombre,
      usuario,
      contrasena,
    };
  
    // Simulamos almacenamiento local
    localStorage.setItem(usuario, JSON.stringify(nuevoUsuario));
  
    alert("¡Usuario registrado con éxito!");
    window.location.href = "login.html";
  });
  