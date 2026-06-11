document.addEventListener("DOMContentLoaded", function () {
    console.log("Login y dependencias JS cargadas correctamente.");

    const loginForm = document.getElementById("loginForm");
    const errorContainer = document.getElementById("errorContainer");

    if (loginForm) {
      loginForm.addEventListener("submit", function (e) {

        if (errorContainer) {
          errorContainer.style.display = 'none';
          errorContainer.textContent = '';
        }

        const usernameInput = document.getElementById("username").value.trim();
        const passwordInput = document.getElementById("password").value;

        if (usernameInput === "") {
          mostrarError("Por favor, ingresa un nombre de usuario válido.");
          return;
        }

        if (passwordInput === "") {
            mostrarError("Por favor, ingresa tu contraseña.");
            return;
        }
      });
    }

    function mostrarError(mensaje) {
        if (errorContainer) {
            errorContainer.textContent = mensaje;
            errorContainer.style.display = 'block';
        } else {
            alert(mensaje);
        }
    }
});