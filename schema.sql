CREATE DATABASE IF NOT EXISTS prode_mundial_2026;
USE prode_mundial_2026;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    estadio VARCHAR(100),
    ciudad VARCHAR(100),
    fecha DATETIME NOT NULL,
    fase VARCHAR(50) NOT NULL
);

CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    partido_id INT NOT NULL UNIQUE, 
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_resultado_partido FOREIGN KEY (partido_id) 
        REFERENCES partidos(id) ON DELETE CASCADE
);

CREATE TABLE predicciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    prediccion_local INT NOT NULL,
    prediccion_visitante INT NOT NULL,
    
    UNIQUE KEY unica_prediccion (usuario_id, partido_id),
    CONSTRAINT fk_pred_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_pred_partido FOREIGN KEY (partido_id) 
        REFERENCES partidos(id) ON DELETE CASCADE
);