from src.model.database import Database
from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.errores import *

class Menu:
    def __init__(self):
        self.db = Database()
        self.actividad = Actividad(self.db)
        self.bitacora = Bitacora(self.db)
        self.usuario = Usuario(self.db)

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE BITÁCORA ---")
            print("1. Registrar actividad")
            print("2. Consultar actividades")
            print("3. Generar reporte")
            print("4. Crear cuenta de usuario")
            print("5. Iniciar sesión")
            print("6. Cambiar contraseña")
            print("7. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.registrar_actividad()
            elif opcion == "2":
                self.consultar_actividades()
            elif opcion == "3":
                self.generar_reporte()
            elif opcion == "4":
                self.crear_cuenta()
            elif opcion == "5":
                self.iniciar_sesion()
            elif opcion == "6":
                self.cambiar_contrasena()
            elif opcion == "7":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def registrar_actividad(self):
        try:
            fecha = input("Fecha (YYYY-MM-DD): ")
            supervisor = input("Supervisor: ")
            descripcion = input("Descripción: ")
            anexos = input("Anexos: ")
            responsable = input("Responsable: ")
            clima = input("Clima: ")
            self.actividad.registrar_actividad(fecha, supervisor, descripcion, anexos, responsable, clima)
            print("Actividad registrada exitosamente.")
        except BaseError as e:
            print(f"Error: {e}")

    def consultar_actividades(self):
        try:
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
            actividades = self.actividad.consultar_actividades(fecha_inicio, fecha_fin)
            for act in actividades:
                print(act)
        except BaseError as e:
            print(f"Error: {e}")

    def generar_reporte(self):
        try:
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
            archivo_pdf = input("Nombre del archivo PDF: ")
            if self.bitacora.generar_reporte(fecha_inicio, fecha_fin, archivo_pdf):
                print("Reporte generado exitosamente.")
            else:
                print("No hay actividades en el rango de fechas proporcionado.")
        except BaseError as e:
            print(f"Error: {e}")

    def crear_cuenta(self):
        try:
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            contrasena = input("Contraseña: ")
            if self.usuario.crear_cuenta(nombre, correo, contrasena):
                print("Cuenta creada exitosamente.")
        except BaseError as e:
            print(f"Error: {e}")

    def iniciar_sesion(self):
        try:
            correo = input("Correo: ")
            contrasena = input("Contraseña: ")
            user = self.usuario.iniciar_sesion(correo, contrasena)
            print(f"Bienvenido {user[1]}")
        except BaseError as e:
            print(f"Error: {e}")

    def cambiar_contrasena(self):
        try:
            correo = input("Correo: ")
            nueva_contrasena = input("Nueva contraseña: ")
            if self.usuario.cambiar_contrasena(correo, nueva_contrasena):
                print("Contraseña cambiada exitosamente.")
        except BaseError as e:
            print(f"Error: {e}")
