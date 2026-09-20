

from collections import deque


class Nodo:
    """Nodo para arboles generales (m-arios)."""

    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)


class NodoExpresion:
    """Nodo binario para el arbol de expresiones aritmeticas."""

    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der



# PUNTO 1: Construccion del arbol general de prueba

def construir_arbol_punto1():
    """Construye el arbol general con las relaciones padre-hijo del Punto 1."""
    a = Nodo("A")
    b = Nodo("B")
    c = Nodo("C")
    d = Nodo("D")
    e = Nodo("E")
    f = Nodo("F")
    g = Nodo("G")
    h = Nodo("H")
    i = Nodo("I")
    j = Nodo("J")
    k = Nodo("K")
    l = Nodo("L")

    a.agregar_hijo(b)
    a.agregar_hijo(c)
    a.agregar_hijo(d)

    b.agregar_hijo(e)
    b.agregar_hijo(f)

    c.agregar_hijo(g)

    d.agregar_hijo(h)
    d.agregar_hijo(i)

    f.agregar_hijo(j)

    h.agregar_hijo(k)
    h.agregar_hijo(l)

    return a


# PUNTO 2: Arbol de expresiones y evaluacion

def construir_arbol_expresion():
    """Construye el arbol de expresion para: (a + 3) * (b - 2) + c / 4."""
    sum1 = NodoExpresion("+", NodoExpresion("a"), NodoExpresion("3"))
    res1 = NodoExpresion("-", NodoExpresion("b"), NodoExpresion("2"))
    mult = NodoExpresion("*", sum1, res1)
    div1 = NodoExpresion("/", NodoExpresion("c"), NodoExpresion("4"))
    return NodoExpresion("+", mult, div1)


def preorden_expresion(nodo):
    """Recorrido preorden (Prefija): raiz -> izq -> der."""
    if not nodo:
        return []
    return [nodo.valor] + preorden_expresion(nodo.izq) + preorden_expresion(nodo.der)


def inorden_expresion(nodo):
    """Recorrido inorden (Infija con parentesis para precedencia)."""
    if not nodo:
        return []
    if not nodo.izq and not nodo.der:
        return [nodo.valor]
    return ["("] + inorden_expresion(nodo.izq) + [nodo.valor] + inorden_expresion(nodo.der) + [")"]


def postorden_expresion(nodo):
    """Recorrido postorden (Postfija): izq -> der -> raiz."""
    if not nodo:
        return []
    return postorden_expresion(nodo.izq) + postorden_expresion(nodo.der) + [nodo.valor]


def evaluar_expresion(nodo, valores):
    """Evalua la expresion recorriendo el arbol en postorden."""
    if not nodo.izq and not nodo.der:
        if nodo.valor in valores:
            return float(valores[nodo.valor])
        return float(nodo.valor)

    val_izq = evaluar_expresion(nodo.izq, valores)
    val_der = evaluar_expresion(nodo.der, valores)

    if nodo.valor == "+":
        return val_izq + val_der
    elif nodo.valor == "-":
        return val_izq - val_der
    elif nodo.valor == "*":
        return val_izq * val_der
    elif nodo.valor == "/":
        return val_izq / val_der
    return 0.0



# PUNTO 3: Recorridos en profundidad (DFS)

def dfs_recursivo(nodo, visitados=None):
    """DFS recursivo en preorden sobre arbol general."""
    if visitados is None:
        visitados = []
    visitados.append(nodo.valor)
    for hijo in nodo.hijos:
        dfs_recursivo(hijo, visitados)
    return visitados


def dfs_iterativo(raiz):
    """DFS iterativo utilizando una pila explicita (LIFO)."""
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
    """Busqueda de un nodo usando DFS, retornando si existe y nodos visitados."""
    if not raiz:
        return False, 0, []
    pila = [raiz]
    visitados = []
    encontrado = False

    while pila:
        actual = pila.pop()
        visitados.append(actual.valor)
        if actual.valor == valor_buscado:
            encontrado = True
            break
        for hijo in reversed(actual.hijos):
            pila.append(hijo)

    return encontrado, len(visitados), visitados


def contar_hojas_dfs(nodo):
    """Cuenta los nodos hoja (sin hijos) en el arbol."""
    if not nodo:
        return 0
    if not nodo.hijos:
        return 1
    total = 0
    for hijo in nodo.hijos:
        total += contar_hojas_dfs(hijo)
    return total


def calcular_altura_dfs(nodo):
    """Calcula la altura del arbol (longitud en aristas desde raiz hasta la hoja mas lejana)."""
    if not nodo or not nodo.hijos:
        return 0
    return 1 + max(calcular_altura_dfs(hijo) for hijo in nodo.hijos)



# PUNTO 4: Recorrido en anchura (BFS)

def bfs_niveles(raiz):
    """Recorrido en anchura usando una cola FIFO (deque), agrupando por niveles."""
    if not raiz:
        return {}, []
    cola = deque([(raiz, 0)])
    niveles = {}
    orden_visita = []

    while cola:
        actual, nivel = cola.popleft()
        orden_visita.append(actual.valor)

        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(actual.valor)

        for hijo in actual.hijos:
            cola.append((hijo, nivel + 1))

    return niveles, orden_visita


def buscar_bfs(raiz, valor_buscado):
    """Busqueda en anchura con cola, reportando nivel y nodos visitados."""
    if not raiz:
        return False, None, 0, []
    cola = deque([(raiz, 0)])
    visitados = []
    encontrado = False
    nivel_hallado = None

    while cola:
        actual, nivel = cola.popleft()
        visitados.append(actual.valor)
        if actual.valor == valor_buscado:
            encontrado = True
            nivel_hallado = nivel
            break
        for hijo in actual.hijos:
            cola.append((hijo, nivel + 1))

    return encontrado, nivel_hallado, len(visitados), visitados



# PUNTO 5: Aplicacion al analisis sintactico descendente

def construir_arbol_sintactico():
    """Construye el arbol sintactico para 'id + id * id' segun la gramatica dada."""
    e = Nodo("E")
    t1 = Nodo("T")
    ep1 = Nodo("E'")
    e.agregar_hijo(t1)
    e.agregar_hijo(ep1)

    f1 = Nodo("F")
    tp1 = Nodo("T'")
    t1.agregar_hijo(f1)
    t1.agregar_hijo(tp1)

    id1 = Nodo("id")
    f1.agregar_hijo(id1)

    eps1 = Nodo("ε")
    tp1.agregar_hijo(eps1)

    mas = Nodo("+")
    t2 = Nodo("T")
    ep2 = Nodo("E'")
    ep1.agregar_hijo(mas)
    ep1.agregar_hijo(t2)
    ep1.agregar_hijo(ep2)

    f2 = Nodo("F")
    tp2 = Nodo("T'")
    t2.agregar_hijo(f2)
    t2.agregar_hijo(tp2)

    id2 = Nodo("id")
    f2.agregar_hijo(id2)

    por = Nodo("*")
    f3 = Nodo("F")
    tp3 = Nodo("T'")
    tp2.agregar_hijo(por)
    tp2.agregar_hijo(f3)
    tp2.agregar_hijo(tp3)

    id3 = Nodo("id")
    f3.agregar_hijo(id3)

    eps2 = Nodo("ε")
    tp3.agregar_hijo(eps2)

    eps3 = Nodo("ε")
    ep2.agregar_hijo(eps3)

    return e


def postorden_general(nodo, visitados=None):
    """Recorrido postorden para arbol general (hijos primero, luego raiz)."""
    if visitados is None:
        visitados = []
    for hijo in nodo.hijos:
        postorden_general(hijo, visitados)
    visitados.append(nodo.valor)
    return visitados


def analizar_arbol_sintactico(raiz):
    """Cuenta nodos terminales, no terminales, producciones vacias y altura."""
    terminales = []
    no_terminales = []
    producciones_vacias = []

    def recorrer(nodo):
        if nodo.valor == "ε":
            producciones_vacias.append(nodo.valor)
        elif not nodo.hijos:
            terminales.append(nodo.valor)
        else:
            no_terminales.append(nodo.valor)
        for hijo in nodo.hijos:
            recorrer(hijo)

    recorrer(raiz)
    altura = calcular_altura_dfs(raiz)

    return {
        "terminales": len(terminales),
        "lista_terminales": terminales,
        "no_terminales": len(no_terminales),
        "lista_no_terminales": no_terminales,
        "producciones_vacias": len(producciones_vacias),
        "altura": altura,
    }



# Ejecucion de todas las pruebas requeridas en el taller

def ejecutar_pruebas():
    print("=" * 60)
    print("PUNTO 2: EVALUACION DE ARBOL DE EXPRESIONES")
    print("=" * 60)
    arbol_exp = construir_arbol_expresion()
    prefijo = " ".join(preorden_expresion(arbol_exp))
    infijo = "".join(inorden_expresion(arbol_exp))
    postfijo = " ".join(postorden_expresion(arbol_exp))
    valores = {"a": 5, "b": 8, "c": 12}
    resultado = evaluar_expresion(arbol_exp, valores)
    print(f"Prefija  (Preorden):  {prefijo}")
    print(f"Infija   (Inorden):   {infijo}")
    print(f"Postfija (Postorden): {postfijo}")
    print(f"Evaluacion para a=5, b=8, c=12: {resultado}")

    print("\n" + "=" * 60)
    print("PUNTO 3: RECORRIDOS EN PROFUNDIDAD (DFS)")
    print("=" * 60)
    arbol1 = construir_arbol_punto1()
    orden_rec = dfs_recursivo(arbol1)
    orden_it = dfs_iterativo(arbol1)
    num_hojas = contar_hojas_dfs(arbol1)
    altura = calcular_altura_dfs(arbol1)

    print(f"DFS Recursivo: {', '.join(orden_rec)}")
    print(f"DFS Iterativo: {', '.join(orden_it)}")
    print(f"Numero de hojas: {num_hojas}")
    print(f"Altura del arbol: {altura}")

    casos_prueba = ["B", "L", "Z"]
    print("\nPruebas de busqueda DFS:")
    for val in casos_prueba:
        enc, cant, visitados = buscar_dfs(arbol1, val)
        print("-" * 40)
        print(f"Valor buscado: {val}")
        print(f"Orden de visita: {', '.join(visitados)}")
        print(f"Resultado: {'encontrado' if enc else 'no encontrado'}")
        print(f"Cantidad de nodos visitados: {cant}")

    print("\n" + "=" * 60)
    print("PUNTO 4: RECORRIDO EN ANCHURA (BFS)")
    print("=" * 60)
    niveles, orden_bfs = bfs_niveles(arbol1)
    print("Nodos agrupados por nivel:")
    for n in sorted(niveles.keys()):
        print(f"Nivel {n}: {', '.join(niveles[n])}")
    print(f"Orden de visita BFS: {', '.join(orden_bfs)}")

    print("\nPruebas de busqueda BFS:")
    for val in casos_prueba:
        enc, nivel, cant, visitados = buscar_bfs(arbol1, val)
        print("-" * 40)
        print(f"Valor buscado: {val}")
        print(f"Resultado: {'encontrado' if enc else 'no encontrado'}")
        print(f"Nivel del valor: {nivel if enc else 'N/A'}")
        print(f"Nodos visitados: {cant}")
        print(f"Orden de visita: {', '.join(visitados)}")

    print("\n" + "=" * 60)
    print("PUNTO 5: ANALISIS SINTACTICO DESCENDENTE")
    print("=" * 60)
    arbol_sint = construir_arbol_sintactico()
    dfs_sint_pre = dfs_recursivo(arbol_sint)
    dfs_sint_post = postorden_general(arbol_sint)
    _, bfs_sint = bfs_niveles(arbol_sint)
    analisis = analizar_arbol_sintactico(arbol_sint)

    print(f"DFS Preorden:  {', '.join(dfs_sint_pre)}")
    print(f"DFS Postorden: {', '.join(dfs_sint_post)}")
    print(f"BFS:           {', '.join(bfs_sint)}")
    print(f"Cantidad de nodos terminales: {analisis['terminales']} ({', '.join(analisis['lista_terminales'])})")
    print(f"Cantidad de nodos no terminales: {analisis['no_terminales']} ({', '.join(analisis['lista_no_terminales'])})")
    print(f"Cantidad de producciones vacias (ε): {analisis['producciones_vacias']}")
    print(f"Altura del arbol sintactico: {analisis['altura']}")


if __name__ == "__main__":
    ejecutar_pruebas()
