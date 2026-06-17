const modal = document.getElementById('platoModal');
const form = document.getElementById('platoForm');
const modalTitle = document.getElementById('modalTitle');

function abrirModalCrear() {
    modalTitle.textContent = "Agregar Nuevo Plato";
    form.reset();
    document.getElementById('plato_id').value = "";
    document.getElementById('estadoContainer').style.display = "none";
    modal.showModal();
}

function abrirModalEditar(id, nombre_plato, descripcion, precio, activo) {
    modalTitle.textContent = "Editar Plato";
    form.reset();
    document.getElementById('plato_id').value = id;
    document.getElementById('modal_nombre').value = nombre_plato;
    document.getElementById('modal_descripcion').value = descripcion;
    document.getElementById('modal_precio').value = precio;

    // Verificamos si viene como string 'True', '1', o directamente un booleano
    document.getElementById('modal_activo').checked = (activo === 'True' || activo === true || activo === 1);
    document.getElementById('estadoContainer').style.display = "block";
    modal.showModal();
}

function cerrarModal() {
    modal.close();
}

form.addEventListener('submit', function(e) {
    e.preventDefault();

    const id = document.getElementById('plato_id').value;
    let url = '/admin/menu';
    let method = 'POST';

    const datos = {
        nombre_plato: document.getElementById('modal_nombre').value,
        descripcion: document.getElementById('modal_descripcion').value,
        precio: parseFloat(document.getElementById('modal_precio').value)
    };

    if (id) {
        url = `/admin/menu/${id}`;
        method = 'PATCH';
    }

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    })
    .then(res => {
        if (res.ok) {
            if (id) {
                const nuevoEstado = document.getElementById('modal_activo').checked;
                actualizarEstadoPlato(id, nuevoEstado ? 1 : 0);
            } else {
                window.location.reload();
            }
        } else {
            return res.json().then(err => { alert(`Error: ${err.mensaje || 'Error desconocido'}`); });
        }
    })
    .catch(err => alert("Ocurrió un error en la comunicación con el servidor."));
});

function actualizarEstadoPlato(id, estadoBool) {
    fetch(`/admin/menu/${id}/estado`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ activo: estadoBool })
    })
    .then(res => {
        if (res.ok) {
            window.location.reload();
        } else {
            return res.json().then(err => { alert(`Error al actualizar estado: ${err.mensaje || ''}`); });
        }
    });
}

function eliminarPlato(id) {
    if (confirm("¿Estás seguro de que deseas eliminar permanentemente este plato de la base de datos?")) {
        fetch(`/admin/menu/${id}`, {
            method: 'DELETE'
        })
        .then(res => {
            if (res.ok) {
                window.location.reload();
            } else {
                return res.json().then(err => { alert(`Error: ${err.mensaje || ''}`); });
            }
        })
        .catch(err => alert("No se pudo procesar la eliminación."));
    }
}