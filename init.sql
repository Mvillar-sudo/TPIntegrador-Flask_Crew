--tabla de autenticacion/login del administrador (ya se tiene cargada la columna "rol" con "administrador")
CREATE TABLE login (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL
);


--tabla menu
CREATE TABLE menu (
	id_plato INT AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE
);


