
class Usuario:
    def __init__(self, db):
        pass
    
    def crear_cuenta(self, nombre, correo, contrasena):
        pass
    
    def iniciar_sesion(self, correo, contrasena):
        pass
    
    def cambiar_contrasena(self, correo, nueva_contrasena):
        pass

from .errores import CamposVaciosError, UsuarioNoEncontradoError, ContrasenaIncorrectaError, CorreoYaRegistradoError

class Usuario:
    def __init__(self, db):
        self.db = db
    
    def crear_cuenta(self, nombre, correo, contrasena):
        if not nombre or not correo or not contrasena:
            raise CamposVaciosError()
        # Verificar si el correo ya está registrado
        query = "SELECT * FROM usuarios WHERE correo = ?"
        if self.db.fetch_query(query, (correo,)):
            raise CorreoYaRegistradoError()
        query = "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)"
        params = (nombre, correo, contrasena)
        self.db.execute_query(query, params)
        return True
    
    def iniciar_sesion(self, correo, contrasena):
        if not correo or not contrasena:
            raise CamposVaciosError()
        query = "SELECT * FROM usuarios WHERE correo = ?"
        usuario = self.db.fetch_query(query, (correo,))
        if not usuario:
            raise UsuarioNoEncontradoError()
        if usuario[0][3] != contrasena:
            raise ContrasenaIncorrectaError()
        return usuario[0]
    
    def cambiar_contrasena(self, correo, nueva_contrasena):
        if not correo or not nueva_contrasena:
            raise CamposVaciosError("El correo y la nueva contraseña no pueden estar vacíos.")
        
        query = "SELECT * FROM usuarios WHERE correo = ?"
        usuario = self.db.fetch_query(query, (correo,))
        if not usuario:
            raise UsuarioNoEncontradoError()
        
        if usuario[0][3] == nueva_contrasena:
            raise ValueError("La nueva contraseña no puede ser igual a la anterior.")
        
        query = "UPDATE usuarios SET contrasena = ? WHERE correo = ?"
        params = (nueva_contrasena, correo)
        self.db.execute_query(query, params)
        return True

