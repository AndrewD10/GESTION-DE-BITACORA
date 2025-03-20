from src.model.database import Database
from src.model.actividad import Actividad
from src.model.bitacora import Bitacora
from src.model.usuario import Usuario
from src.model.errores import *


def main():
    db = Database()
    actividad = Actividad(db)
    bitacora = Bitacora(db)
    usuario = Usuario(db)

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
            try:
                fecha = input("Fecha (YYYY-MM-DD): ")
                supervisor = input("Supervisor: ")
                descripcion = input("Descripción: ")
                anexos = input("Anexos: ")
                responsable = input("Responsable: ")
                clima = input("Clima: ")
                actividad.registrar_actividad(fecha, supervisor, descripcion, anexos, responsable, clima)
                print("Actividad registrada exitosamente.")
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            try:
                fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
                actividades = actividad.consultar_actividades(fecha_inicio, fecha_fin)
                for act in actividades:
                    print(act)
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            try:
                fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
                archivo_pdf = input("Nombre del archivo PDF: ")
                if bitacora.generar_reporte(fecha_inicio, fecha_fin, archivo_pdf):
                    print("Reporte generado exitosamente.")
                else:
                    print("No hay actividades en el rango de fechas proporcionado.")
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            try:
                nombre = input("Nombre: ")
                correo = input("Correo: ")
                contrasena = input("Contraseña: ")
                if usuario.crear_cuenta(nombre, correo, contrasena):
                    print("Cuenta creada exitosamente.")
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "5":
            try:
                correo = input("Correo: ")
                contrasena = input("Contraseña: ")
                user = usuario.iniciar_sesion(correo, contrasena)
                print(f"Bienvenido {user[1]}")
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "6":
            try:
                correo = input("Correo: ")
                nueva_contrasena = input("Nueva contraseña: ")
                if usuario.cambiar_contrasena(correo, nueva_contrasena):
                    print("Contraseña cambiada exitosamente.")
            except BaseError as e:
                print(f"Error: {e}")

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
