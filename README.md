# Taller: Árboles, Recorridos y Complejidad Computacional

### Estructuras de datos para el análisis sintáctico descendente

##  Descripción General del Proyecto

Este repositorio contiene la solución práctica y conceptual del taller de árboles y complejidad computacional aplicado al análisis sintáctico descendente. El propósito principal es afianzar el manejo de árboles generales y binarios como estructura base en el diseño de traductores y compiladores, analizando su implementación algorítmica y su eficiencia tanto temporal ($\mathcal{O}$) como espacial.

##  Estructura del Repositorio

El proyecto se encuentra organizado modularmente por carpetas independientes para cada punto del taller:

```
taller_sintaxis/
├── ejer_1/                 # Punto 1: Conceptos y representación de árboles
│   └── .
├── ejer_2/                 # Punto 2: Construcción de un árbol de expresiones
│   └── .
├── ejer_3/                 # Punto 3: Recorridos en profundidad (DFS)
│   └── .
├── ejer_4/                 # Punto 4: Recorrido en anchura (BFS)
│   ├── punto4_bfs.py       # Implementación algorítmica de BFS
│   └── README.md           # Documentación técnica y análisis del Punto 4
├── ejer_5/                 # Punto 5: Aplicación al análisis sintáctico
│   └── .
└── README.md               # Documentación general del repositorio (este archivo)

```

## Resumen y Alcance de Cada Ejercicio

### `ejer_1/` — Conceptos y Representación de Árboles

* **Ubicación:** `ejer_1/`

* **Idea General:** Modelado formal de un árbol a partir de relaciones padre-hijo dadas.

* **Actividades principales:**

  * Identificación de elementos clave: raíz, nodos internos, hojas, ancestros, descendientes y hermanos.

  * Cálculo de propiedades estructurales: grado de cada nodo, grado del árbol, profundidad y altura.

  * Verificación formal de propiedades (si es binario, completo y balanceado).

  * Análisis de complejidad temporal para conteo, altura y búsqueda exhaustiva.

### `ejer_2/` — Construcción de un Árbol de Expresiones

* **Ubicación:** `ejer_2/`

* **Idea General:** Representación sintáctica de expresiones aritméticas respetando precedencia y asociatividad de operadores.

* **Actividades principales:**

  * Identificación de operandos y operadores para la expresión $(a+3) \times (b-2) + \frac{c}{4}$.

  * Construcción del árbol sintáctico de la expresión.

  * Extracción de notaciones mediante recorridos: preorden (prefija), inorden (infija) y postorden (postfija).

  * Evaluación del árbol mediante recorrido postorden para valores concretos de $a, b, c$.

  * Análisis de complejidad espacial y efecto del desbalanceo en memoria de pila.

### `ejer_3/` — Recorridos en Profundidad: DFS

* **Ubicación:** `ejer_3/`

* **Idea General:** Implementación de la estructura de árbol general ($n$-ario) y algoritmos basados en exploración en profundidad.

* **Actividades principales:**

  * Definición de nodos con soporte para número arbitrario de hijos.

  * Implementación de DFS recursivo e iterativo con pila LIFO.

  * Búsqueda de valores, conteo de hojas y cálculo de altura.

  * Comparativa de consumo de memoria entre recursión e iteración, y análisis frente a árboles balanceados vs. desbalanceados.

### `ejer_4/` — Recorrido en Anchura: BFS

* **Ubicación:** `ejer_4/`

* **Idea General:** Procesamiento por niveles (estratos horizontales) de un árbol general utilizando una cola FIFO.

* **Actividades principales implementadas:**

  * Implementación de BFS recibiendo la raíz y visitando ordenadamente por niveles.

  * Impresión de nodos agrupados por nivel y orden de visita global.

  * Búsqueda con reporte del nivel de coincidencia y conteo de nodos examinados.

  * Análisis conceptual sobre el rol de la cola vs. pila, consumo de memoria en árboles anchos y optimalidad en caminos mínimos.

###  `ejer_5/` — Aplicación al Análisis Sintáctico y Comparación Final

* **Ubicación:** `ejer_5/`

* **Idea General:** Integración de la teoría de árboles en el análisis sintáctico descendente para una gramática libre de contexto ($E, T, F$).

* **Actividades principales:**

  * Construcción paso a paso del árbol sintáctico para la cadena `id + id * id`.

  * Comparación entre el orden de creación de nodos y el recorrido preorden.

  * Demostración de cómo la estructura del árbol modela la precedencia de operadores ($*$ sobre $+$).

  * Tabla comparativa global entre DFS y BFS, y conclusión sobre la pertinencia en analizadores descendentes.

