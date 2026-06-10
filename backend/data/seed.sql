USE tpintegrador_db;

-- 1. Insertar usuario admin por defecto: email: admin@mail.com, password: admin123
INSERT INTO usuarios (nombre, email, password, activo)
VALUES (
    'Administrador', 
    'admin@mail.com', 
    'scrypt:32768:8:1$l6kgtPhOrNo39H5G$523d6119731120cdcc7699c7a2a0e7ee1a5fa33966cb78b7fb681a3f91b8add05a98009b7699a74cdaef6e1932add28f369d4e7c72ebfa29abb99797958db860', 
    TRUE
) ON DUPLICATE KEY UPDATE email=email;

-- 2. Insertar servicios iniciales
INSERT INTO servicios (nombre, activo) VALUES
('Estacionamiento', TRUE),
('Acceso para personas con movilidad reducida', TRUE),
('Wifi Gratis', TRUE),
('Espacio al aire libre', TRUE)
ON DUPLICATE KEY UPDATE nombre=nombre;

-- 3. Insertar platillos iniciales del menú (productos)
INSERT INTO men8u (nombre, precio, descripcion, activo, imagen) VALUES
('Pizza Napolitana', 12500.00, 'Pizza con mozzarella, rodajas de tomate, ajo y albahaca fresca.', TRUE, 'https://www.recetasnestlecam.com/sites/default/files/styles/recipe_detail_desktop_new/public/srh_recipes/017845e65b2068a168e87a38f0722a75.jpg?itok=2bgODUGg'),
('Milanesa con Papas Fritas', 11000.00, 'Clásica milanesa de carne acompañada de papas fritas crujientes.', TRUE, 'https://www.recetasnestlecam.com/sites/default/files/styles/recipe_detail_desktop_new/public/srh_recipes/017845e65b2068a168e87a38f0722a75.jpg?itok=2bgODUGg'),
('Hamburguesa Completa', 9500.00, 'Hamburguesa casera con queso, lechuga, tomate, huevo y jamón, con papas.', TRUE, 'https://www.recetasnestlecam.com/sites/default/files/styles/recipe_detail_desktop_new/public/srh_recipes/017845e65b2068a168e87a38f0722a75.jpg?itok=2bgODUGg'),
('Ensalada César', 8500.00, 'Lettuce romana, croutons, queso parmesano y aderezo César.', TRUE, 'https://www.recetasnestlecam.com/sites/default/files/styles/recipe_detail_desktop_new/public/srh_recipes/017845e65b2068a168e87a38f0722a75.jpg?itok=2bgODUGg'),
('Tiramisú', 4500.00, 'Postre clásico italiano con café y mascarpone.', TRUE, 'https://www.recetasnestlecam.com/sites/default/files/styles/recipe_detail_desktop_new/public/srh_recipes/017845e65b2068a168e87a38f0722a75.jpg?itok=2bgODUGg')
ON DUPLICATE KEY UPDATE nombre=nombre;
