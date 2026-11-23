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
    |           Gestión Centralizada de Errores (manejador_errores.py).          |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

from excepciones import ErrorMedicion, ValorFueraDeRango, ErrorRegistro
from medicion import MedicionAgua


def convertir_numero(valor, campo):
    """Convierte a float; lanza ValueError con mensaje claro si no es numérico."""
    try:
        return float(str(valor).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError(f"'{campo}' debe ser numérico (recibido: {valor!r}).") from None


def leer_numero(mensaje):
    """Pide un número por consola y reintenta hasta recibir uno válido."""
    while True:
        try:
            return convertir_numero(input(mensaje), "entrada")
        except ValueError:
            print("⚠ Entrada no numérica. Intenta de nuevo (ej. 7.2).")


def ejecutar_seguro(operacion, *args, **kwargs):
    """Ejecuta `operacion`; devuelve (exito, resultado) sin detener el programa."""
    try:
        return True, operacion(*args, **kwargs)
    except ValorFueraDeRango as e:      # subclase: Va antes que ErrorMedicion
        print(f"⚠ Valor fuera de rango: {e}")
    except ErrorMedicion as e:
        print(f"⚠ Error de medición: {e}")
    except ErrorRegistro as e:
        print(f"⚠ Error de registro: {e}")
    except ValueError as e:
        print(f"⚠ Dato inválido: {e}")
    except Exception as e:              # Último recurso
        print(f"⚠ Error inesperado ({type(e).__name__}): {e}")
    return False, None


def registrar_medicion(registro, fecha, temperatura, ph, oxigeno, turbidez):
    """Crea una MedicionAgua y la agrega al registro (puede lanzar excepciones)."""
    if not isinstance(registro, list):
        raise ErrorRegistro("El registro no es válido: se esperaba una lista.")
    medicion = MedicionAgua(
        fecha,
        convertir_numero(temperatura, "temperatura"),
        convertir_numero(ph, "pH"),
        convertir_numero(oxigeno, "oxígeno"),
        convertir_numero(turbidez, "turbidez"),
    )
    registro.append(medicion)
    return medicion


def consultar_mediciones(registro):
    """Devuelve las mediciones; lanza ErrorRegistro si no hay ninguna."""
    if registro is None or len(registro) == 0:
        raise ErrorRegistro("No hay mediciones registradas para consultar.")
    return registro


def registrar_medicion_segura(registro, fecha, temperatura, ph, oxigeno, turbidez):
    """Versión segura: imprime confirmación o el error amigable."""
    exito, medicion = ejecutar_seguro(
        registrar_medicion, registro, fecha, temperatura, ph, oxigeno, turbidez
    )
    if exito:
        print(f"✔ Medición del {medicion.fecha} registrada correctamente.")
    return exito


def consultar_mediciones_seguro(registro):
    """Versión segura: imprime todas las mediciones o el error amigable."""
    exito, mediciones = ejecutar_seguro(consultar_mediciones, registro)
    if exito:
        for i, m in enumerate(mediciones, start=1):
            print(f"\n--- Medición {i} ---\n{m.mostrar_informacion()}")
    return exito