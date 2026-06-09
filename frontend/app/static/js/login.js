document.addEventListener("DOMContentLoaded", function () {
    console.log("Login y dependencias JS cargadas correctamente.");

    const loginForm = document.getElementById("loginForm");
    const errorContainer = document.getElementById("errorContainer");

    if (loginForm) {
      loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

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

        const datos = {
            usuario: usernameInput,
            password: passwordInput
        };

        const url = loginForm.getAttribute('data-action');

        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(res => {
            if (res.ok) {
                window.location.href = '/admin/dashboard';
            } else {
                return res.json().then(err => {
                    throw new Error(err.mensaje || 'Usuario o contraseña incorrectos.');
                });
            }
        })
        .catch(err => {
            mostrarError(err.message);
        });
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