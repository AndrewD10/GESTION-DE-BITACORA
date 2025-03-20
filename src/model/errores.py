class BaseError(Exception):
    """Clase base para los errores personalizados."""
    pass

class CamposVaciosError(BaseError):
    """Se genera cuando un campo obligatorio está vacío."""
    def __init__(self, mensaje="Los campos no pueden estar vacíos."):
        super().__init__(mensaje)

class UsuarioNoEncontradoError(BaseError):
    """Se genera cuando un usuario no existe en la base de datos."""
    def __init__(self, mensaje="El usuario no existe."):
        super().__init__(mensaje)

class ContrasenaIncorrectaError(BaseError):
    """Se genera cuando la contraseña ingresada es incorrecta."""
    def __init__(self, mensaje="Contraseña incorrecta."):
        super().__init__(mensaje)

class CorreoYaRegistradoError(BaseError):
    """Se genera cuando se intenta registrar un usuario con un correo ya existente."""
    def __init__(self, mensaje="El correo ya está registrado."):
        super().__init__(mensaje)

class FechaInvalidaError(BaseError):
    """Se genera cuando se ingresa una fecha con formato incorrecto."""
    def __init__(self, mensaje="La fecha ingresada no es válida."):
        super().__init__(mensaje)

class RangoFechasInvalidoError(BaseError):
    """Se genera cuando el rango de fechas ingresado no es válido (ej. fecha de inicio mayor que fecha de fin)."""
    def __init__(self, mensaje="El rango de fechas es inválido."):
        super().__init__(mensaje)

class ReporteError(BaseError):
    """Se genera cuando hay un problema al generar el reporte."""
    def __init__(self, mensaje="No se pudo generar el reporte."):
        super().__init__(mensaje)
