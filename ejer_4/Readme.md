
## Punto 4. Recorrido en Anchura: BFS en Árboles Generales

**Curso:** Lenguajes de Programación y Traducción  
**Tema:** Estructuras de datos para el análisis sintáctico descendente  
**Módulo:** Punto 4 (Implementación de BFS, Preguntas de Análisis y Salida Estructurada)

---

## 1. Justificación y Fundamentación Teórica

### ¿Por qué se hizo? (Fundamento Teórico)
En la teoría de lenguajes y compiladores, un árbol de derivación o sintaxis abstracta representa la estructura jerárquica de un programa. Mientras que el recorrido en profundidad (DFS) profundiza rama por rama, el **Recorrido en Anchura (Breadth-First Search - BFS)** explora el árbol **estrato por estrato**, procesando todos los nodos que se encuentran a una distancia de $d$ aristas de la raíz antes de acceder a cualquier nodo situado a distancia $d+1$.

Este enfoque es fundamental cuando se desea:
1. **Analizar la estructura por capas de abstracción:** Observar la expansión de reglas gramaticales nivel a nivel.
2. **Optimización de caminos mínimos:** Encontrar el nodo más cercano a la raíz (menor profundidad) que satisfaga una propiedad dada sin caer en ramas infinitas o de profundidad arbitraria.

### ¿Para qué se hizo? (Objetivo Práctico)
1. **Cumplir los 7 requerimientos del Punto 4:**
   - Recibir la raíz de un árbol general ($n$-ario).
   - Visitar los nodos nivel por nivel.
   - Mostrar el orden de visita global.
   - Agrupar e imprimir los nodos de cada nivel independiente.
   - Implementar un motor de búsqueda por anchura.
   - Identificar con precisión el nivel en el que reside el valor buscado.
   - Contabilizar el número de nodos inspeccionados hasta dar con el objetivo o determinar su inexistencia.
2. **Validar el formato de salida formal** estipulado en la guía del taller.
3. **Analizar el comportamiento de memoria y tiempo** de las estructuras FIFO frente a LIFO.

### ¿Cómo se llegó a la solución? (Metodología y Diseño)
1. **Estructura de Datos Dinámica:** Se utilizó la clase `NodoArbol`, permitiendo que cada nodo almacene un valor escalar y una lista dinámica de punteros a sus hijos directos (`hijos: List[NodoArbol]`).
2. **Uso de Cola FIFO (`collections.deque`):** Para garantizar un tiempo de inserción y extracción $\mathcal{O}(1)$ amortizado por nodo, se empleó una cola de doble extremo (`deque`) operada estrictamente como FIFO (`append` al final, `popleft` al inicio).
3. **Seguimiento Explícito de Niveles:** Para resolver los puntos 4 y 6 simultáneamente, cada elemento encolado es una tupla `(nodo, nivel)`. La raíz entra con `nivel = 0`, y al expandir sus hijos, estos ingresan con `nivel + 1`.
4. **Búsqueda con Parada Temprana (*Early Exit*):** La función `buscar_bfs` detiene el procesamiento en el instante exacto en que encuentra el valor, registrando la cantidad de nodos visitados y el nivel del hallazgo.

---

## 2. Estructura del Árbol General Analizado

El árbol evaluado corresponde a la estructura jerárquica general con relaciones padre-hijo del taller:

```text
Nivel 0 (Raíz):                     [A]
                               /     |     \
                             /       |       \
Nivel 1:                   [B]      [C]      [D]
                          /   \      |      /   \
Nivel 2:                [E]   [F]   [G]   [H]   [I]
                               |          / \
Nivel 3:                      [J]       [K] [L]
```

### Clasificación por Niveles
- **Nivel 0:** $A$
- **Nivel 1:** $B, C, D$
- **Nivel 2:** $E, F, G, H, I$
- **Nivel 3:** $J, K, L$

---

## 3. Salida del Programa (Formato del Taller)

El programa genera la salida respetando fielmente la estructura exigida en el taller:

```text
=================================================================
 REPORTE BFS - EJECUCIÓN (CASO: VALOR EXISTENTE)
=================================================================
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L

Orden de visita: A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L

Valor buscado: G
Resultado: encontrado
Nivel del valor: 2
Nodos visitados: 7

=================================================================
 REPORTE BFS - EJECUCIÓN (CASO: VALOR EN ÚLTIMO NIVEL)
=================================================================
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L

Orden de visita: A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L

Valor buscado: K
Resultado: encontrado
Nivel del valor: 3
Nodos visitados: 11

=================================================================
 REPORTE BFS - EJECUCIÓN (CASO: VALOR INEXISTENTE)
=================================================================
Nivel 0: A
Nivel 1: B, C, D
Nivel 2: E, F, G, H, I
Nivel 3: J, K, L

Orden de visita: A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L

Valor buscado: X
Resultado: no encontrado
Nivel del valor: No aplica
Nodos visitados: 12
```

---

## 4. Respuestas Detalladas a las Preguntas de Análisis

A continuación se resuelven de forma exhaustiva y rigurosa las **6 preguntas de análisis** planteadas en la página 4 y 5 del taller:

### 1. ¿Por qué BFS requiere una cola?
BFS exige procesar los nodos en orden estricto de llegada: **Primero en Entrar, Primero en Salir (FIFO - First In, First Out)**. 
Para garantizar que todos los nodos a profundidad $d$ sean visitados antes de tocar cualquier nodo a profundidad $d+1$, los hijos de los nodos del nivel $d$ deben ser puestos "a la espera" detrás de los nodos que ya estaban en ese mismo nivel. Una cola asegura que los nodos del nivel superior se desencolen y procesen por completo antes de que llegue el turno de los nodos del nivel inferior.

### 2. ¿Qué sucedería si se utilizara una pila?
Si la cola FIFO se reemplaza por una pila LIFO (Last In, First Out), el orden de extracción cambia por completo: el último nodo ingresado sería el primero en ser procesado.
Como consecuencia directa:
- El algoritmo deja de ser un recorrido en anchura y **se transforma en un recorrido en profundidad (DFS)**.
- En lugar de avanzar nivel por nivel horizontalmente, la ejecución descenderá inmediatamente hacia las hojas a lo largo de la rama más recientemente descubierta.

### 3. ¿Cuál es la complejidad temporal de BFS?
La complejidad temporal de BFS en un árbol general es:
$$\mathcal{O}(N)$$
donde $N$ representa el número total de nodos del árbol.
**Justificación:** Cada nodo entra a la cola exactamente una vez y sale de la cola exactamente una vez. Además, para cada nodo se recorre su lista de hijos para encolarlos; la suma de las longitudes de todas las listas de hijos es igual al número de aristas del árbol, que en cualquier árbol conectado y acíclico es exactamente $N - 1$. Por lo tanto, el número total de operaciones es proporcional a $N + (N - 1) \in \mathcal{O}(N)$.

### 4. ¿Cuál es su complejidad espacial?
La complejidad espacial de BFS está dominada por la cantidad máxima de nodos almacenados simultáneamente en la cola auxiliar:
$$\mathcal{O}(W)$$
donde $W$ es el **ancho máximo del árbol** (*maximum width*), es decir, el número máximo de nodos presentes en un mismo nivel.
- En el mejor caso (árbol degenerado en lista, un hijo por nodo): $W = 1 \implies \mathcal{O}(1)$.
- En un árbol $k$-ario completo o balanceado con factor de ramificación $b$: el último nivel contiene aproximadamente $\frac{b-1}{b} N$ nodos, lo que implica que en el peor caso espacial:
$$\mathcal{O}(W) = \mathcal{O}(N)$$

### 5. ¿Cuál recorrido puede consumir más memoria en un árbol ancho: DFS o BFS?
**En un árbol ancho, el recorrido BFS consume considerablemente más memoria que DFS.**
- **Análisis de BFS:** En un árbol de poca profundidad pero con un factor de ramificación muy alto (por ejemplo, una raíz con 100,000 hijos), BFS debe almacenar simultáneamente en la cola a los 100,000 hijos antes de procesar el nivel siguiente, consumiendo memoria del orden $\mathcal{O}(N)$.
- **Análisis de DFS:** Por su parte, DFS únicamente mantiene en memoria la ruta activa desde la raíz hasta el nodo actual (la profundidad del camino). Si el árbol tiene altura $h = 1$, la pila de DFS sólo almacena $\mathcal{O}(h)$ elementos en la pila de activación (apenas 1 o 2 llamadas activas).
Por lo tanto, ante estructuras anchas y poco profundas, BFS satura la memoria con rapidez mientras que DFS opera con consumo prácticamente despreciable.

### 6. Si se busca el nodo menos profundo que cumpla una condición, ¿qué recorrido resulta más apropiado? Justifique.
**El recorrido más apropiado es BFS (anchura).**
**Justificación:**
1. **Garantía de Optimalidad:** BFS explora exhaustivamente los nodos en orden no decreciente de profundidad ($d = 0, 1, 2, \dots$). En consecuencia, el primer nodo que coincida con el predicado de búsqueda es **estrictamente el de menor profundidad** (camino más corto en número de aristas desde la raíz).
2. **Prevención de bucles o ramas infinitas:** DFS puede descender miles de niveles por una rama infructuosa antes de retroceder (*backtracking*), consumiendo tiempo y memoria innecesarios aun cuando la respuesta óptima se encontraba en el nivel 1 en una rama adyacente.

---

## 5. Tabla Comparativa de Complejidad de Recorridos

| Criterio | DFS (Profundidad) | BFS (Anchura) |
| :--- | :--- | :--- |
| **Estructura auxiliar** | Pila LIFO (o Call Stack recursivo) | Cola FIFO |
| **Orden de exploración** | Vertical (hacia las hojas primero) | Horizontal (nivel por nivel) |
| **Complejidad temporal** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Complejidad espacial** | $\mathcal{O}(h)$ (proporcional a la altura) | $\mathcal{O}(W)$ (proporcional al ancho máximo) |
| **Consumo en árbol ancho** | Muy bajo ($\mathcal{O}(h)$ con $h$ pequeño) | Muy alto ($\mathcal{O}(W) \approx \mathcal{O}(N)$) |
| **Consumo en árbol profundo/estrecho** | Alto ($\mathcal{O}(N)$ si está desbalanceado) | Muy bajo ($\mathcal{O}(1)$ a $\mathcal{O}(k)$) |
| **Búsqueda del nodo menos profundo** | No óptimo (puede explorar ramas profundas) | **Óptimo y garantizado** |

---

## 6. Guía de Ejecución

### Requisitos
- Tener instalado Python versión 3.8 o superior.
- No se requieren librerías de terceros (se utiliza únicamente la biblioteca estándar).

### Instrucciones de Ejecución
1. Guardar los archivos `punto4_bfs.py` y `README.md` en el mismo directorio.
2. Abrir una terminal o consola de comandos en esa ubicación.
3. Ejecutar el script:
   - En Windows:
     ```bash
     python punto4_bfs.py
     ```
   - En Linux / macOS:
     ```bash
     python3 punto4_bfs.py
     ```
4. El programa ejecutará las pruebas y desplegará en consola la separación por niveles, el orden de visita general y los 3 escenarios de búsqueda con el formato formal requerido.
