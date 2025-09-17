-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS flasklogin CHARACTER SET utf8 COLLATE utf8_general_ci;

-- Usar la base de datos
USE flasklogin;

-- Crear la tabla 'cuentas'
CREATE TABLE IF NOT EXISTS cuentas (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY usuario_UNIQUE (usuario),
    UNIQUE KEY email_UNIQUE (email)
);
