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
        altInput: true,          
        dateFormat: "Y-m-d",      
        altFormat: "d/m/Y",     
        disable: [
            function(date) { return (date.getDay() === 0); } 
        ]
    });
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        console.log("Enviando reserva...");
    });
});