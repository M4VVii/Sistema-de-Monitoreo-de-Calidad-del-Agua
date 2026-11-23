<div align="center">

# 💧 Monitor de Agua

</div>

<div align="center">
  <table>
    <tr>
      <td align="center" valign="middle">
        <img src="logos/ipn.webp" alt="Logo IPN" width="100">
      </td>
      <td align="center" valign="middle">
        <strong>INSTITUTO POLITÉCNICO NACIONAL</strong><br>
        <strong>ESCUELA SUPERIOR DE CÓMPUTO</strong><br><br>
        Ingeniería en Inteligencia Artificial<br>
        Paradigmas de Programación — Práctica Paradigma Orientado a Objetos<br>
        Semestre: 2027-1<br>
      </td>
      <td align="center" valign="middle">
        <img src="logos/escom.webp" alt="Logo ESCOM" width="140">
      </td>
    </tr>
  </table>
</div>

<div align="justify">

## 1. Descripción del Proyecto y Problema que Resuelve

**Monitor de Agua** es una aplicación **modular de consola** desarrollada en **Python puro**, usando **únicamente la biblioteca estándar**. No utiliza sensores físicos, bases de datos ni interfaces gráficas; los datos se capturan manualmente por consola y se mantienen en memoria durante la ejecución.

**El Problema:** Los cuerpos de agua como lagos, lagunas y jagüeyes requieren un monitoreo periódico de sus parámetros fisicoquímicos (pH, temperatura, oxígeno disuelto y turbidez) para detectar a tiempo alteraciones ambientales. Sin una validación sistemática, los valores anómalos pasan inadvertidos o se registran datos inconsistentes.

**La Solución:** Un sistema orientado a objetos que **valida rangos didácticos** al momento de registrar cada medición, **encapsula los datos sensibles** mediante niveles de acceso, **maneja excepciones personalizadas** sin detener el programa y **evalúa el estado del agua** combinando criterios físicos y químicos.

## 2. Arquitectura POO e Implementación Técnica

### 2.1 Encapsulamiento y Niveles de Acceso

Python no impone modificadores de acceso estrictos; se aplican por **convención** (`_`) y por **name mangling** (`__`).

| Clase | Atributo | Nivel | Acceso |
|:--|:--|:--|:--|
| `MedicionAgua` | `fecha`, `turbidez` | **Público** | Directo: `medicion.fecha` |
| `MedicionAgua` | `_temperatura` | **Protegido** | Convención: Uso interno y en subclases/módulos cercanos |
| `MedicionAgua` | `__ph`, `__oxigeno` | **Privado** | Solo con `get_ph()`, `set_ph()`, `get_oxigeno()`, `set_oxigeno()` |
| `CuerpoAgua` | `nombre` | **Público** | Directo: `cuerpo.nombre` |
| `CuerpoAgua` | `_ubicacion` | **Protegido** | Accesible desde la subclase `Laguna` |
| `CuerpoAgua` | `__tipo` | **Privado** | Solo con `get_tipo()` |

- Los **setters validan** el rango antes de modificar el valor, mediante el método privado `__validar()`, que lanza `ValorFueraDeRango` si el dato no cumple.
- El *name mangling* transforma `__ph` en `_MedicionAgua__ph` y `__tipo` en `_CuerpoAgua__tipo`, por lo que no se accede a ellos con su nombre original desde fuera de su clase.
- `Laguna.mostrar_informacion_laguna()` **demuestra la diferencia de forma controlada**: Accede directamente a `self.nombre` (público) y `self._ubicacion` (protegido), captura el `AttributeError` al leer `self.__tipo` (que Python interpreta como `_Laguna__tipo`) y muestra el acceso correcto con `self.get_tipo()`.

```python
try:
    print(self.__tipo)            # se interpreta como self._Laguna__tipo
except AttributeError as e:
    print(f"AttributeError: {e}")
print(self.get_tipo())            # acceso correcto mediante getter
```

### 2.2 Herencia Simple y Sobrescritura

`Laguna` hereda de `CuerpoAgua`:

- **Reutiliza el constructor padre** con `super().__init__(nombre, ubicacion, tipo)` y agrega los atributos públicos `profundidad` y `numero_puntos_muestreo`.
- **Sobrescribe `evaluar_estado()`**:
  - `CuerpoAgua.evaluar_estado()` calcula el porcentaje de mediciones dentro de rango: **Bueno** (≥ 80 %), **Regular** (≥ 50 %) o **Crítico** (< 50 %).
  - `Laguna.evaluar_estado()` invoca la versión base con `super()` y le añade observaciones propias: Si la **profundidad es menor a 2 m** (laguna somera, más sensible a temperatura y oxígeno) y si hay **menos de 3 puntos de muestreo** (evaluación poco representativa).

### 2.3 Herencia Múltiple y MRO (Method Resolution Order)

`SistemaEvaluacion` hereda simultáneamente de `EvaluadorFisico` (temperatura y turbidez) y `EvaluadorQuimico` (pH y oxígeno disuelto). Ambas clases definen un método con el **mismo nombre**, `obtener_criterio_base()`.

```python
class SistemaEvaluacion(EvaluadorFisico, EvaluadorQuimico):
    def obtener_criterio_base(self):
        return f"Sistema de Evaluación -> {super().obtener_criterio_base()}"
```

`SistemaEvaluacion.mro()` devuelve el orden lineal de búsqueda, de izquierda a derecha:

```text
SistemaEvaluacion -> EvaluadorFisico -> EvaluadorQuimico -> object
```

Como `EvaluadorFisico` aparece primero, `super().obtener_criterio_base()` resuelve y ejecuta **su versión** (`"Criterio Físico: ..."`); la de `EvaluadorQuimico` queda oculta y solo se alcanza con una llamada explícita (`EvaluadorQuimico.obtener_criterio_base(self)`). Ambas se muestran en la opción 6 del menú.

Además, `evaluar_calidad(medicion)` invoca los cuatro métodos heredados (`evaluar_temperatura`, `evaluar_turbidez`, `evaluar_ph`, `evaluar_oxigeno`) y emite el dictamen general: **ACEPTABLE** o **REQUIERE ATENCIÓN**.

### 2.4 Manejo de Excepciones Personalizadas

```text
Exception
├── ErrorMedicion
│   └── ValorFueraDeRango
└── ErrorRegistro
```

| Excepción | Cuándo se lanza |
|:--|:--|
| `ErrorMedicion` | Clase base de los errores relacionados con mediciones. |
| `ValorFueraDeRango` | Un parámetro ambiental no cumple su rango permitido. |
| `ErrorRegistro` | Operación inválida sobre el registro (sin cuerpo de agua o sin mediciones). |

`manejador_errores.py` centraliza la captura: `ejecutar_seguro(operacion, *args, **kwargs)` ejecuta cualquier operación dentro de `try / except` y devuelve `(exito, resultado)`. Captura, en este orden, `ValorFueraDeRango`, `ErrorMedicion`, `ErrorRegistro`, `ValueError` (entradas no numéricas) y `Exception` (último recurso), e imprime mensajes amigables **sin detener el programa**. La subclase se captura antes que su clase base para que el mensaje sea el más específico.

## 3. Estructura del Proyecto y Descripción de Módulos

```text
📦 monitor-agua/
├── 📂 evidencias/           # Capturas de pantalla del entorno virtual y pruebas
├── 📂 logos/                # Escudos institucionales (IPN y ESCOM)
├── 📂 venv/                 # Entorno virtual (excluido de Git y del .zip de entrega)
├── 📜 .gitignore            # Exclusión de venv, __pycache__ y archivos sensibles
├── 📜 cuerpo_agua.py        # Clases CuerpoAgua y Laguna (herencia simple y sobrescritura)
├── 📜 evaluadores.py        # EvaluadorFisico, EvaluadorQuimico y SistemaEvaluacion (MRO)
├── 📜 excepciones.py        # Excepciones personalizadas (ErrorMedicion, ValorFueraDeRango, ErrorRegistro)
├── 📜 LICENSE               # Licencia del proyecto
├── 📜 main.py               # Programa principal y menú de interacción en consola
├── 📜 manejador_errores.py  # Gestión centralizada de errores con try/except/raise
├── 📜 medicion.py           # Clase MedicionAgua (encapsulamiento y rangos didácticos)
└── 📜 README.md             # Documentación del proyecto
```

| Módulo | Responsabilidad |
|:--|:--|
| `main.py` | Punto de entrada. Menú de consola en ciclo `while` (opciones 1 a 8), estado en memoria (cuerpo de agua y lista de mediciones) y despacho de cada opción mediante `ejecutar_seguro()`. |
| `cuerpo_agua.py` | Clases `CuerpoAgua` y `Laguna` (herencia simple): Datos del cuerpo de agua, `mostrar_informacion()`, `evaluar_estado()` y demostración de acceso público/protegido/privado. |
| `medicion.py` | Clase `MedicionAgua`: Encapsulamiento, getters/setters, validación privada de rangos, `validar_rangos()` y `mostrar_informacion()`. |
| `evaluadores.py` | `EvaluadorFisico`, `EvaluadorQuimico` y `SistemaEvaluacion` (herencia múltiple): Dictámenes por parámetro, reporte de calidad y `mostrar_mro()`. |
| `excepciones.py` | Jerarquía `ErrorMedicion`, `ValorFueraDeRango` y `ErrorRegistro`. |
| `manejador_errores.py` | Funciones seguras con `try / except / raise`: `convertir_numero()`, `leer_numero()`, `ejecutar_seguro()`, `registrar_medicion()`, `consultar_mediciones()` y sus variantes `_segura`. |

## 4. Parámetros de Validación (Rangos Didácticos)

| Parámetro | Atributo en `MedicionAgua` | Nivel de acceso | Rango válido |
|:--|:--|:--:|:--:|
| **pH** | `__ph` | Privado | `6.5 a 8.5` |
| **Temperatura** | `_temperatura` | Protegido | `0 a 35 °C` |
| **Oxígeno disuelto** | `__oxigeno` | Privado | `>= 5 mg/L` |
| **Turbidez** | `turbidez` | Público | `0 a 10 NTU` |

Si algún valor incumple su rango, `MedicionAgua` lanza `ValorFueraDeRango` con un mensaje claro y la medición **no se guarda**.

## 5. Instalación y Ejecución Local

**Requisitos previos:** Python 3.x (sin dependencias externas).

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Ejecutar la aplicación**

```bash
python main.py
```

## 6. Pruebas Obligatorias Validadas

| # | Prueba | Resultado verificado en consola |
|:-:|:--|:--|
| 1 | **Registro correcto de `Laguna Azul`** (opción 1) | Se instancia `Laguna` con profundidad y puntos de muestreo, y se confirma con su información. |
| 2 | **Detección de valores fuera de rango** (opción 2) | Se lanza `ValorFueraDeRango`, se muestra un mensaje amigable y la medición no se almacena. |
| 3 | **Modificación de atributos privados mediante *setters*** (opción 8) | `set_ph()` y `set_oxigeno()` validan y actualizan; si un valor es inválido se revierten los cambios. |
| 4 | **Herencia y sobrescritura en `Laguna`** (opción 3) | Se ejecutan `mostrar_informacion()`, el `evaluar_estado()` sobrescrito y `mostrar_informacion_laguna()`. |
| 5 | **Herencia múltiple y resolución MRO** (opción 6) | Se imprime `SistemaEvaluacion.mro()` y se demuestra que `super()` ejecuta primero `EvaluadorFisico`. |
| 6 | **Consulta controlada de medición inexistente** (opción 4 sin datos) | Se lanza `ErrorRegistro`, se muestra el mensaje y el programa continúa sin cerrarse. |

## 7. WHISPER...

💧🌿 *"El agua es la fuerza motriz de toda la naturaleza."*

**~By Leonardo da Vinci** ✨

---

***Repositorio mantenido por MAVV.*** 🫰
</div>