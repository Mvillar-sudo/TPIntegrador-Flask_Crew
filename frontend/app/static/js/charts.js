document.addEventListener("DOMContentLoaded", function () {
    
    const metricElements = document.querySelectorAll(".metric-number");
    
    
    let datosPlatos = HISTORIAL_INICIAL.platos || [metricElements[0] ? parseInt(metricElements[0].innerText) : 0];
    let datosReservas = HISTORIAL_INICIAL.reservas || [metricElements[1] ? parseInt(metricElements[1].innerText) : 0];
    let datosServicios = HISTORIAL_INICIAL.servicios || [metricElements[2] ? parseInt(metricElements[2].innerText) : 0];
    let tiempos = HISTORIAL_INICIAL.tiempos || [new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })];

   
    const options = {
        series: [
            { name: "Platos Activos", data: datosPlatos },
            { name: "Reservas Pendientes", data: datosReservas },
            { name: "Servicios Activos", data: datosServicios }
        ],
        chart: {
            id: 'realtime-dashboard',
            height: 350,
            type: 'line',
            animations: {
                enabled: true,
                easing: 'linear',
                dynamicAnimation: { speed: 1000 }
            },
            toolbar: { show: false }
        },
        colors: ['#28a745', '#ffc107', '#17a2b8'],
        stroke: { curve: 'smooth', width: 3 },
        markers: { size: 4 },
        xaxis: {
            categories: tiempos,
            title: { text: 'Historial de Actualizaciones (Tiempo Real)' }
        },
        yaxis: { title: { text: 'Cantidad' }, min: 0 }
    };

    const chart = new ApexCharts(document.querySelector("#chart-lineas-dashboard"), options);
    chart.render();

    
    setInterval(function () {
        
        fetch(URL_METRICAS_VIVO) 
            .then(response => response.json())
            .then(data => {
                if (metricElements[0]) metricElements[0].innerText = data.actual.platos;
                if (metricElements[1]) metricElements[1].innerText = data.actual.reservas;
                if (metricElements[2]) metricElements[2].innerText = data.actual.servicios;

                datosPlatos = data.historial.platos;
                datosReservas = data.historial.reservas;
                datosServicios = data.historial.servicios;
                tiempos = data.historial.tiempos;

                chart.updateSeries([
                    { 
                        name: "Platos Activos", 
                        data: datosPlatos 
                    },
                    { 
                        name: "Reservas Pendientes", 
                        data: datosReservas 
                    },
                    { 
                        name: "Servicios Activos", 
                        data: datosServicios 
                    }
                ]);
                
                
                chart.updateOptions({
                    xaxis: { categories: tiempos }
                });
            })
            .catch(error => console.error("Error obteniendo métricas:", error));

    }, 10000);

});