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
    |           Clases CuerpoAgua y Laguna - Herencia Simple (cuerpo_agua.py).   |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

from excepciones import ErrorRegistro


class CuerpoAgua:
    def __init__(self, nombre, ubicacion, tipo):
        self.nombre = nombre          # público
        self._ubicacion = ubicacion   # protegido (convención)
        self.__tipo = tipo            # privado (name mangling: _CuerpoAgua__tipo)

    def get_tipo(self):
        return self.__tipo

    def mostrar_informacion(self):
        return (f"Cuerpo de agua: {self.nombre}\n"
                f"Ubicación:      {self._ubicacion}\n"
                f"Tipo:           {self.__tipo}")

    def evaluar_estado(self, mediciones=None):
        """Evaluación general según el porcentaje de mediciones dentro de rango."""
        if not mediciones:
            raise ErrorRegistro(f"No hay mediciones para evaluar '{self.nombre}'.")
        total = len(mediciones)
        ok = sum(1 for m in mediciones if m.validar_rangos())
        proporcion = ok / total
        nivel = "Bueno" if proporcion >= 0.8 else "Regular" if proporcion >= 0.5 else "Crítico"
        return f"{self.nombre} ({self.get_tipo()}): estado {nivel} ({ok}/{total} mediciones en rango)"


class Laguna(CuerpoAgua):
    def __init__(self, nombre, ubicacion, tipo, profundidad, numero_puntos_muestreo):
        super().__init__(nombre, ubicacion, tipo)
        if profundidad <= 0 or numero_puntos_muestreo < 1:
            raise ValueError("Profundidad debe ser > 0 y los puntos de muestreo ≥ 1.")
        self.profundidad = profundidad                      # metros
        self.numero_puntos_muestreo = numero_puntos_muestreo

    def mostrar_informacion_laguna(self):
        """Muestra datos propios y demuestra público vs protegido vs privado."""
        lineas = [
            f"Laguna:               {self.nombre}   <- público: acceso directo",
            f"Ubicación:            {self._ubicacion}   <- protegido: accesible en la subclase (por convención)",
            f"Profundidad:          {self.profundidad} m",
            f"Puntos de muestreo:   {self.numero_puntos_muestreo}",
        ]
        try:
            lineas.append(f"Tipo (self.__tipo):   {self.__tipo}")   # se interpreta como _Laguna__tipo
        except AttributeError as e:
            lineas.append(f"self.__tipo           -> AttributeError: {e}")
        lineas.append(f"self.get_tipo():      {self.get_tipo()}   <- acceso correcto vía getter")
        lineas.append(f"self._CuerpoAgua__tipo: {self._CuerpoAgua__tipo}   <- name mangling (no recomendado)")
        return "\n".join(lineas)

    def evaluar_estado(self, mediciones=None):
        """Evaluación específica: base + profundidad y representatividad del muestreo."""
        base = super().evaluar_estado(mediciones)
        notas = []
        if self.profundidad < 2:
            notas.append("laguna somera: más sensible a cambios de temperatura y oxígeno")
        else:
            notas.append("profundidad adecuada para estabilidad térmica")
        if self.numero_puntos_muestreo < 3:
            notas.append("pocos puntos de muestreo: evaluación poco representativa")
        else:
            notas.append("muestreo representativo")
        return f"{base}\nLaguna -> " + "; ".join(notas) + "."