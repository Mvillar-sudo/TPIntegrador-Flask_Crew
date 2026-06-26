document.addEventListener("DOMContentLoaded", () => {
    console.log("¡Dashboard JS cargado y escuchando errores de imágenes!");

    document.addEventListener("error", (event) => {
        const elemento = event.target;
        
        if (elemento.tagName === "IMG" && elemento.classList.contains("img-plato-tabla")) {
            elemento.src = "/static/img/img_1.jpg";
            elemento.classList.add("img-placeholder");
        }
    }, true);
});