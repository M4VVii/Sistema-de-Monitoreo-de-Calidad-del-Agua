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
    |           Clase MedicionAgua y Encapsulamiento (medicion.py).              |
    |   ALUMNO:                                                                  |
    |    - Valencia Villanueva Adrian                                            |
    |____________________________________________________________________________|
"""

from excepciones import ValorFueraDeRango


class MedicionAgua:
    RANGO_PH = (6.5, 8.5)
    RANGO_TEMPERATURA = (0, 35)      # °C
    OXIGENO_MINIMO = 5               # mg/L
    RANGO_TURBIDEZ = (0, 10)         # NTU

    def __init__(self, fecha, temperatura, ph, oxigeno, turbidez):
        self.fecha = fecha                                   # público
        self._temperatura = self.__validar("temperatura", temperatura)  # protegido
        self.__ph = self.__validar("ph", ph)                 # privado
        self.__oxigeno = self.__validar("oxigeno", oxigeno)  # privado
        self.turbidez = self.__validar("turbidez", turbidez) # público

    # Validación (método privado)
    def __validar(self, parametro, valor):
        """Devuelve el valor como float o lanza ValorFueraDeRango / ValueError."""
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"{parametro} debe ser numérico (recibido: {valor!r}).") from None

        if parametro == "ph":
            ok, esperado = self.RANGO_PH[0] <= valor <= self.RANGO_PH[1], "6.5 a 8.5"
        elif parametro == "temperatura":
            ok, esperado = self.RANGO_TEMPERATURA[0] <= valor <= self.RANGO_TEMPERATURA[1], "0 a 35 °C"
        elif parametro == "oxigeno":
            ok, esperado = valor >= self.OXIGENO_MINIMO, "≥ 5 mg/L"
        elif parametro == "turbidez":
            ok, esperado = self.RANGO_TURBIDEZ[0] <= valor <= self.RANGO_TURBIDEZ[1], "0 a 10 NTU"
        else:
            raise ValueError(f"Parámetro desconocido: {parametro}")

        if not ok:
            raise ValorFueraDeRango(f"{parametro} = {valor} fuera de rango (permitido: {esperado}).")
        return valor

    # Getters y setters de atributos privados
    def get_ph(self):
        return self.__ph

    def set_ph(self, nuevo_ph):
        self.__ph = self.__validar("ph", nuevo_ph)

    def get_oxigeno(self):
        return self.__oxigeno

    def set_oxigeno(self, nuevo_oxigeno):
        self.__oxigeno = self.__validar("oxigeno", nuevo_oxigeno)

    # Resultados
    def resumen_rangos(self):
        """Devuelve {parametro: bool}; revalida también los atributos públicos/protegidos."""
        datos = {
            "temperatura": self._temperatura,
            "ph": self.__ph,
            "oxigeno": self.__oxigeno,
            "turbidez": self.turbidez,
        }
        resumen = {}
        for parametro, valor in datos.items():
            try:
                self.__validar(parametro, valor)
                resumen[parametro] = True
            except (ValorFueraDeRango, ValueError):
                resumen[parametro] = False
        return resumen

    def validar_rangos(self):
        """True si todos los parámetros cumplen los criterios."""
        return all(self.resumen_rangos().values())

    def mostrar_informacion(self):
        """Devuelve un texto con todos los datos (privados vía getters)."""
        estado = "CUMPLE" if self.validar_rangos() else "NO CUMPLE"
        return (
            f"Fecha:        {self.fecha}\n"
            f"Temperatura:  {self._temperatura} °C\n"
            f"pH:           {self.get_ph()}\n"
            f"Oxígeno:      {self.get_oxigeno()} mg/L\n"
            f"Turbidez:     {self.turbidez} NTU\n"
            f"Criterios:    {estado}"
        )