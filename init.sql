--tabla de autenticacion/login del administrador
CREATE TABLE login (
    id_admin INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    contraseña VARCHAR(50),
    rol VARCHAR(50)
);

INSERT INTO login 
	(usuario, contraseña, rol)
VALUES
	('Menendez', '81010', 'administrador'),
    ('Murphy', '97616', 'administrador'),
    ('Shepherd', '56162', 'administrador');


--tabla menu
CREATE TABLE menu (
	id_plato INT AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10,2),
    estado BOOLEAN
);


