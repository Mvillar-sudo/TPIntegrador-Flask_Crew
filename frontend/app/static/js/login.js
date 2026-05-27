document.addEventListener("DOMContentLoaded", function () {
  console.log("Login y dependencias JS cargadas correctamente.");

  // Aquí puedes agregar validaciones personalizadas en el futuro, por ejemplo:
  const loginForm = document.querySelector("form");
  
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      const usernameInput = document.getElementById("username").value.trim();
      
      if (usernameInput === "") {
        e.preventDefault();
        alert("Por favor, ingresa un nombre de usuario válido.");
      }
    });
  }
});