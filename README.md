# Sistema de Resolución de Modelación Lineal

## Descripción

Aplicación desarrollada en Python y PyQt6 para la formulación y resolución de modelos de Programación Lineal mediante Método Gráfico y Método Simplex.

### Características principales

- Maximización y minimización.
- Restricciones <=, >= y =.
- Método gráfico para 2 variables.
- Método simplex para cualquier cantidad de variables.
- Variables de holgura, exceso y artificiales.
- Implementación de Big-M.
- Detección de:
  - Solución óptima.
  - Óptimos múltiples.
  - Modelo infactible.
  - Modelo no acotado.
- Interfaz gráfica desarrollada con PyQt6.

---

## Tecnologías utilizadas

### Lenguaje

- Python 3.13

### Librerías

```bash
pip install pyqt6
pip install matplotlib
pip install numpy
```

## Ejecución

```bash
python main.py
```

---

### Módulos utilizados

- dataclasses
- numpy
- matplotlib
- PyQt6

---

## Arquitectura

```text
ProyectoPL
│
├── main.py
│
├── controllers
│   ├── captura_controller.py
│   ├── grafico_controller.py
│   └── simplex_controller.py
│
├── models
│   ├── problema.py
│   ├── restriccion.py
│   └── variable.py
│
├── services
│   ├── solucionador_grafico.py
│   └── solucionador_simplex.py
│
├── views
│   ├── inicio_view.py
│   ├── instrucciones_view.py
│   ├── captura_view.py
│   ├── resumen_view.py
│   ├── grafico_view.py
│   └── simplex_view.py
│
└── utils
    ├── constantes.py
    └── validaciones.py
```

---

## Casos de prueba validados

### Caso 1

```text
MAX
Z = 4X + 6Y

X + Y <= 8
2X + Y <= 10
```

Resultado:

```text
X = 0
Y = 8
Z = 48
```

---

### Caso 2

```text
MAX
Z = 5X + 3Y

X - Y >= 1
```

Resultado:

```text
NO_ACOTADO
```

---

### Caso 3

```text
MAX
Z = 2X + 4Y

X + Y <= 3
X + Y >= 7
```

Resultado:

```text
INFACTIBLE
```

---

### Caso 4

```text
MAX
Z = 3X + 3Y

X + Y <= 10
X <= 8
Y <= 2
```

Resultado:

```text
Óptimos múltiples
(8,2)
(2,8)
Z = 30
```

---

### Caso 5

```text
MAX
Z = 8X + 6Y + 5Z + 4W + 3V
```

Resultado:

```text
Método gráfico no disponible (Máx 3 variables)
Método simplex resuelto correctamente
```

---

## Validaciones implementadas

- Nombre del caso obligatorio.
- Variables obligatorias.
- Función objetivo obligatoria.
- Restricciones completas.
- Método gráfico limitado a 2 variables.
- Detección de modelos infactibles.
- Detección de modelos no acotados.
- Manejo de errores mediante mensajes amigables.

---

## Autores

- Duvan Palma de la Hoz
- Johnny Coy Herrera
- Oswaldo Moreno Altahona
- Daniel Mejía De la Hoz
- Moisés Cerna Juliao

---

## Asignatura

Electiva Complementaria II

Ingeniería de Sistemas

Corporación Universitaria Politecnico de la Costa Atlantica
