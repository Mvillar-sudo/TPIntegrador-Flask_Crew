document.addEventListener("DOMContentLoaded", () => {
    const formulariosEliminar = document.querySelectorAll(".form-eliminar");
    formulariosEliminar.forEach(form => {
        form.addEventListener("submit", (e) => {
            const tipoElemento = form.getAttribute("data-nombre") || "este elemento";
            
            if (!confirm(`¿Estás seguro de que deseas eliminar ${tipoElemento}?`)) {
                e.preventDefault();
            }
        });
    });
});