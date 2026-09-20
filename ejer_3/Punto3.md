# Taller de Árboles - Punto 3: Recorridos en Profundidad (DFS)
**Materia:** Lenguajes de Programación y Traducción  
**Estudiante:** Yeimy Beltrán  

---

## ¿De qué trata este punto?
En este punto trabajamos con el árbol general del **Punto 1** (un árbol donde cada nodo puede tener cualquier cantidad de hijos). El objetivo fue:
1. Crear en código la estructura del árbol.
2. Implementar el recorrido en profundidad (**DFS**) tanto de manera recursiva como iterativa con una pila.
3. Crear las funciones para buscar valores, contar las hojas y calcular la altura.
4. Realizar las pruebas de búsqueda solicitadas (un nodo cerca a la raíz, uno del último nivel y uno que no exista).
5. Analizar la complejidad y el consumo de memoria.

---

## 1. Cómo representé el Árbol General en Código

Para no complicarnos con librerías raras, armé una clase sencilla en Python llamada `Nodo`. Cada nodo guarda su letra (`valor`) y tiene una lista simple (`hijos`) donde se agregan sus hijos directos:

```python
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []  # Lista con las referencias a sus hijos

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
```

Para armar el árbol del Punto 1, simplemente creé los nodos de la `A` a la `L` y los fui enlazando según el enunciado:
- A tiene como hijos a B, C, D
- B tiene como hijos a E, F
- C tiene a G
- D tiene a H, I
- F tiene a J
- H tiene a K, L

---

## 2. Los Algoritmos de DFS que se Hicieron

### 1. DFS Recursivo (Preorden)
Visita primero el nodo en el que está parado y luego se llama a sí mismo para cada uno de los hijos de la lista, de izquierda a derecha. Es muy corto porque aprovecha la recursión de Python.

### 2. DFS Iterativo (con Pila)
Para hacerlo sin recursión, usé una lista como pila (*stack*, regla LIFO: último en entrar, primero en salir).  
- Saco el nodo que esté en la cima de la pila y lo anoto en la lista de visitados.
- Para que los hijos se visiten de izquierda a derecha (igual que en el recursivo), meto los hijos a la pila en orden invertido (`reversed(nodo.hijos)`), así el primer hijo queda arriba de todo en la pila listo para ser el siguiente.

### 3. Búsqueda con DFS
Es un recorrido que va revisando nodo por nodo. Apenas encuentra el valor que buscamos, se frena inmediatamente y nos dice que lo encontró, devolviendo la lista de los nodos que alcanzó a visitar y la cantidad total de visitas. Si se vacía la pila y no lo encontró, avisa que no existe.

### 4. Conteo de Hojas con DFS
Revisa cada nodo: si su lista de hijos está vacía (`not nodo.hijos`), significa que es una hoja y cuenta 1. Si tiene hijos, suma recursivamente las hojas de todos ellos.

### 5. Cálculo de la Altura con DFS
Si el nodo es una hoja su altura es 0. Si tiene hijos, calcula la altura máxima entre sus hijos y le suma 1 ($1 + \max(\text{alturas})$).

---

## 3. Dibujo del Recorrido DFS (Orden de Visita)

En el siguiente dibujo muestro el camino que sigue DFS bajando siempre por la rama izquierda hasta el fondo antes de devolverse (*backtracking*):

![Recorrido DFS Preorden](imagenes/recorrido_dfs_punto3.png)

### Secuencia del recorrido completo:
$$\text{A } (\#1) \to \text{B } (\#2) \to \text{E } (\#3) \to \text{F } (\#4) \to \text{J } (\#5) \to \text{C } (\#6) \to \text{G } (\#7) \to \text{D } (\#8) \to \text{H } (\#9) \to \text{K } (\#10) \to \text{L } (\#11) \to \text{I } (\#12)$$

- **Resultado DFS Recursivo:** `A, B, E, F, J, C, G, D, H, K, L, I`
- **Resultado DFS Iterativo:** `A, B, E, F, J, C, G, D, H, K, L, I`  
*(Ambos dieron exactamente el mismo resultado).*

### Propiedades calculadas del árbol:
- **Número de hojas:** **6** (son los nodos: E, G, I, J, K, L).
- **Altura del árbol:** **3** (camino más largo: A $\to$ B $\to$ F $\to$ J o A $\to$ D $\to$ H $\to$ L).

---

## 4. Pruebas de Búsqueda Solicitadas

Nos pidieron probar tres casos de búsqueda en el árbol. Aquí está la visualización gráfica de qué nodos visitó en cada prueba:

![Visualización de Pruebas de Búsqueda DFS](imagenes/busqueda_dfs_pruebas_punto3.png)

### Detalle de cada caso:

#### Prueba 1: Valor cercano a la raíz (`B`)
- **Valor buscado:** `B`
- **Orden de visita:** `A, B`
- **¿Fue encontrado?:** Sí (encontrado).
- **Cantidad de nodos visitados:** **2**
*(Como B es el primer hijo directo de la raíz, lo encuentra casi de inmediato).*

#### Prueba 2: Valor del último nivel (`L`)
- **Valor buscado:** `L`
- **Orden de visita:** `A, B, E, F, J, C, G, D, H, K, L`
- **¿Fue encontrado?:** Sí (encontrado).
- **Cantidad de nodos visitados:** **11**
*(Tuvo que recorrer primero todas las ramas de B y de C completas, bajar por D y por H, pasar por K y finalmente llegar a L).*

#### Prueba 3: Valor que no existe (`Z`)
- **Valor buscado:** `Z`
- **Orden de visita:** `A, B, E, F, J, C, G, D, H, K, L, I`
- **¿Fue encontrado?:** No (no encontrado).
- **Cantidad de nodos visitados:** **12** (visitó todos los nodos del árbol para confirmar que no estaba).

---

## 5. Análisis de Complejidad

### Tabla de complejidad para operaciones con DFS:

| Operación con DFS | Mejor caso | Peor caso | Espacio en memoria |
| :--- | :---: | :---: | :---: |
| **Recorrer todo el árbol** | $O(N)$ | $O(N)$ | $O(h)$ |
| **Buscar un valor** | $O(1)$ *(si está en la raíz)* | $O(N)$ *(si es el último o no está)* | $O(h)$ |
| **Contar hojas** | $O(N)$ | $O(N)$ | $O(h)$ |
| **Calcular la altura** | $O(N)$ | $O(N)$ | $O(h)$ |

### Explicación del uso de memoria:

1. **DFS Recursivo vs. DFS Iterativo:**
   - En el **DFS recursivo**, la memoria la maneja automáticamente Python en su pila de llamadas internas (*call stack*). Si el árbol fuera exageradamente profundo, Python podría botar un error de límite de recursión (`RecursionError`).
   - En el **DFS iterativo**, la memoria la manejamos nosotros con una lista normal que hace de pila. La ventaja es que no tenemos el límite de llamadas del sistema.
   - En ambos casos, el consumo máximo de memoria es **$O(h)$** (la altura de la rama activa), porque en la pila solo se guardan los nodos del camino que va desde la raíz hasta el nodo que se está revisando en ese momento.

2. **Árbol Balanceado vs. Árbol Desbalanceado:**
   - En un **árbol balanceado**, la altura es bajita ($h \approx \log N$), así que la pila solo necesita guardar poquitos nodos a la vez (por ejemplo, en un árbol de 1000 nodos balanceados, la altura sería apenas de unos 10 niveles).
   - En un **árbol completamente desbalanceado** (como una línea recta donde cada nodo solo tiene un hijo hacia abajo), la altura es igual al total de nodos ($h = N$). En ese caso la memoria de la pila se dispara a **$O(N)$**, guardando casi todo el árbol en la memoria al mismo tiempo.

---

## 6. Código en Python

Dejo aquí el código limpio y ordenado que programé para este punto:

```python
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def dfs_recursivo(nodo, visitados=None):
    if visitados is None:
        visitados = []
    visitados.append(nodo.valor)
    for hijo in nodo.hijos:
        dfs_recursivo(hijo, visitados)
    return visitados

def dfs_iterativo(raiz):
    if not raiz:
        return []
    visitados = []
    pila = [raiz]
    while pila:
        actual = pila.pop()
        visitados.append(actual.valor)
        for hijo in reversed(actual.hijos):
            pila.append(hijo)
    return visitados

def buscar_dfs(raiz, valor_buscado):
    pila = [raiz]
    visitados = []
    while pila:
        actual = pila.pop()
        visitados.append(actual.valor)
        if actual.valor == valor_buscado:
            return True, len(visitados), visitados
        for hijo in reversed(actual.hijos):
            pila.append(hijo)
    return False, len(visitados), visitados

def contar_hojas_dfs(nodo):
    if not nodo.hijos:
        return 1
    return sum(contar_hojas_dfs(hijo) for hijo in nodo.hijos)

def calcular_altura_dfs(nodo):
    if not nodo.hijos:
        return 0
    return 1 + max(calcular_altura_dfs(hijo) for hijo in nodo.hijos)
```
