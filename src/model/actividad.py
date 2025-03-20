
class Actividad:
    def __init__(self, db):
        pass
    
    def registrar_actividad(self, fecha, supervisor, descripcion, anexos, responsable, clima):
        pass
    
    def consultar_actividades(self, fecha_inicio, fecha_fin):
        pass
    
    def generar_reporte(self, fecha_inicio, fecha_fin, archivo_pdf="reporte.pdf"):
        pass

from .errores import CamposVaciosError, FechaInvalidaError, RangoFechasInvalidoError
from datetime import datetime

class Actividad:
    def __init__(self, db):
        self.db = db
    
    def registrar_actividad(self, fecha, supervisor, descripcion, anexos, responsable, clima):
        if not fecha or not supervisor or not descripcion or not responsable:
            raise CamposVaciosError()
        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()
        
        query = "INSERT INTO actividades (fecha, supervisor, descripcion, anexos, responsable, clima) VALUES (?, ?, ?, ?, ?, ?)"
        params = (fecha, supervisor, descripcion, anexos, responsable, clima)
        self.db.execute_query(query, params)
    
    def consultar_actividades(self, fecha_inicio, fecha_fin):
        if not fecha_inicio or not fecha_fin:
            raise FechaInvalidaError("Las fechas no pueden estar vacías.")
        
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError()
        
        if fecha_inicio_dt > fecha_fin_dt:
            raise RangoFechasInvalidoError("La fecha de inicio no puede ser mayor que la fecha de fin.")
        
        query = "SELECT * FROM actividades WHERE fecha BETWEEN ? AND ?"
        params = (fecha_inicio, fecha_fin)
        return self.db.fetch_query(query, params)
    
    def generar_reporte(self, fecha_inicio, fecha_fin, archivo_pdf="reporte.pdf"):
        actividades = self.consultar_actividades(fecha_inicio, fecha_fin)
        if not actividades:
            return False
        # Lógica para generar el PDF (omitida por simplicidad)
        return True

