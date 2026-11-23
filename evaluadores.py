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
    |           Evaluadores y Herencia Múltiple / MRO (evaluadores.py).          |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

OK = "[OK]"
ALERTA = "[ALERTA]"


def _dictamen(parametro, valor, minimo, maximo, rango_txt):
    """Compara valor con [minimo, maximo] (None = sin límite) y devuelve un dictamen."""
    en_rango = (minimo is None or valor >= minimo) and (maximo is None or valor <= maximo)
    if en_rango:
        return f"{OK} {parametro}: {valor} dentro del rango ({rango_txt})."
    if minimo is not None and valor < minimo:
        causa = "por debajo del mínimo"
    elif maximo is not None and valor > maximo:
        causa = "por encima del máximo"
    else:
        causa = "valor no válido"
    return f"{ALERTA} {parametro}: {valor} {causa} (permitido: {rango_txt})."


class EvaluadorFisico:
    RANGO_TEMPERATURA = (0, 35)   # °C
    RANGO_TURBIDEZ = (0, 10)      # NTU

    def evaluar_temperatura(self, medicion):
        minimo, maximo = self.RANGO_TEMPERATURA
        return _dictamen("Temperatura", medicion._temperatura, minimo, maximo, "0 a 35 °C")

    def evaluar_turbidez(self, medicion):
        minimo, maximo = self.RANGO_TURBIDEZ
        return _dictamen("Turbidez", medicion.turbidez, minimo, maximo, "0 a 10 NTU")

    def obtener_criterio_base(self):
        return "Criterio Físico: Evaluación basada en temperatura y turbidez del agua."


class EvaluadorQuimico:
    RANGO_PH = (6.5, 8.5)
    OXIGENO_MINIMO = 5            # mg/L

    def evaluar_ph(self, medicion):
        minimo, maximo = self.RANGO_PH
        return _dictamen("pH", medicion.get_ph(), minimo, maximo, "6.5 a 8.5")

    def evaluar_oxigeno(self, medicion):
        return _dictamen("Oxígeno disuelto", medicion.get_oxigeno(), self.OXIGENO_MINIMO, None, "≥ 5 mg/L")

    def obtener_criterio_base(self):   # mismo nombre que en EvaluadorFisico
        return "Criterio Químico: Evaluación basada en pH y oxígeno disuelto."


class SistemaEvaluacion(EvaluadorFisico, EvaluadorQuimico):
    def obtener_criterio_base(self):
        # super() sigue el MRO: El siguiente tras SistemaEvaluacion es EvaluadorFisico
        return f"Sistema de Evaluación -> {super().obtener_criterio_base()}"

    def evaluar_calidad(self, medicion):
        """Reporte completo con los 4 dictámenes y el estado general."""
        dictamenes = [
            self.evaluar_temperatura(medicion),   # EvaluadorFisico
            self.evaluar_turbidez(medicion),      # EvaluadorFisico
            self.evaluar_ph(medicion),            # EvaluadorQuimico
            self.evaluar_oxigeno(medicion),       # EvaluadorQuimico
        ]
        fallas = sum(1 for d in dictamenes if ALERTA in d)
        estado = "ACEPTABLE" if fallas == 0 else "REQUIERE ATENCIÓN"
        lineas = [
            "=== REPORTE DE CALIDAD DEL AGUA ===",
            f"Fecha de medición: {medicion.fecha}",
            "-----------------------------------",
            *dictamenes,
            "-----------------------------------",
            f"Parámetros con alerta: {fallas}/4",
            f"ESTADO GENERAL: {estado}",
        ]
        return "\n".join(lineas)

    def mostrar_mro(self):
        """Imprime el MRO y demuestra qué método repetido se ejecuta primero."""
        mro = SistemaEvaluacion.mro()
        print("MRO de SistemaEvaluacion:")
        print("  " + " -> ".join(clase.__name__ for clase in mro))
        print("\nself.obtener_criterio_base() (vía super()):")
        print(f"  {self.obtener_criterio_base()}")
        print("Llamada explícita a EvaluadorQuimico (super() no la alcanza, Físico la oculta):")
        print(f"  {EvaluadorQuimico.obtener_criterio_base(self)}")
        print(
            "\nExplicación: el MRO (Method Resolution Order) es el orden lineal, de izquierda a "
            "derecha, en que Python busca atributos y métodos en la jerarquía. Como "
            "SistemaEvaluacion hereda primero de EvaluadorFisico, super() resuelve ahí el método "
            "repetido y EvaluadorQuimico queda después en la cadena."
        )