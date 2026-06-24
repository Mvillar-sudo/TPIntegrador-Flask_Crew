document.addEventListener("DOMContentLoaded", function () {
    
    if (document.getElementById("reader")) {
        
        let scanner = new Html5QrcodeScanner("reader", { 
            fps: 10,       
            qrbox: 250   
        });

        scanner.render(function(qrData) {
            scanner.clear(); 

            let id_reserva, qr_code;
            
            try {
                const data = JSON.parse(qrData);
                id_reserva = data.id_reserva;
                qr_code = data.qr_code;
                
            } catch (e) {
                const divResultado = document.getElementById('resultado');
                const mensajeResultado = document.getElementById('resultado-mensaje');
                
                if (divResultado && mensajeResultado) {
                    divResultado.style.display = 'block';
                    divResultado.classList.add('qr-result-error'); // Aplicamos clase CSS externa
                    mensajeResultado.textContent = '✗ QR inválido o mal formado';
                }
                return;
            }

            window.location.href = `${URL_VALIDAR_QR}?id_reserva=${id_reserva}&qr_code=${qr_code}`;
        });
    }
});