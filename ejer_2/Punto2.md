# Taller de Árboles - Punto 2: Construcción de un Árbol de Expresiones
**Materia:** Lenguajes de Programación y Traducción  
**Estudiante:** Yeimy Beltrán  

---

## ¿De qué trata este punto?
En este punto nos dan la siguiente expresión matemática:

$$(a + 3) \times (b - 2) + \frac{c}{4}$$

El objetivo es analizar sus partes, armar manualmente el árbol binario de expresión respetando la jerarquía de las operaciones, hacer los tres recorridos principales (preorden, inorden y postorden), y luego calcular el resultado paso a paso evaluando el árbol desde las hojas hasta la raíz con los valores $a = 5$, $b = 8$ y $c = 12$.

---

## 1. Operandos y Operadores

Separé los elementos de la expresión de la siguiente manera:

- **Operandos (los datos con los que se opera):**
  - Variables: **$a$, $b$, $c$**
  - Constantes numéricas: **$3$, $2$, $4$**
  *(En el árbol, todos los operandos siempre quedan como hojas).*

- **Operadores (las operaciones a realizar):**
  - Suma interna: **$+$** (en la operación $a + 3$)
  - Resta interna: **$-$** (en la operación $b - 2$)
  - Multiplicación: **$\times$** o **$*$**
  - División: **$/$** o **$\div$** (en la operación $c / 4$)
  - Suma principal: **$+$** (la que une los dos lados de la expresión)
  *(En el árbol, todos los operadores quedan como nodos internos).*

---

## 2. Construcción Manual del Árbol de Expresión

Para armarlo manualmente respetando la precedencia de los operadores:
1. Lo primero que se debe resolver por estar entre paréntesis son las sumas y restas: $(a + 3)$ y $(b - 2)$.
2. Luego se resuelven las operaciones de mayor prioridad: la multiplicación $\times$ que une ambos paréntesis, y la división $c / 4$.
3. Por último, la operación de menor precedencia que se hace al final de todo es la **suma central $+$**. Como es la última en evaluarse, esa suma debe ser la **raíz principal** del árbol.

### Dibujo del Árbol de Expresión:

![Árbol de Expresión del Punto 2](imagenes/arbol_expresion_punto2.png)

*(En el dibujo puse los operadores en círculos azules como nodos internos y los operandos en círculos amarillos como hojas).*

---

## 3. Recorridos del Árbol

Realicé los tres recorridos siguiendo las reglas de visita:

### A. Preorden (Raíz $\to$ Subárbol Izquierdo $\to$ Subárbol Derecho)
Voy anotando primero la raíz de cada subárbol antes de bajar a sus hijos:
```text
+ * + a 3 - b 2 / c 4
```

### B. Inorden (Subárbol Izquierdo $\to$ Raíz $\to$ Subárbol Derecho)
Visito primero el hijo izquierdo, luego la operación y luego el hijo derecho.  
- Si lo escribo con paréntesis para no perder el orden de las operaciones:
```text
(((a + 3) * (b - 2)) + (c / 4))
```
- Sin paréntesis queda: `a + 3 * b - 2 + c / 4`

### C. Postorden (Subárbol Izquierdo $\to$ Subárbol Derecho $\to$ Raíz)
Resuelvo primero los dos hijos y por último visito la raíz de la operación:
```text
a 3 + b 2 - * c 4 / +
```

---

## 4. Relación con las Notaciones

Cada recorrido corresponde exactamente a una forma estándar de escribir expresiones:

- **El recorrido en Preorden** nos da la **notación prefija** (también llamada Notación Polaca), donde el operador se coloca antes de sus dos operandos.
- **El recorrido en Inorden** nos da la **notación infija**, que es la que usamos normalmente en matemáticas donde el operador va en medio de los dos operandos.
- **El recorrido en Postorden** nos da la **notación postfija** (conocida como Notación Polaca Inversa o RPN), donde el operador va después de sus operandos.

---

## 5. Evaluación Manual del Árbol

Nos piden evaluar el árbol con:
- **$a = 5$**
- **$b = 8$**
- **$c = 12$**

Como la regla del taller dice que debemos hacerlo **recorriendo el árbol** (postorden, de abajo hacia arriba) y no reemplazando en la fórmula original, el proceso paso a paso fue el siguiente:

### Dibujo de la Evaluación Paso a Paso:

![Evaluación Paso a Paso del Árbol de Expresión](imagenes/evaluacion_expresion_punto2.png)

### Paso a paso detallado:
1. **Subárbol izquierdo inferior 1 ($+$):**  
   Operamos sus hojas: $a + 3 = 5 + 3 = \mathbf{8}$.
2. **Subárbol izquierdo inferior 2 ($-$):**  
   Operamos sus hojas: $b - 2 = 8 - 2 = \mathbf{6}$.
3. **Subárbol de la multiplicación ($\times$):**  
   Multiplicamos los dos resultados anteriores: $8 \times 6 = \mathbf{48}$.
4. **Subárbol derecho de la división ($/$):**  
   Operamos sus hojas: $c / 4 = 12 / 4 = \mathbf{3}$.
5. **Raíz principal ($+$):**  
   Sumamos el resultado del lado izquierdo con el del lado derecho:  
   $$48 + 3 = \mathbf{51}$$

**Resultado final:** **51**

---

## 6. Preguntas de Análisis

### 1. ¿Por qué la evaluación de una expresión puede realizarse mediante un recorrido en postorden?
Porque para poder hacer cualquier operación matemática (como sumar, multiplicar o dividir), primero necesitamos conocer obligatoriamente los dos números sobre los cuales se va a operar. El recorrido en postorden hace exactamente eso: primero visita y calcula todo el subárbol izquierdo, luego todo el subárbol derecho, y al final procesa el operador con esos dos valores ya listos.

### 2. ¿Cuál es la complejidad temporal de evaluar el árbol?
Es **$O(N)$**, donde $N$ es la cantidad total de nodos que tiene el árbol (en este ejercicio son 11 nodos: 5 operadores y 6 operandos). Esto es porque cada nodo se visita y se evalúa una sola vez con operaciones simples de tiempo constante.

### 3. ¿Cuál es la complejidad espacial del recorrido recursivo en función de $h$?
Es **$O(h)$**, donde $h$ es la altura del árbol (en este caso $h = 3$). Esto pasa porque cuando una función recursiva se llama a sí misma, las llamadas que quedan pendientes en memoria corresponden a la profundidad de la rama por la que va bajando en ese instante.

### 4. ¿Qué ocurre con el consumo de memoria si el árbol está completamente desbalanceado?
Si el árbol está desbalanceado (por ejemplo, si fuera una rama larga hacia un solo lado donde cada nodo solo tiene un hijo), la altura $h$ se vuelve igual al total de nodos ($h = N$). En ese caso, la memoria de la recursión crecería hasta **$O(N)$**, consumiendo mucha más memoria y pudiendo generar un error de desbordamiento de pila (*RecursionError* o *stack overflow*) si la expresión fuera muy grande.
