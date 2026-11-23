"""
    ______________________________________________________________________________
    |                                                                            |
    |                       INSTITUTO POLITÉCNICO NACIONAL                       |
    |                        ESCUELA SUPERIOR DE CÓMPUTO                         |
    |                                                                            |
    |                  Asignatura: Paradigmas de Programación                    |
    |                  Práctica: Paradigma Orientado a Objetos                   |
    |                  Docente: Dra. Morales Rodriguez Ursula Samantha           |
    |                                                                            |
    |   TÍTULO: Sistema de Monitoreo de Calidad del Agua.                        |
    |           Programa Principal y Menú de Consola (main.py).                  |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

from datetime import date

from excepciones import ErrorRegistro
from manejador_errores import ejecutar_seguro, convertir_numero, consultar_mediciones
from medicion import MedicionAgua
from cuerpo_agua import CuerpoAgua, Laguna
from evaluadores import SistemaEvaluacion


def mostrar_menu():
    print("\nSISTEMA DE MONITOREO DE CALIDAD DEL AGUA")
    print("1. Registrar un cuerpo de agua.")
    print("2. Registrar una medición.")
    print("3. Consultar información del cuerpo de agua.")
    print("4. Consultar todas las mediciones registradas.")
    print("5. Evaluar la calidad del agua.")
    print("6. Mostrar el orden MRO del sistema de evaluación.")
    print("7. Salir.")
    print("8. Modificar pH y oxígeno de una medición.")


# Entradas
def leer_float(mensaje, campo):
    """Lee un número; lanza ValueError si no es numérico."""
    return convertir_numero(input(mensaje), campo)


def leer_entero(mensaje, campo):
    """Lee un entero; lanza ValueError si no lo es."""
    valor = leer_float(mensaje, campo)
    if not valor.is_integer():
        raise ValueError(f"'{campo}' debe ser un número entero.")
    return int(valor)


def exigir_cuerpo(estado):
    """Devuelve el cuerpo de agua o lanza ErrorRegistro si no existe."""
    if estado["cuerpo"] is None:
        raise ErrorRegistro("Aún no hay un cuerpo de agua registrado (usa la opción 1).")
    return estado["cuerpo"]


# Opciones
def registrar_cuerpo(estado):
    nombre = input("Nombre: ").strip()
    ubicacion = input("Ubicación: ").strip()
    tipo = input("Tipo (ej. laguna, río, presa): ").strip()
    if not nombre or not ubicacion or not tipo:
        raise ValueError("Nombre, ubicación y tipo no pueden estar vacíos.")

    if tipo.lower() == "laguna":
        profundidad = leer_float("Profundidad (m): ", "profundidad")
        puntos = leer_entero("Número de puntos de muestreo: ", "número de puntos de muestreo")
        cuerpo = Laguna(nombre, ubicacion, tipo, profundidad, puntos)
    else:
        cuerpo = CuerpoAgua(nombre, ubicacion, tipo)

    estado["cuerpo"] = cuerpo
    print("\n✔ Cuerpo de agua registrado:")
    print(cuerpo.mostrar_informacion())
    if isinstance(cuerpo, Laguna):
        print(f"Profundidad:    {cuerpo.profundidad} m\n"
              f"Puntos muestreo: {cuerpo.numero_puntos_muestreo}")


def registrar_medicion(estado):
    exigir_cuerpo(estado)                       # Lanza ErrorRegistro si no hay
    fecha = input("Fecha (AAAA-MM-DD, Enter = hoy): ").strip() or date.today().isoformat()
    ph = leer_float("pH: ", "pH")
    temperatura = leer_float("Temperatura (°C): ", "temperatura")
    oxigeno = leer_float("Oxígeno disuelto (mg/L): ", "oxígeno")
    turbidez = leer_float("Turbidez (NTU): ", "turbidez")

    # Puede lanzar ValorFueraDeRango, solo se guarda si es válida
    medicion = MedicionAgua(fecha, temperatura, ph, oxigeno, turbidez)
    estado["mediciones"].append(medicion)
    print("\n✔ Medición registrada:")
    print(medicion.mostrar_informacion())


def consultar_cuerpo(estado):
    cuerpo = exigir_cuerpo(estado)
    print("\n" + cuerpo.mostrar_informacion())
    # evaluar_estado() (sobrescrito en Laguna), sin mediciones lanza ErrorRegistro
    exito, evaluacion = ejecutar_seguro(cuerpo.evaluar_estado, estado["mediciones"])
    if exito:
        print("\nEvaluación: " + evaluacion)
    if isinstance(cuerpo, Laguna):
        print("\n" + cuerpo.mostrar_informacion_laguna())


def consultar_todas(estado):
    mediciones = consultar_mediciones(estado["mediciones"])   # Lanza ErrorRegistro si vacía
    for i, m in enumerate(mediciones, start=1):
        print(f"\n--- Medición {i} ---\n{m.mostrar_informacion()}")


def evaluar_calidad(estado):
    mediciones = consultar_mediciones(estado["mediciones"])
    print(f"\nEvaluando la última medición (#{len(mediciones)} de {len(mediciones)}):")
    print(SistemaEvaluacion().evaluar_calidad(mediciones[-1]))


def mostrar_mro(estado):
    SistemaEvaluacion().mostrar_mro()


def modificar_ph_oxigeno(estado):
    mediciones = consultar_mediciones(estado["mediciones"])
    for i, m in enumerate(mediciones, start=1):
        print(f"{i}. {m.fecha} | pH: {m.get_ph()} | Oxígeno: {m.get_oxigeno()} mg/L")

    indice = leer_entero("Número de medición a modificar: ", "índice")
    if not 1 <= indice <= len(mediciones):
        raise ErrorRegistro(f"No existe la medición #{indice} (hay {len(mediciones)}).")
    medicion = mediciones[indice - 1]

    nuevo_ph = leer_float("Nuevo pH: ", "pH")
    nuevo_oxigeno = leer_float("Nuevo oxígeno (mg/L): ", "oxígeno")

    ph_ant, ox_ant = medicion.get_ph(), medicion.get_oxigeno()
    try:
        medicion.set_ph(nuevo_ph)               # Solo mediante setters
        medicion.set_oxigeno(nuevo_oxigeno)
    except Exception:
        medicion.set_ph(ph_ant)                 # Revierte para no dejar cambios a medias
        medicion.set_oxigeno(ox_ant)
        raise                                   # El manejador mostrará el error

    print(f"\n✔ Valores actualizados -> pH: {medicion.get_ph()} | "
          f"Oxígeno: {medicion.get_oxigeno()} mg/L")


# Programa principal
def main():
    estado = {"cuerpo": None, "mediciones": []}
    acciones = {
        "1": registrar_cuerpo,
        "2": registrar_medicion,
        "3": consultar_cuerpo,
        "4": consultar_todas,
        "5": evaluar_calidad,
        "6": mostrar_mro,
        "8": modificar_ph_oxigeno,
    }

    while True:
        mostrar_menu()
        try:
            opcion = input("Elige una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrumpida. ¡Hasta pronto!")
            break

        if opcion == "7":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        if opcion in acciones:
            try:
                ejecutar_seguro(acciones[opcion], estado)
            except (EOFError, KeyboardInterrupt):
                print("\nOperación cancelada.")
        else:
            print("⚠ Opción no válida. Elige un número del 1 al 8.")


if __name__ == "__main__":
    main()