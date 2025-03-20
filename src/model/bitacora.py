
class Bitacora:
    def __init__(self, db):
        pass
    
    def agregar_entrada(self, actividad):
        pass
    
    def obtener_entradas(self, fecha_inicio, fecha_fin):
        pass

from .errores import FechaInvalidaError, RangoFechasInvalidoError, ReporteError
from datetime import datetime

class Bitacora:
    def __init__(self, db):
        self.db = db
    
    def agregar_entrada(self, actividad):
        query = "INSERT INTO bitacora (fecha, supervisor, descripcion, anexos, responsable, clima) VALUES (?, ?, ?, ?, ?, ?)"
        params = (actividad.fecha, actividad.supervisor, actividad.descripcion, actividad.anexos, actividad.responsable, actividad.clima)
        try:
            datetime.strptime(actividad.fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()
        self.db.execute_query(query, params)
    
    def obtener_entradas(self, fecha_inicio, fecha_fin):
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()
        
        if fecha_inicio_dt > fecha_fin_dt:
            raise RangoFechasInvalidoError()
        
        query = "SELECT * FROM bitacora WHERE fecha BETWEEN ? AND ?"
        params = (fecha_inicio, fecha_fin)
        return self.db.fetch_query(query, params)
    
    def generar_reporte(self, fecha_inicio, fecha_fin, archivo_pdf="reporte.pdf"):
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")
        
        if not archivo_pdf:
            raise ReporteError("El nombre del archivo no puede estar vacío.")
        
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()
        
        if fecha_inicio_dt > fecha_fin_dt:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")
        
        actividades = self.obtener_entradas(fecha_inicio, fecha_fin)
        
        # Lógica para generar el PDF (omitida por simplicidad)
        try:
            with open(archivo_pdf, 'w') as f:
                f.write("Reporte de actividades\n")
                for actividad in actividades:
                    f.write(f"{actividad}\n")
        except Exception:
            raise ReporteError("No se pudo generar el reporte.")
        
        return True

