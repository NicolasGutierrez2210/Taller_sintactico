"""
Punto 4: Recorrido en anchura (BFS) en Árbol General (N-ario)

Requerimientos implementados:
1. Recibir como entrada la raíz del árbol.
2. Visitar los nodos nivel por nivel.
3. Mostrar el orden de visita general.
4. Mostrar los nodos agrupados por nivel.
5. Permitir buscar un valor.
6. Informar el nivel en el que se encontró el valor.
7. Mostrar la cantidad de nodos visitados.
Formato de salida estricto según la plantilla del enunciado.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Tuple


class NodoArbol:
    """
    Representa un nodo de un árbol general (n-ario).
    Almacena un valor y una lista de referencias a sus nodos hijos.
    """
    def __init__(self, valor: Any):
        self.valor: Any = valor
        self.hijos: List['NodoArbol'] = []

    def agregar_hijo(self, hijo: 'NodoArbol') -> None:
        """Añade un hijo al nodo manteniendo el orden de inserción (izquierda a derecha)."""
        self.hijos.append(hijo)

    def __repr__(self) -> str:
        return f"Nodo({self.valor})"



# 1. Recorrido BFS por Niveles (Requisitos 1, 2, 3 y 4)

def bfs_por_niveles(raiz: Optional[NodoArbol]) -> Tuple[List[Any], Dict[int, List[Any]]]:
    """
    Ejecuta el recorrido en anchura (BFS) utilizando una cola FIFO.
    
    Retorna:
      - orden_visita: Lista con todos los valores en el orden exacto en que fueron visitados.
      - niveles: Diccionario donde cada clave es el número de nivel (0, 1, 2, ...)
                 y su valor es la lista de nodos pertenecientes a dicho nivel.
    """
    if raiz is None:
        return [], {}

    # La cola almacena tuplas: (nodo_actual, nivel_actual)
    cola: deque[Tuple[NodoArbol, int]] = deque([(raiz, 0)])
    orden_visita: List[Any] = []
    niveles: Dict[int, List[Any]] = {}

    while cola:
        actual, nivel = cola.popleft()

        # Registrar orden de visita
        orden_visita.append(actual.valor)

        # Agrupar por nivel
        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(actual.valor)

        # Encolar los hijos para el siguiente nivel (nivel + 1)
        for hijo in actual.hijos:
            cola.append((hijo, nivel + 1))

    return orden_visita, niveles



# 2. Búsqueda mediante BFS (Requisitos 5, 6 y 7)

def buscar_bfs(raiz: Optional[NodoArbol], valor_buscado: Any) -> Tuple[bool, Optional[int], int, List[Any]]:
    """
    Busca un valor en el árbol mediante BFS utilizando una cola FIFO.
    
    Retorna:
      - encontrado (bool): True si el valor existe en el árbol, False en caso contrario.
      - nivel_encontrado (int o None): El nivel en el que se ubica el nodo (None si no existe).
      - nodos_visitados (int): Cantidad de nodos examinados hasta encontrar el valor o agotar el árbol.
      - orden_visita (list): Secuencia de nodos visitados durante la exploración.
    """
    if raiz is None:
        return False, None, 0, []

    cola: deque[Tuple[NodoArbol, int]] = deque([(raiz, 0)])
    nodos_visitados = 0
    orden_visita: List[Any] = []

    while cola:
        actual, nivel = cola.popleft()
        nodos_visitados += 1
        orden_visita.append(actual.valor)

        if actual.valor == valor_buscado:
            return True, nivel, nodos_visitados, orden_visita

        for hijo in actual.hijos:
            cola.append((hijo, nivel + 1))

    return False, None, nodos_visitados, orden_visita



# 3. Presentación de la salida con el formato del taller

def imprimir_reporte_bfs(raiz: Optional[NodoArbol], valor_buscado: Any) -> None:
    """
    Imprime los resultados del BFS respetando estrictamente la estructura 
    definida en la guía del taller.
    """
    orden_visita, niveles = bfs_por_niveles(raiz)
    encontrado, nivel_hallado, visitados, _ = buscar_bfs(raiz, valor_buscado)

    # Mostrar nodos agrupados por nivel
    for nivel, nodos in sorted(niveles.items()):
        print(f"Nivel {nivel}: {', '.join(str(v) for v in nodos)}")

    print(f"\nOrden de visita: {' -> '.join(str(v) for v in orden_visita)}")

    # Bloque de búsqueda según la plantilla del enunciado
    print(f"\nValor buscado: {valor_buscado}")
    print(f"Resultado: {'encontrado' if encontrado else 'no encontrado'}")
    print(f"Nivel del valor: {nivel_hallado if encontrado else 'No aplica'}")
    print(f"Nodos visitados: {visitados}")



# 4. Construcción del Árbol de Prueba del Taller

def construir_arbol_ejemplo() -> NodoArbol:
    """
    Construye el árbol general definido en el Punto 1 del taller:
      A -> B, C, D
      B -> E, F
      C -> G
      D -> H, I
      F -> J
      H -> K, L
    """
    nodos = {letra: NodoArbol(letra) for letra in "ABCDEFGHIJKL"}

    nodos['A'].agregar_hijo(nodos['B'])
    nodos['A'].agregar_hijo(nodos['C'])
    nodos['A'].agregar_hijo(nodos['D'])

    nodos['B'].agregar_hijo(nodos['E'])
    nodos['B'].agregar_hijo(nodos['F'])

    nodos['C'].agregar_hijo(nodos['G'])

    nodos['D'].agregar_hijo(nodos['H'])
    nodos['D'].agregar_hijo(nodos['I'])

    nodos['F'].agregar_hijo(nodos['J'])

    nodos['H'].agregar_hijo(nodos['K'])
    nodos['H'].agregar_hijo(nodos['L'])

    return nodos['A']


#  Demostración Principal

if __name__ == "__main__":
    arbol = construir_arbol_ejemplo()

 
    print(" REPORTE BFS - EJECUCIÓN (CASO: VALOR EXISTENTE)")

    imprimir_reporte_bfs(arbol, valor_buscado='G')

   
    print(" REPORTE BFS - EJECUCIÓN (CASO: VALOR EN ÚLTIMO NIVEL)")
   
    imprimir_reporte_bfs(arbol, valor_buscado='K')


    print(" REPORTE BFS - EJECUCIÓN (CASO: VALOR INEXISTENTE)")
 
    imprimir_reporte_bfs(arbol, valor_buscado='X')
