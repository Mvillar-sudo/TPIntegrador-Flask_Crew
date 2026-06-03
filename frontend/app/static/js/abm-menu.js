const modal = document.getElementById('platoModal');
    const form = document.getElementById('platoForm');
    const modalTitle = document.getElementById('modalTitle');

    // Abre el modal configurado para CREAR (Alta)
    function abrirModalCrear() {
        modalTitle.textContent = "Agregar Nuevo Plato";
        form.reset();
        document.getElementById('plato_id').value = "";
        document.getElementById('estadoContainer').style.display = "none"; // Nace activo por defecto
        modal.showModal();
    }

    // Abre el modal configurado para EDITAR (Modificación)
    function abrirModalEditar(id, nombre, descripcion, precio, activo) {
        modalTitle.textContent = "Editar Plato";
        form.reset();
        document.getElementById('plato_id').value = id;
        document.getElementById('modal_nombre').value = nombre;
        document.getElementById('modal_descripcion').value = descripcion;
        document.getElementById('modal_precio').value = precio;
        
        // Ajustamos el checkbox según el estado que viene de la base de datos
        document.getElementById('modal_activo').checked = (activo === 'True' || activo === true);
        document.getElementById('estadoContainer').style.display = "block"; // Permite activar/desactivar
        modal.showModal();
    }

    // Cierra el modal
    function cerrarModal() {
        modal.close();
    }

    // 1. CREAR O MODIFICAR DATOS DEL PLATO
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const id = document.getElementById('plato_id').value;
        let url = '/admin/menu';
        let method = 'POST';
        
        // Estructura de datos base para enviar al request.json
        const datos = {
            nombre: document.getElementById('modal_nombre').value,
            descripcion: document.getElementById('modal_descripcion').value,
            precio: parseFloat(document.getElementById('modal_precio').value)
        };

        // Si hay un ID presente, cambiamos la estrategia a una actualización (PATCH)
        if (id) {
            url = `/admin/menu/${id}`;
            method = 'PATCH'; // Adaptado a tu ruta @admin_menu_bp.route("/admin/menu/<id>", methods=["PATCH"])
        }

        fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(res => {
            if (res.ok) {
                // Si la actualización de datos fue exitosa e implica un cambio de estado, lo procesamos seguido
                if (id) {
                    const nuevoEstado = document.getElementById('modal_activo').checked;
                    actualizarEstadoPlato(id, nuevoEstado);
                } else {
                    window.location.reload();
                }
            } else {
                return res.json().then(err => { alert(`Error: ${err.mensaje}`); });
            }
        })
        .catch(err => alert("Ocurrió un error en la comunicación con el servidor."));
    });

    // 2. CAMBIAR VISIBILIDAD / ESTADO (PATCH)
    // Adaptado a: @admin_menu_bp.route("/admin/menu/<id>/estado", methods=["PATCH"])
    function actualizarEstadoPlato(id, estadoBool) {
        fetch(`/admin/menu/${id}/estado`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ estado: estadoBool }) // Tu backend espera: data["estado"]
        })
        .then(res => {
            if (res.ok) {
                window.location.reload();
            } else {
                return res.json().then(err => { alert(`Error al actualizar estado: ${err.mensaje}`); });
            }
        });
    }

    // 3. ELIMINAR PLATO DEFINITIVAMENTE (DELETE)
    // Adaptado a: @admin_menu_bp.route("/admin/menu/<id>", methods=["DELETE"])
    function eliminarPlato(id) {
        if (confirm("¿Estás seguro de que deseas eliminar permanentemente este plato de la base de datos?")) {
            fetch(`/admin/menu/${id}`, {
                method: 'DELETE'
            })
            .then(res => {
                if (res.ok) {
                    window.location.reload();
                } else {
                    return res.json().then(err => { alert(`Error: ${err.mensaje}`); });
                }
            })
            .catch(err => alert("No se pudo procesar la eliminación."));
        }
    }