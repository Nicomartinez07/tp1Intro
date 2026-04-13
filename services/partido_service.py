from datetime import datetime
import repositories.partido_repository as db

def obtener_partidos(equipo=None, fecha=None, fase=None):

    if fecha:
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha inválida. El formato debe ser YYYY-MM-DD.")
    
    return db.obtener_partidos(equipo, fecha, fase)