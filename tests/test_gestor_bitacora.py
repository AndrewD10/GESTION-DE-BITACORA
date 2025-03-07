import pytest
from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.database import Database

class TestRegistroActividad:
    def setup_method(self, method):
        """Método de configuración para cada prueba"""
        self.db = Database()
        self.actividad = Actividad(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_registro_actividad_valida(self):
        """Registrar una actividad con datos correctos"""
        self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "Revisión de equipos", "anexo.pdf", "María", "Soleado")
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert len(actividades) == 1
    
    def test_registro_actividad_sin_anexo(self):
        """Registrar una actividad sin archivo adjunto"""
        self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "Limpieza del área", "", "Carlos", "Nublado")
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][3] == "Limpieza del área"
    
    def test_registro_actividad_con_clima_variable(self):
        """Registrar una actividad con una condición climática cambiante"""
        self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "Reparación de equipo", "", "Ana", "Lluvia intermitente")
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][6] == "Lluvia intermitente"
    
    # ---- PRUEBAS EXTREMAS ----
    def test_registro_actividad_fecha_lejana(self):
        """Registrar una actividad con una fecha muy en el futuro"""
        self.actividad.registrar_actividad("2035-12-31", "Juan Pérez", "Mantenimiento futuro", "", "Carlos", "Soleado")
        actividades = self.actividad.consultar_actividades("2035-12-31", "2035-12-31")
        assert len(actividades) == 1
    
    def test_registro_actividad_mucha_info(self):
        """Registrar una actividad con una descripción muy larga"""
        descripcion_larga = "A" * 1000
        self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", descripcion_larga, "", "Ana", "Nublado")
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert len(actividades[0][3]) == 1000
    
    def test_registro_actividad_clima_desconocido(self):
        """Registrar una actividad con un tipo de clima poco común"""
        self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "Tarea de prueba", "", "Luis", "Huracán categoría 5")
        actividades = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert actividades[0][6] == "Huracán categoría 5"
    
    # ---- PRUEBAS DE ERROR ----
    def test_registro_actividad_fecha_invalida(self):
        """Intentar registrar una actividad con una fecha incorrecta"""
        with pytest.raises(ValueError):
            self.actividad.registrar_actividad("fecha_invalida", "Juan Pérez", "Revisión", "", "Pedro", "Soleado")
    
    def test_registro_actividad_sin_descripcion(self):
        """Intentar registrar una actividad sin descripción"""
        with pytest.raises(ValueError):
            self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "", "", "María", "Nublado")
    
    def test_registro_actividad_sin_responsable(self):
        """Intentar registrar una actividad sin responsable asignado"""
        with pytest.raises(ValueError):
            self.actividad.registrar_actividad("2025-03-06", "Juan Pérez", "Reparación", "", "", "Soleado")


class TestConsultarActividades:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.actividad = Actividad(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_consultar_actividades_rango_valido(self):
        """Consultar actividades dentro de un rango de fechas válido"""
        resultado = self.actividad.consultar_actividades("2025-03-01", "2025-03-10")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_sin_resultados(self):
        """Consultar actividades en un rango donde no hay registros"""
        resultado = self.actividad.consultar_actividades("2030-01-01", "2030-01-10")
        assert resultado == []
    
    def test_consultar_actividades_fecha_actual(self):
        """Consultar actividades en la fecha actual"""
        resultado = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert isinstance(resultado, list)
    
    # ---- PRUEBAS EXTREMAS ----
    def test_consultar_actividades_rango_extremadamente_amplio(self):
        """Consultar actividades en un rango de fechas muy amplio"""
        resultado = self.actividad.consultar_actividades("2000-01-01", "2100-12-31")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_mismo_dia(self):
        """Consultar actividades en un solo día"""
        resultado = self.actividad.consultar_actividades("2025-03-06", "2025-03-06")
        assert isinstance(resultado, list)
    
    def test_consultar_actividades_fechas_invertidas(self):
        """Consultar actividades con fechas invertidas (fecha fin antes que fecha inicio)"""
        resultado = self.actividad.consultar_actividades("2025-03-10", "2025-03-01")
        assert resultado == []
    
    # ---- PRUEBAS DE ERROR ----
    def test_consultar_actividades_fechas_invalidas(self):
        """Intentar consultar actividades con fechas inválidas"""
        with pytest.raises(ValueError):
            self.actividad.consultar_actividades("fecha_invalida", "2025-03-06")
    
    def test_consultar_actividades_sin_parametros(self):
        """Intentar consultar actividades sin proporcionar fechas"""
        with pytest.raises(ValueError):
            self.actividad.consultar_actividades("", "")
    
    def test_consultar_actividades_caracteres_especiales(self):
        """Intentar consultar actividades con caracteres especiales en las fechas"""
        with pytest.raises(ValueError):
            self.actividad.consultar_actividades("@#$$%", "2025-03-06")


class TestGenerarReporte:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.actividad = Actividad(self.db)
        self.bitacora = Bitacora(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_generar_reporte_rango_valido(self):
        """Generar un reporte en un rango de fechas válido"""
        resultado = self.bitacora.generar_reporte("2025-03-01", "2025-03-10", "reporte.pdf")
        assert resultado is True
    
    def test_generar_reporte_sin_resultados(self):
        """Generar un reporte en un rango sin actividades registradas"""
        resultado = self.bitacora.generar_reporte("2030-01-01", "2030-01-10", "reporte_vacio.pdf")
        assert resultado is True  # El PDF debe generarse aunque esté vacío
    
    def test_generar_reporte_fecha_actual(self):
        """Generar un reporte con la fecha actual"""
        resultado = self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "reporte_hoy.pdf")
        assert resultado is True
    
    # ---- PRUEBAS EXTREMAS ----
    def test_generar_reporte_rango_extremadamente_amplio(self):
        """Generar un reporte con un rango de fechas muy grande"""
        resultado = self.bitacora.generar_reporte("2000-01-01", "2100-12-31", "reporte_extremo.pdf")
        assert resultado is True
    
    def test_generar_reporte_mismo_dia(self):
        """Generar un reporte con un solo día de rango"""
        resultado = self.bitacora.generar_reporte("2025-03-06", "2025-03-06", "reporte_un_dia.pdf")
        assert resultado is True
    
    def test_generar_reporte_fechas_invertidas(self):
        """Generar un reporte con fechas invertidas (fecha fin antes que fecha inicio)"""
        with pytest.raises(ValueError):
            self.bitacora.generar_reporte("2025-03-10", "2025-03-01", "reporte_error.pdf")
    
    # ---- PRUEBAS DE ERROR ----
    def test_generar_reporte_fechas_invalidas(self):
        """Intentar generar un reporte con fechas inválidas"""
        with pytest.raises(ValueError):
            self.bitacora.generar_reporte("fecha_invalida", "2025-03-06", "reporte_error.pdf")
    
    def test_generar_reporte_sin_parametros(self):
        """Intentar generar un reporte sin proporcionar fechas"""
        with pytest.raises(ValueError):
            self.bitacora.generar_reporte("", "", "reporte_error.pdf")
    
    def test_generar_reporte_nombre_archivo_invalido(self):
        """Intentar generar un reporte con un nombre de archivo inválido"""
        with pytest.raises(ValueError):
            self.bitacora.generar_reporte("2025-03-01", "2025-03-10", "")

class TestCrearCuenta:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.usuario = Usuario(self.db)
    
    # ---- PRUEBAS NORMALES ----
    def test_crear_cuenta_valida(self):
        """Crear una cuenta con datos válidos"""
        resultado = self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "Password123")
        assert resultado is True
    
    def test_crear_cuenta_diferentes_usuarios(self):
        """Crear múltiples cuentas con diferentes usuarios"""
        resultado1 = self.usuario.crear_cuenta("María López", "maria@example.com", "ClaveSegura123")
        resultado2 = self.usuario.crear_cuenta("Carlos Gómez", "carlos@example.com", "OtraClave456")
        assert resultado1 is True and resultado2 is True
    
    def test_crear_cuenta_sin_nombre(self):
        """Crear una cuenta sin proporcionar un nombre"""
        with pytest.raises(ValueError):
            self.usuario.crear_cuenta("", "anonimo@example.com", "Clave123")
    
    # ---- PRUEBAS EXTREMAS ----
    def test_crear_cuenta_nombre_muy_largo(self):
        """Crear una cuenta con un nombre extremadamente largo"""
        nombre_largo = "Juan" * 50
        resultado = self.usuario.crear_cuenta(nombre_largo, "juanlargo@example.com", "Password123")
        assert resultado is True
    
    def test_crear_cuenta_contrasena_muy_larga(self):
        """Crear una cuenta con una contraseña extremadamente larga"""
        contrasena_larga = "A" * 100
        resultado = self.usuario.crear_cuenta("Pedro Martínez", "pedro@example.com", contrasena_larga)
        assert resultado is True
    
    def test_crear_cuenta_con_caracteres_especiales(self):
        """Crear una cuenta con caracteres especiales en el nombre y correo"""
        resultado = self.usuario.crear_cuenta("Usuario#1!", "user!@example.com", "Clave$123")
        assert resultado is True
    
    # ---- PRUEBAS DE ERROR ----
    def test_crear_cuenta_sin_correo(self):
        """Intentar crear una cuenta sin correo electrónico"""
        with pytest.raises(ValueError):
            self.usuario.crear_cuenta("Juan Pérez", "", "Password123")
    
    def test_crear_cuenta_sin_contrasena(self):
        """Intentar crear una cuenta sin contraseña"""
        with pytest.raises(ValueError):
            self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "")
    
    def test_crear_cuenta_correo_repetido(self):
        """Intentar crear una cuenta con un correo ya registrado"""
        self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "Password123")
        with pytest.raises(ValueError):
            self.usuario.crear_cuenta("Otro Usuario", "juan@example.com", "NuevaClave456")

class TestIniciarSesion:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.usuario = Usuario(self.db)
        self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "Password123")
    
    # ---- PRUEBAS NORMALES ----
    def test_iniciar_sesion_valida(self):
        """Iniciar sesión con credenciales correctas"""
        resultado = self.usuario.iniciar_sesion("juan@example.com", "Password123")
        assert resultado is not None
    
    def test_iniciar_sesion_usuario_diferente(self):
        """Iniciar sesión con otra cuenta válida"""
        self.usuario.crear_cuenta("María López", "maria@example.com", "ClaveSegura123")
        resultado = self.usuario.iniciar_sesion("maria@example.com", "ClaveSegura123")
        assert resultado is not None
    
    def test_iniciar_sesion_despues_de_creacion(self):
        """Crear una cuenta e iniciar sesión inmediatamente después"""
        self.usuario.crear_cuenta("Carlos Gómez", "carlos@example.com", "OtraClave456")
        resultado = self.usuario.iniciar_sesion("carlos@example.com", "OtraClave456")
        assert resultado is not None
    
    # ---- PRUEBAS EXTREMAS ----
    def test_iniciar_sesion_contrasena_muy_larga(self):
        """Iniciar sesión con una contraseña extremadamente larga"""
        contrasena_larga = "A" * 100
        self.usuario.crear_cuenta("Pedro Martínez", "pedro@example.com", contrasena_larga)
        resultado = self.usuario.iniciar_sesion("pedro@example.com", contrasena_larga)
        assert resultado is not None
    
    def test_iniciar_sesion_con_caracteres_especiales(self):
        """Iniciar sesión con un correo y contraseña con caracteres especiales"""
        self.usuario.crear_cuenta("Usuario#1!", "user!@example.com", "Clave$123")
        resultado = self.usuario.iniciar_sesion("user!@example.com", "Clave$123")
        assert resultado is not None
    
    def test_iniciar_sesion_usuario_con_nombre_largo(self):
        """Iniciar sesión con un usuario cuyo nombre es muy largo"""
        nombre_largo = "UsuarioLargo" * 20
        self.usuario.crear_cuenta(nombre_largo, "largousuario@example.com", "Password123")
        resultado = self.usuario.iniciar_sesion("largousuario@example.com", "Password123")
        assert resultado is not None
    
    # ---- PRUEBAS DE ERROR ----
    def test_iniciar_sesion_usuario_inexistente(self):
        """Intentar iniciar sesión con un usuario que no existe"""
        with pytest.raises(ValueError):
            self.usuario.iniciar_sesion("desconocido@example.com", "ClaveInvalida")
    
    def test_iniciar_sesion_contrasena_incorrecta(self):
        """Intentar iniciar sesión con una contraseña incorrecta"""
        with pytest.raises(ValueError):
            self.usuario.iniciar_sesion("juan@example.com", "ClaveIncorrecta")
    
    def test_iniciar_sesion_sin_parametros(self):
        """Intentar iniciar sesión sin ingresar usuario ni contraseña"""
        with pytest.raises(ValueError):
            self.usuario.iniciar_sesion("", "")


class TestCambiarContrasena:
    def setup_method(self, method):
        """Configuración antes de cada prueba"""
        self.db = Database()
        self.usuario = Usuario(self.db)
        self.usuario.crear_cuenta("Juan Pérez", "juan@example.com", "Password123")
    
    # ---- PRUEBAS NORMALES ----
    def test_cambiar_contrasena_valida(self):
        """Cambiar contraseña con credenciales correctas"""
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "NuevaPassword456")
        assert resultado is True
    
    def test_cambiar_contrasena_varias_veces(self):
        """Cambiar contraseña dos veces seguidas"""
        self.usuario.cambiar_contrasena("juan@example.com", "NuevaClave1")
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "NuevaClave2")
        assert resultado is True
    
    def test_cambiar_contrasena_despues_de_creacion(self):
        """Cambiar contraseña inmediatamente después de crear una cuenta"""
        self.usuario.crear_cuenta("María López", "maria@example.com", "ClaveSegura123")
        resultado = self.usuario.cambiar_contrasena("maria@example.com", "NuevaClave789")
        assert resultado is True
    
    # ---- PRUEBAS EXTREMAS ----
    def test_cambiar_contrasena_muy_larga(self):
        """Cambiar contraseña con una contraseña extremadamente larga"""
        contrasena_larga = "A" * 100
        resultado = self.usuario.cambiar_contrasena("juan@example.com", contrasena_larga)
        assert resultado is True
    
    def test_cambiar_contrasena_con_caracteres_especiales(self):
        """Cambiar contraseña con caracteres especiales"""
        resultado = self.usuario.cambiar_contrasena("juan@example.com", "Clave$%&/()=?")
        assert resultado is True
    
    def test_cambiar_contrasena_a_misma_clave(self):
        """Intentar cambiar la contraseña a la misma que ya tenía"""
        with pytest.raises(ValueError):
            self.usuario.cambiar_contrasena("juan@example.com", "Password123")
    
    # ---- PRUEBAS DE ERROR ----
    def test_cambiar_contrasena_usuario_inexistente(self):
        """Intentar cambiar la contraseña de un usuario que no existe"""
        with pytest.raises(ValueError):
            self.usuario.cambiar_contrasena("desconocido@example.com", "NuevaClave")
    
    def test_cambiar_contrasena_sin_parametros(self):
        """Intentar cambiar la contraseña sin proporcionar parámetros"""
        with pytest.raises(ValueError):
            self.usuario.cambiar_contrasena("", "")
    
    def test_cambiar_contrasena_sin_contrasena_nueva(self):
        """Intentar cambiar la contraseña sin proporcionar la nueva contraseña"""
        with pytest.raises(ValueError):
            self.usuario.cambiar_contrasena("juan@example.com", "")
