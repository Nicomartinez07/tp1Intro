import db
from datetime import datetime

def seed_data():
    conn = None
    try:
        conn = db.get_connection()
        cur = conn.cursor(dictionary=True)

        print("Limpiando datos existentes...")
        # El ON DELETE CASCADE en tu schema se encarga de limpiar resultados y predicciones
        cur.execute("DELETE FROM usuarios")
        cur.execute("DELETE FROM partidos")

        # 1. Insertar Usuarios
        usuarios_data = [
            ('Nicolas', 'nicolas@uba.ar'),
            ('Lionel', 'leo@seleccion.ar'),
            ('Julian', 'spider@manchester.uk')
        ]
        query_user = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
        cur.executemany(query_user, usuarios_data)
        
        # Obtenemos los IDs generados
        cur.execute("SELECT id, nombre FROM usuarios")
        users = {row['nombre']: row['id'] for row in cur.fetchall()}

        # 2. Insertar Partidos
        # Formato: (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase)
        partidos_data = [
            ('Argentina', 'Arabia Saudita', 'MetLife Stadium', 'New Jersey', '2026-06-11 15:00:00', 'Fase de Grupos'),
            ('México', 'Polonia', 'Estadio Azteca', 'Ciudad de México', '2026-06-11 18:00:00', 'Fase de Grupos'),
            ('Francia', 'Australia', 'BC Place', 'Vancouver', '2026-06-12 16:00:00', 'Fase de Grupos'),
            ('Estados Unidos', 'Marruecos', 'SoFi Stadium', 'Los Angeles', '2026-06-12 19:00:00', 'Fase de Grupos'),
            ('España', 'Costa Rica', 'Hard Rock Stadium', 'Miami', '2026-06-13 13:00:00', 'Fase de Grupos'),
            ('Alemania', 'Japón', 'NRG Stadium', 'Houston', '2026-06-13 16:00:00', 'Fase de Grupos'),
            ('Bélgica', 'Canadá', 'BMO Field', 'Toronto', '2026-06-13 20:00:00', 'Fase de Grupos'),
            ('Brasil', 'Serbia', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-14 15:00:00', 'Fase de Grupos'),
            ('Portugal', 'Ghana', 'Gillette Stadium', 'Boston', '2026-06-14 18:00:00', 'Fase de Grupos'),
            ('Uruguay', 'Corea del Sur', 'Lincoln Financial Field', 'Philadelphia', '2026-06-14 21:00:00', 'Fase de Grupos'),
            ('Inglaterra', 'Irán', 'Levi\'s Stadium', 'Santa Clara', '2026-06-15 14:00:00', 'Fase de Grupos'),
            ('Países Bajos', 'Senegal', 'Arrowhead Stadium', 'Kansas City', '2026-06-15 17:00:00', 'Fase de Grupos'),
            ('Suiza', 'Camerún', 'Lumen Field', 'Seattle', '2026-06-15 20:00:00', 'Fase de Grupos'),
            ('Croacia', 'Marruecos', 'AT&T Stadium', 'Arlington', '2026-06-16 13:00:00', 'Fase de Grupos'),
            ('Dinamarca', 'Túnez', 'Akron Stadium', 'Guadalajara', '2026-06-16 16:00:00', 'Fase de Grupos'),
            ('Argentina', 'México', 'Estadio Azteca', 'Ciudad de México', '2026-06-20 20:00:00', 'Fase de Grupos'),
            ('España', 'Alemania', 'MetLife Stadium', 'New Jersey', '2026-06-21 20:00:00', 'Fase de Grupos'),
            ('Francia', 'Dinamarca', 'SoFi Stadium', 'Los Angeles', '2026-06-21 17:00:00', 'Fase de Grupos'),
            ('Brasil', 'Suiza', 'Hard Rock Stadium', 'Miami', '2026-06-22 19:00:00', 'Fase de Grupos'),
            ('Portugal', 'Uruguay', 'NRG Stadium', 'Houston', '2026-06-22 16:00:00', 'Fase de Grupos'),
            ('Polonia', 'Argentina', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-25 20:00:00', 'Fase de Grupos'),
            ('Canadá', 'Marruecos', 'BMO Field', 'Toronto', '2026-06-26 15:00:00', 'Fase de Grupos'),
            ('Ghana', 'Uruguay', 'Gillette Stadium', 'Boston', '2026-06-26 18:00:00', 'Fase de Grupos'),
            ('Camerún', 'Brasil', 'Lincoln Financial Field', 'Philadelphia', '2026-06-27 19:00:00', 'Fase de Grupos'),
            ('Japón', 'España', 'BC Place', 'Vancouver', '2026-06-27 16:00:00', 'Fase de Grupos')
        ]
        query_partido = """
            INSERT INTO partidos (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.executemany(query_partido, partidos_data)

        # Obtenemos los IDs de los partidos
        cur.execute("SELECT id, equipo_local FROM partidos")
        matches = {row['equipo_local']: row['id'] for row in cur.fetchall()}

        # 3. Insertar Resultados Reales
        # (partido_id, goles_local, goles_visitante)
        resultados_data = [
            (matches['Argentina'], 1, 2), # Perdió el local
            (matches['México'], 0, 0),    # Empate
            (matches['Francia'], 4, 1)    # Ganó el local
        ]
        cur.executemany("INSERT INTO resultados (partido_id, goles_local, goles_visitante) VALUES (%s, %s, %s)", resultados_data)

        # 4. Insertar Predicciones (Aquí es donde testeamos tu lógica de puntos)
        # Nicolas: Pega el resultado exacto (3 pts) y un ganador (1 pt)
        # Lionel: Pega dos ganadores (2 pts)
        predicciones_data = [
            # Nicolas
            (users['Nicolas'], matches['Argentina'], 1, 2), # Exacto: 3pts
            (users['Nicolas'], matches['México'], 1, 1),    # Erró: 0pts (Era 0-0, pero SIGN es igual, así que sumaría 1pt por empate)
            
            # Lionel
            (users['Lionel'], matches['Argentina'], 0, 1),  # Ganador correcto: 1pt
            (users['Lionel'], matches['Francia'], 2, 0)     # Ganador correcto: 1pt
        ]
        query_pred = """
            INSERT INTO predicciones (usuario_id, partido_id, prediccion_local, prediccion_visitante) 
            VALUES (%s, %s, %s, %s)
        """
        cur.executemany(query_pred, predicciones_data)

        conn.commit()
        print("¡Seed finalizado con éxito!")
        print(f"Usuarios creados: {len(usuarios_data)}")
        print(f"Partidos creados: {len(partidos_data)}")

    except Exception as e:
        print(f"Error al cargar el seed: {e}")
        if conn: conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    seed_data()