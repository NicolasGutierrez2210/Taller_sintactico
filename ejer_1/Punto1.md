# Taller de Árboles - Punto 1: Conceptos y Representación
**Materia:** Lenguajes de Programación y Traducción  
**Estudiante:** Yeimy Beltrán  

---

## ¿De qué trata este punto?
En este primer punto nos dan una lista con las relaciones entre nodos padre e hijos para armar un árbol general. A partir de esa información, dibujé el árbol a mano/diagrama y respondí las preguntas sobre sus partes, relaciones, medidas y clasificación.

Las relaciones que nos dieron fueron:
- **A** es padre de: **B, C, D**
- **B** es padre de: **E, F**
- **C** es padre de: **G**
- **D** es padre de: **H, I**
- **F** es padre de: **J**
- **H** es padre de: **K, L**

---

## 1. Dibujo del Árbol

Aquí está el árbol dibujado con sus conexiones, niveles y la diferenciación por colores de la raíz, los nodos internos y las hojas:

![Árbol General del Punto 1](imagenes/arbol_punto1.png)

*(Explicación de cómo lo dibujé: Empecé colocando la raíz **A** arriba en el Nivel 0. Como **A** tiene tres hijos (**B, C, D**), los coloqué en el Nivel 1. Luego fui sacando los hijos de cada uno: de **B** saqué a **E** y **F**, de **C** saqué a **G**, y de **D** saqué a **H** e **I** en el Nivel 2. Por último, en el Nivel 3 dibujé a **J** que es hijo de **F**, y a **K** y **L** que son hijos de **H**).*

---

## 2. Partes del Árbol y Relaciones entre Nodos

### Identificación general:
- **Raíz:** **A** (es el nodo de donde empieza todo el árbol y no tiene ningún padre).
- **Hojas:** **E, G, I, J, K, L** (son los nodos finales que ya no tienen ningún hijo, en total son 6 hojas).
- **Nodos internos:** **B, C, D, F, H** (y también **A**, son los nodos que tienen al menos un hijo conectado).

### Preguntas específicas de relaciones:
- **¿Quién es el padre de J?**  
  El padre de **J** es **F**.
- **¿Cuáles son los ancestros de L?**  
  Son **H, D y A**. (Se obtienen subiendo por la rama desde **L** hasta llegar a la raíz).
- **¿Cuáles son los descendientes de B?**  
  Son **E, F y J**. (Son todos los nodos que nacen o están por debajo de **B**).
- **¿Cuáles son los hermanos de H?**  
  El hermano de **H** es **I** (porque los dos son hijos directos del mismo padre **D**).

---

## 3. Grados, Profundidad y Altura

### Grado de cada nodo (cuántos hijos directos tiene):
- **Grado(A):** 3 (hijos: B, C, D)
- **Grado(B):** 2 (hijos: E, F)
- **Grado(C):** 1 (hijo: G)
- **Grado(D):** 2 (hijos: H, I)
- **Grado(E):** 0 (no tiene hijos)
- **Grado(F):** 1 (hijo: J)
- **Grado(G):** 0
- **Grado(H):** 2 (hijos: K, L)
- **Grado(I):** 0
- **Grado(J):** 0
- **Grado(K):** 0
- **Grado(L):** 0

- **Grado del árbol:** **3** (es el grado más alto que tiene algún nodo en todo el árbol, que en este caso es el nodo **A**).

### Profundidad de los nodos pedidos:
*(Tomando la raíz A en el nivel / profundidad 0)*:
- **Profundidad de A:** **0** (está en la raíz).
- **Profundidad de F:** **2** (camino: A $\to$ B $\to$ F).
- **Profundidad de J:** **3** (camino: A $\to$ B $\to$ F $\to$ J).
- **Profundidad de L:** **3** (camino: A $\to$ D $\to$ H $\to$ L).

### Altura total del árbol:
- **Altura:** **3** (es la distancia o número de aristas desde la raíz **A** hasta las hojas más lejanas que son **J, K o L**).  
*(Nota: si el profesor cuenta la altura por número de niveles de nodos, entonces sería **4**).*

---

## 4. Clasificación del Árbol

- **¿Es binario?**  
  **No**, porque el nodo **A** tiene 3 hijos (**B, C, D**), y la regla de un árbol binario es que cada nodo puede tener como máximo 2 hijos.
- **¿Es completo?**  
  **No**, primero porque ni siquiera es binario, y segundo porque sus niveles no están totalmente llenos ni sus hojas están acomodadas de izquierda a derecha de forma consecutiva.
- **¿Es balanceado?**  
  **No**, porque sus ramas tienen alturas muy distintas. Por ejemplo, por el lado de **C** el camino se termina en el nivel 2 con **G**, mientras que por los lados de **B** y **D** las ramas bajan hasta el nivel 3 con **J, K y L**.

---

## 5. Análisis de Complejidad

**¿Cuál es la complejidad temporal de un algoritmo que visita todos los nodos para contar hojas, calcular la altura o buscar un valor que no está?**

La complejidad es **$O(N)$** (donde $N$ es el total de nodos del árbol, que en este caso son 12).  

La razón es muy sencilla: como este árbol no está ordenado (no es un árbol binario de búsqueda donde uno sabe si irse a la izquierda o a la derecha), para contar cuántas hojas hay, saber qué tan alto es o estar 100% seguros de que un valor no existe, el algoritmo obligatoriamente tiene que pasar y revisar cada uno de los $N$ nodos del árbol al menos una vez. No hay forma de saltarse ninguno.
