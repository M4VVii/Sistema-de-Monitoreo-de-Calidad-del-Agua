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
    |           Jerarquía de Excepciones Personalizadas (excepciones.py).        |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

class ErrorMedicion(Exception):
    """Base para errores relacionados con las mediciones."""


class ValorFueraDeRango(ErrorMedicion):
    """Un parámetro ambiental está fuera de los rangos permitidos."""


class ErrorRegistro(Exception):
    """Operación inválida sobre el registro (vacío, sin cuerpo de agua, etc.)."""