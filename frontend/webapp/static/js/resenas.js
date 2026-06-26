document.addEventListener("DOMContentLoaded", function () {
    const reviewForm = document.querySelector(".review-form");

    if (reviewForm) {
        reviewForm.addEventListener("submit", function (e) {
            const comentario = document.querySelector("#comentario").value.trim();

            if (comentario.length < 10) {
                e.preventDefault();
                alert("¡Por favor, cuéntanos un poco más! Tu opinión debe tener al menos 10 caracteres.");
            }
        });
    }
});