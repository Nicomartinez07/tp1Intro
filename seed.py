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

        # 1. Insertar 15 Usuarios
        usuarios_data = [
            ('Nicolas', 'nicolas@uba.ar'),
            ('Lionel', 'leo@seleccion.ar'),
            ('Julian', 'spider@manchester.uk'),
            ('Emiliano', 'dibu@astonvilla.uk'),
            ('Angel', 'fideo@rosario.ar'),
            ('Rodrigo', 'motor@atletico.es'),
            ('Enzo', 'enzo@chelsea.uk'),
            ('Alexis', 'maca@liverpool.uk'),
            ('Cristian', 'cuti@tottenham.uk'),
            ('Nahuel', 'molina@atletico.es'),
            ('Lisandro', 'licha@manchester.uk'),
            ('Gonzalo', 'montiel@sevilla.es'),
            ('Lautaro', 'toro@inter.it'),
            ('Paulo', 'joya@roma.it'),
            ('Alejandro', 'garna@manchester.uk')
        ]
        query_user = "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"
        cur.executemany(query_user, usuarios_data)
        
        # Obtenemos los IDs generados
        cur.execute("SELECT id, nombre FROM usuarios")
        users = {row['nombre']: row['id'] for row in cur.fetchall()}

        # 2. Insertar Partidos
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
            ('Uruguay', 'Corea del Sur', 'Lincoln Financial Field', 'Philadelphia', '2026-06-14 21:00:00', 'Fase de Grupos')
        ]
        query_partido = """
            INSERT INTO partidos (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.executemany(query_partido, partidos_data)

        # Obtenemos los IDs de los partidos
        cur.execute("SELECT id, equipo_local FROM partidos")
        matches = {row['equipo_local']: row['id'] for row in cur.fetchall()}

        # 3. Insertar Resultados Reales (7 resultados)
        resultados_data = [
            (matches['Argentina'], 1, 2),       # Perdió el local
            (matches['México'], 0, 0),          # Empate
            (matches['Francia'], 4, 1),         # Ganó el local
            (matches['Estados Unidos'], 2, 0),  # Ganó el local
            (matches['España'], 7, 0),          # Ganó el local
            (matches['Alemania'], 1, 2),        # Perdió el local
            (matches['Brasil'], 2, 0)           # Ganó el local
        ]
        cur.executemany("INSERT INTO resultados (partido_id, goles_local, goles_visitante) VALUES (%s, %s, %s)", resultados_data)

        # 4. Insertar Predicciones para variar el ranking
        predicciones_data = [
            # Nicolas: 5 puntos
            (users['Nicolas'], matches['Argentina'], 1, 2), # Exacto (3)
            (users['Nicolas'], matches['México'], 1, 1),    # Diferencia/Empate (1)
            (users['Nicolas'], matches['Francia'], 2, 0),   # Ganador (1)
            
            # Lionel: 7 puntos
            (users['Lionel'], matches['Argentina'], 2, 0),  # Nada (0)
            (users['Lionel'], matches['México'], 0, 0),     # Exacto (3)
            (users['Lionel'], matches['Francia'], 3, 1),    # Ganador (1)
            (users['Lionel'], matches['Brasil'], 2, 0),     # Exacto (3)

            # Julian: 4 puntos
            (users['Julian'], matches['Argentina'], 3, 0),  # Nada (0)
            (users['Julian'], matches['Francia'], 4, 1),    # Exacto (3)
            (users['Julian'], matches['España'], 2, 0),     # Ganador (1)

            # Emiliano: 7 puntos (Empatado con Lionel)
            (users['Emiliano'], matches['México'], 1, 0),   # Nada (0)
            (users['Emiliano'], matches['Estados Unidos'], 2, 0), # Exacto (3)
            (users['Emiliano'], matches['Brasil'], 3, 0),   # Ganador (1)
            (users['Emiliano'], matches['Alemania'], 1, 2), # Exacto (3)

            # Angel: 3 puntos
            (users['Angel'], matches['Francia'], 1, 1),     # Nada (0)
            (users['Angel'], matches['España'], 7, 0),      # Exacto (3)
            (users['Angel'], matches['Alemania'], 2, 1),    # Nada (0)

            # Rodrigo: 12 puntos (Líder del ranking)
            (users['Rodrigo'], matches['Argentina'], 1, 2), # Exacto (3)
            (users['Rodrigo'], matches['México'], 0, 0),    # Exacto (3)
            (users['Rodrigo'], matches['Francia'], 4, 1),   # Exacto (3)
            (users['Rodrigo'], matches['Estados Unidos'], 2, 0), # Exacto (3)

            # Enzo: 0 puntos (Último lugar)
            (users['Enzo'], matches['Brasil'], 1, 1),       # Nada (0)
            (users['Enzo'], matches['Alemania'], 1, 0),     # Nada (0)
            (users['Enzo'], matches['Estados Unidos'], 1, 1), # Nada (0)

            # Alexis: 3 puntos
            (users['Alexis'], matches['España'], 3, 0),     # Ganador (1)
            (users['Alexis'], matches['Brasil'], 1, 0),     # Ganador (1)
            (users['Alexis'], matches['Francia'], 2, 1),    # Ganador (1)

            # Cristian: 7 puntos
            (users['Cristian'], matches['Alemania'], 1, 2), # Exacto (3)
            (users['Cristian'], matches['Argentina'], 1, 2),# Exacto (3)
            (users['Cristian'], matches['México'], 2, 2),   # Diferencia/Empate (1)

            # Nahuel: 3 puntos
            (users['Nahuel'], matches['Estados Unidos'], 3, 0), # Ganador (1)
            (users['Nahuel'], matches['España'], 4, 0),         # Ganador (1)
            (users['Nahuel'], matches['Brasil'], 2, 1),         # Ganador (1)

            # Lisandro: 0 puntos
            (users['Lisandro'], matches['Argentina'], 2, 1),# Nada (0)
            (users['Lisandro'], matches['México'], 0, 1),   # Nada (0)
            (users['Lisandro'], matches['Francia'], 0, 2),  # Nada (0)

            # Gonzalo: 12 puntos (Empatado en el liderazgo)
            (users['Gonzalo'], matches['España'], 7, 0),    # Exacto (3)
            (users['Gonzalo'], matches['Brasil'], 2, 0),    # Exacto (3)
            (users['Gonzalo'], matches['Alemania'], 1, 2),  # Exacto (3)
            (users['Gonzalo'], matches['Estados Unidos'], 2, 0), # Exacto (3)

            # Lautaro: 4 puntos
            (users['Lautaro'], matches['México'], 0, 0),    # Exacto (3)
            (users['Lautaro'], matches['Francia'], 1, 0),   # Ganador (1)

            # Paulo: 0 puntos
            (users['Paulo'], matches['Argentina'], 0, 0),   # Nada (0)
            (users['Paulo'], matches['Alemania'], 0, 0),    # Nada (0)
            (users['Paulo'], matches['Brasil'], 0, 0),      # Nada (0)

            # Alejandro: 5 puntos
            (users['Alejandro'], matches['Estados Unidos'], 2, 0), # Exacto (3)
            (users['Alejandro'], matches['España'], 2, 0),         # Ganador (1)
            (users['Alejandro'], matches['Brasil'], 3, 1),         # Ganador (1)
            (users['Alejandro'], matches['Alemania'], 1, 1)        # Nada (0)
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
        print(f"Resultados creados: {len(resultados_data)}")
        print(f"Predicciones creadas: {len(predicciones_data)}")

    except Exception as e:
        print(f"Error al cargar el seed: {e}")
        if conn: conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    seed_data()