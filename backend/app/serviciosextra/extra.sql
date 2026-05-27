-- Estructura para la tabla de servicios extras
CREATE TABLE IF NOT EXISTS servicios_extras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    disponible BOOLEAN DEFAULT TRUE
);

-- Datos de carga inicial para probar el sistema
INSERT INTO servicios_extras (nombre, descripcion) VALUES 
('Estacionamiento Privado', 'Estacionamiento vigilado incluido con la reserva.'),
('Acceso Adaptado', 'Rampas y espacios para sillas de ruedas.');
