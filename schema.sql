CREATE DATABASE IF NOT EXISTS prode_mundial_2026;
USE prode_mundial_2026;

CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE partidos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    estadio VARCHAR(100),
    ciudad VARCHAR(100),
    fecha DATETIME NOT NULL,
    fase VARCHAR(50) NOT NULL
);

CREATE TABLE resultados (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    partido_id INT NOT NULL UNIQUE, 
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE
);

CREATE TABLE predicciones (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    prediccion_local INT NOT NULL,
    prediccion_visitante INT NOT NULL,
    
    UNIQUE KEY unica_prediccion (usuario_id, partido_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE
);

