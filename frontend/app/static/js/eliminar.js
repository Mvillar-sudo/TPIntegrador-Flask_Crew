document.addEventListener("DOMContentLoaded", () => {
    const formulariosEliminar = document.querySelectorAll(".form-eliminar");
    formulariosEliminar.forEach(form => {
        form.addEventListener("submit", (e) => {
            if (!confirm("¿Estás seguro de que deseas eliminar este plato?")) {
                e.preventDefault();
            }
        });
    });
});