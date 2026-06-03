document.addEventListener("DOMContentLoaded", function() {
            let horasDeshabilitadas = [];

            const horaPicker = flatpickr("#reserva-hora", {
                enableTime: true,
                noCalendar: true,
                dateFormat: "H:i",
                time_24hr: true,
                minTime: "12:30",
                maxTime: "23:00",
                minuteIncrement: 30,
                disable: [
                    function(time) {
                        const horaStr = time.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
                        return horasDeshabilitadas.includes(horaStr);
                    }
                ]
            });

            const fechaPicker = flatpickr("#reserva-fecha", {
                locale: "es",
                minDate: "today",
                dateFormat: "Y-m-d",
                disable: [
                    function(date) { return (date.getDay() === 7); } // Domingo cerrado
                ],
                onChange: function(selectedDates, dateStr) {
                    if (!dateStr) return;

                    fetch(`/api/reservas/horas-ocupadas?fecha=${dateStr}`)
                        .then(response => response.json())
                        .then(horasLlenas => {
                            horasDeshabilitadas = horasLlenas; 
                            
                            horaPicker.clear();
                            horaPicker.set("disabled", false); 
                            horaPicker.redraw();
                        })
                        .catch(err => console.error("Error buscando disponibilidad:", err));
                }
            });

            const form = document.querySelector('form[action*="landing"]');
            form.addEventListener('submit', function(e) {
                e.preventDefault(); 

                const datosReserva = {
                    nombre: document.getElementById('name').value,
                    email: document.getElementById('Email').value,
                    fecha: document.getElementById('reserva-fecha').value,
                    hora: document.getElementById('reserva-hora').value,
                    cantidad_personas: parseInt(document.getElementById('activities').value)
                };

                fetch('/api/reservas/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datosReserva)
                })
                .then(res => {
                    if (res.status === 201) {
                        alert("¡Reserva creada con éxito! Revisa tu correo.");
                        form.reset();
                        horaPicker.set("disabled", true);
                    } else {
                        return res.json().then(data => { alert(`Error: ${data.mensaje}`); });
                    }
                })
                .catch(err => alert("Ocurrió un error al procesar la reserva."));
            });
        });