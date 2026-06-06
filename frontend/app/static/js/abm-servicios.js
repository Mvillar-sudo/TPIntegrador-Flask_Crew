document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('servicioModal');
    const form = document.getElementById('servicioForm');

    window.abrirModalCrear = () => {
        if (form) form.reset();
        if (modal) modal.showModal();
    };

    window.cerrarModal = () => {
        if (modal) modal.close();
    };

    window.alternarEstadoServicio = (idServicio, nuevoEstado) => {
        fetch(`/api/servicios/${idServicio}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ activo: nuevoEstado })
        })
        .then(res => {
            if (res.ok) {
                window.location.reload();
            } else {
                return res.json().then(err => { 
                    alert(`Error al actualizar: ${JSON.stringify(err.errores)}`); 
                });
            }
        })
        .catch(() => alert("Error de comunicación con el servidor."));
    };

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const datos = {
                nombre: document.getElementById('modal_nombre').value,
                descripcion: document.getElementById('modal_descripcion').value
            };

            fetch('/api/servicios', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datos)
            })
            .then(res => {
                if (res.ok) {
                    window.location.reload();
                } else {
                    return res.json().then(err => { 
                        alert(`Error de validación: ${JSON.stringify(err.errores)}`); 
                    });
                }
            })
            .catch(() => alert("Error de comunicación con el servidor."));
        });
    }
});