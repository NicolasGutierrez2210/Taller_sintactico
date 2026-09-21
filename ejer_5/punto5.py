#!/usr/bin/env python3

import sys
import os

# Asegurar codificación UTF-8 en consola para símbolos como ε y tildes
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import matplotlib.pyplot as plt


class NodeType(Enum):
    NON_TERMINAL = "No Terminal"
    TERMINAL = "Terminal"
    EPSILON = "Producción Vacía (ε)"


@dataclass
class SyntaxTreeNode:
    symbol: str
    node_type: NodeType
    creation_id: int
    children: List['SyntaxTreeNode'] = field(default_factory=list)
    depth: int = 0
    x: float = 0.0
    y: float = 0.0

    def add_child(self, child: 'SyntaxTreeNode'):
        self.children.append(child)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def __repr__(self):
        return f"{self.symbol}(#{self.creation_id})"


class TopDownParser:
    """
    Simulador de Analizador Sintáctico Descendente Predictivo Recursivo (LL(1)).
    Construye el árbol de análisis sintáctico registrando paso a paso la regla
    aplicada y numerando cada nodo en el momento exacto de su creación.
    """

    def __init__(self, tokens: List[str]):
        self.tokens = tokens + ["$"]  # Marcador de fin de cadena
        self.pos = 0
        self.node_counter = 0
        self.steps_log: List[Dict[str, Any]] = []

    def current_token(self) -> str:
        return self.tokens[self.pos]

    def _next_node_id(self) -> int:
        self.node_counter += 1
        return self.node_counter

    def parse(self) -> SyntaxTreeNode:
        self.steps_log.append({
            "paso": len(self.steps_log) + 1,
            "accion": "Inicio del análisis descendente",
            "simbolo": "E",
            "lookahead": self.current_token(),
            "regla": "Inicio en símbolo inicial E"
        })
        root = self._parse_E()
        if self.current_token() == "$":
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Fin exitoso",
                "simbolo": "$",
                "lookahead": "$",
                "regla": "Cadena completamente consumida y aceptada."
            })
        else:
            raise SyntaxError(f"Error de sintaxis: token no esperado '{self.current_token()}' al final.")
        return root

    def _match(self, expected_token: str) -> SyntaxTreeNode:
        tok = self.current_token()
        if tok == expected_token:
            node_id = self._next_node_id()
            node = SyntaxTreeNode(symbol=tok, node_type=NodeType.TERMINAL, creation_id=node_id)
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Match terminal",
                "simbolo": tok,
                "lookahead": tok,
                "regla": f"Consumir terminal '{tok}' (Nodo #{node_id})"
            })
            self.pos += 1
            return node
        else:
            raise SyntaxError(f"Error sintáctico: Se esperaba '{expected_token}', pero se encontró '{tok}'")

    def _parse_E(self) -> SyntaxTreeNode:
        node_id = self._next_node_id()
        node = SyntaxTreeNode(symbol="E", node_type=NodeType.NON_TERMINAL, creation_id=node_id)
        tok = self.current_token()

        if tok in ["id", "("]:
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "E",
                "lookahead": tok,
                "regla": f"E -> T E' (Nodo #{node_id})"
            })
            node.add_child(self._parse_T())
            node.add_child(self._parse_E_prime())
            return node
        else:
            raise SyntaxError(f"Error en E con lookahead '{tok}'")

    def _parse_E_prime(self) -> SyntaxTreeNode:
        node_id = self._next_node_id()
        node = SyntaxTreeNode(symbol="E'", node_type=NodeType.NON_TERMINAL, creation_id=node_id)
        tok = self.current_token()

        if tok == "+":
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "E'",
                "lookahead": tok,
                "regla": f"E' -> + T E' (Nodo #{node_id})"
            })
            node.add_child(self._match("+"))
            node.add_child(self._parse_T())
            node.add_child(self._parse_E_prime())
            return node
        elif tok in [")", "$"]:
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir a ε",
                "simbolo": "E'",
                "lookahead": tok,
                "regla": f"E' -> ε (por Follow(E')={{$, )}}) (Nodo #{node_id})"
            })
            eps_id = self._next_node_id()
            eps_node = SyntaxTreeNode(symbol="ε", node_type=NodeType.EPSILON, creation_id=eps_id)
            node.add_child(eps_node)
            return node
        else:
            raise SyntaxError(f"Error en E' con lookahead '{tok}'")

    def _parse_T(self) -> SyntaxTreeNode:
        node_id = self._next_node_id()
        node = SyntaxTreeNode(symbol="T", node_type=NodeType.NON_TERMINAL, creation_id=node_id)
        tok = self.current_token()

        if tok in ["id", "("]:
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "T",
                "lookahead": tok,
                "regla": f"T -> F T' (Nodo #{node_id})"
            })
            node.add_child(self._parse_F())
            node.add_child(self._parse_T_prime())
            return node
        else:
            raise SyntaxError(f"Error en T con lookahead '{tok}'")

    def _parse_T_prime(self) -> SyntaxTreeNode:
        node_id = self._next_node_id()
        node = SyntaxTreeNode(symbol="T'", node_type=NodeType.NON_TERMINAL, creation_id=node_id)
        tok = self.current_token()

        if tok == "*":
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "T'",
                "lookahead": tok,
                "regla": f"T' -> * F T' (Nodo #{node_id})"
            })
            node.add_child(self._match("*"))
            node.add_child(self._parse_F())
            node.add_child(self._parse_T_prime())
            return node
        elif tok in ["+", ")", "$"]:
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir a ε",
                "simbolo": "T'",
                "lookahead": tok,
                "regla": f"T' -> ε (por Follow(T')={{+, $, )}}) (Nodo #{node_id})"
            })
            eps_id = self._next_node_id()
            eps_node = SyntaxTreeNode(symbol="ε", node_type=NodeType.EPSILON, creation_id=eps_id)
            node.add_child(eps_node)
            return node
        else:
            raise SyntaxError(f"Error en T' con lookahead '{tok}'")

    def _parse_F(self) -> SyntaxTreeNode:
        node_id = self._next_node_id()
        node = SyntaxTreeNode(symbol="F", node_type=NodeType.NON_TERMINAL, creation_id=node_id)
        tok = self.current_token()

        if tok == "id":
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "F",
                "lookahead": tok,
                "regla": f"F -> id (Nodo #{node_id})"
            })
            node.add_child(self._match("id"))
            return node
        elif tok == "(":
            self.steps_log.append({
                "paso": len(self.steps_log) + 1,
                "accion": "Expandir no terminal",
                "simbolo": "F",
                "lookahead": tok,
                "regla": f"F -> ( E ) (Nodo #{node_id})"
            })
            node.add_child(self._match("("))
            node.add_child(self._parse_E())
            node.add_child(self._match(")"))
            return node
        else:
            raise SyntaxError(f"Error en F con lookahead '{tok}'")


# Algoritmos de Recorrido: DFS Preorden, DFS Postorden y BFS

def dfs_preorden(node: SyntaxTreeNode) -> List[SyntaxTreeNode]:
    """
    Recorrido en profundidad DFS Preorden:
    1. Visita la raíz (nodo actual).
    2. Recorre recursivamente cada subárbol hijo de izquierda a derecha.
    """
    result = [node]
    for child in node.children:
        result.extend(dfs_preorden(child))
    return result


def dfs_postorden(node: SyntaxTreeNode) -> List[SyntaxTreeNode]:
    """
    Recorrido en profundidad DFS Postorden:
    1. Recorre recursivamente cada subárbol hijo de izquierda a derecha.
    2. Visita la raíz (nodo actual).
    """
    result = []
    for child in node.children:
        result.extend(dfs_postorden(child))
    result.append(node)
    return result


def bfs_niveles(root: SyntaxTreeNode) -> Dict[int, List[SyntaxTreeNode]]:
    """
    Recorrido en anchura BFS utilizando una cola (FIFO):
    Visita los nodos nivel por nivel, agrupándolos según su distancia a la raíz.
    """
    levels: Dict[int, List[SyntaxTreeNode]] = {}
    queue = deque([(root, 0)])

    while queue:
        node, level = queue.popleft()
        node.depth = level
        if level not in levels:
            levels[level] = []
        levels[level].append(node)

        for child in node.children:
            queue.append((child, level + 1))

    return levels


# Algoritmo de Análisis Estructural del Árbol Sintáctico (Punto 5.7


def analizar_arbol_sintactico(node: Optional[SyntaxTreeNode]) -> Dict[str, int]:
    """
    Algoritmo recursivo en una sola pasada (O(N)) que computa:
    - Cantidad de nodos terminales
    - Cantidad de nodos no terminales
    - Cantidad de producciones vacías ε
    - Altura del árbol sintáctico (máxima distancia en aristas desde la raíz a una hoja)
    - Niveles totales del árbol (altura + 1)
    """
    if node is None:
        return {
            "terminales": 0,
            "no_terminales": 0,
            "epsilons": 0,
            "altura_aristas": -1,
            "niveles_nodos": 0
        }

    if node.node_type == NodeType.EPSILON:
        return {
            "terminales": 0,
            "no_terminales": 0,
            "epsilons": 1,
            "altura_aristas": 0,
            "niveles_nodos": 1
        }
    elif node.node_type == NodeType.TERMINAL:
        return {
            "terminales": 1,
            "no_terminales": 0,
            "epsilons": 0,
            "altura_aristas": 0,
            "niveles_nodos": 1
        }
    else:
        # Nodo no terminal
        term = 0
        noterm = 1  # El propio nodo actual
        eps = 0
        max_h_aristas = -1

        for child in node.children:
            res = analizar_arbol_sintactico(child)
            term += res["terminales"]
            noterm += res["no_terminales"]
            eps += res["epsilons"]
            if res["altura_aristas"] > max_h_aristas:
                max_h_aristas = res["altura_aristas"]

        altura_aristas = max_h_aristas + 1
        return {
            "terminales": term,
            "no_terminales": noterm,
            "epsilons": eps,
            "altura_aristas": altura_aristas,
            "niveles_nodos": altura_aristas + 1
        }


# Asignación de Coordenadas y Generación de Diagramas (Estilo Referencia


def calcular_coordenadas(root: SyntaxTreeNode):
    """
    Asigna coordenadas (x, y) a cada nodo para que el árbol se dibuje de forma
    elegante y proporcional, idéntico al estilo sintáctico/lingüístico de referencia.
    - Las hojas se distribuyen uniformemente en el eje x de izquierda a derecha.
    - Cada nodo padre se ubica en el punto medio de sus hijos directos.
    - El eje y corresponde al nivel de profundidad del nodo (y = -profundidad).
    """
    # 1. Asignar niveles (y)
    bfs_niveles(root)

    # 2. Recolectar hojas en orden de aparición (inorden sintáctico)
    hojas = []
    def recolectar_hojas(u: SyntaxTreeNode):
        if u.is_leaf():
            hojas.append(u)
        else:
            for ch in u.children:
                recolectar_hojas(ch)

    recolectar_hojas(root)

    # Asignar coordenadas x a las hojas espaciadas
    for i, hoja in enumerate(hojas):
        hoja.x = float(i * 2.2)

    # 3. Asignar coordenadas x a los nodos internos en postorden
    def asignar_x_padres(u: SyntaxTreeNode):
        for ch in u.children:
            asignar_x_padres(ch)
        if not u.is_leaf():
            u.x = sum(ch.x for ch in u.children) / len(u.children)
        u.y = -float(u.depth) * 1.5

    asignar_x_padres(root)


def generar_diagramas(root: SyntaxTreeNode, prefijo_salida: str = "arbol_sintactico"):
    calcular_coordenadas(root)

    todos_los_nodos = dfs_preorden(root)

    # Configuración de estilos visuales
    for con_numeracion in [False, True]:
        fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
        ax.set_facecolor("white")
        fig.patch.set_facecolor("white")

        # Dibujar líneas de conexión padre-hijo (líneas rectas sólidas y limpias)
        for u in todos_los_nodos:
            for ch in u.children:
                ax.plot([u.x, ch.x], [u.y, ch.y],
                        color="#111111", linewidth=1.3, zorder=1)

        # Dibujar etiquetas de nodos
        for u in todos_los_nodos:
            if con_numeracion:
                # Mostrar símbolo y número de creación
                if u.node_type == NodeType.TERMINAL:
                    texto = f"{u.symbol}\n(#{u.creation_id})"
                    color_texto = "#0d47a1"  # Azul oscuro elegante para terminales
                    peso = "bold"
                    tamano = 11
                elif u.node_type == NodeType.EPSILON:
                    texto = f"{u.symbol}\n(#{u.creation_id})"
                    color_texto = "#b71c1c"  # Rojo sobrio para epsilon
                    peso = "bold"
                    tamano = 11
                else:
                    texto = f"{u.symbol}\n(#{u.creation_id})"
                    color_texto = "#1a237e"  # No terminales
                    peso = "bold"
                    tamano = 12
            else:
                texto = u.symbol
                if u.node_type == NodeType.TERMINAL:
                    color_texto = "#000000"
                    peso = "bold"
                    tamano = 13
                elif u.node_type == NodeType.EPSILON:
                    color_texto = "#7f0000"
                    peso = "bold"
                    tamano = 13
                else:
                    color_texto = "#000000"
                    peso = "bold"
                    tamano = 14

            # Fondo blanco para evitar que las líneas se crucen con el texto
            ax.text(u.x, u.y, texto,
                    ha="center", va="center",
                    fontsize=tamano, fontweight=peso,
                    color=color_texto,
                    bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=0.95),
                    zorder=2)

        # Configurar límites y aspecto
        xs = [u.x for u in todos_los_nodos]
        ys = [u.y for u in todos_los_nodos]
        margin_x = 1.0
        margin_y = 1.2
        ax.set_xlim(min(xs) - margin_x, max(xs) + margin_x)
        ax.set_ylim(min(ys) - margin_y, max(ys) + margin_y)
        ax.axis("off")

        # Título elegante
        if con_numeracion:
            plt.title("Árbol Sintáctico con Orden de Creación de Nodos (Analizador Descendente)\nCadena: 'id + id * id'",
                      fontsize=14, fontweight="bold", pad=20, color="#111111")
            nombre_base = f"{prefijo_salida}_numerado"
        else:
            plt.title("Árbol Sintáctico Concreto (Parse Tree)\nGramática de Expresiones Aritméticas — Cadena: 'id + id * id'",
                      fontsize=14, fontweight="bold", pad=20, color="#111111")
            nombre_base = prefijo_salida

        plt.tight_layout()
        plt.savefig(f"{nombre_base}.png", dpi=300, facecolor="white")
        plt.savefig(f"{nombre_base}.svg", facecolor="white")
        plt.close()
        print(f" -> Diagrama generado: {nombre_base}.png y {nombre_base}.svg")


# Impresión del Árbol en Formato Jerárquico en Consol


def imprimir_arbol_consola(node: SyntaxTreeNode, prefijo: str = "", es_ultimo: bool = True):
    conector = "└── " if es_ultimo else "├── "
    tipo_str = f"[{node.node_type.value}]"
    print(f"{prefijo}{conector}{node.symbol} (Nodo #{node.creation_id}, Nivel {node.depth}) {tipo_str}")
    prefijo_hijo = prefijo + ("    " if es_ultimo else "│   ")
    for i, child in enumerate(node.children):
        imprimir_arbol_consola(child, prefijo_hijo, i == len(node.children) - 1)


# Programa Principa


def main():
    entrada_tokens = ["id", "+", "id", "*", "id"]
    print("=" * 80)
    print("RESOLUCIÓN PUNTO 5: APLICACIÓN AL ANÁLISIS SINTÁCTICO")
    print(f"Entrada analizada: {' '.join(entrada_tokens)}")
    print("=" * 80)

    # 1. Construcción paso a paso con el analizador descendente
    parser = TopDownParser(entrada_tokens)
    root = parser.parse()

    print("\n--- PASO A PASO DEL ANALIZADOR DESCENDENTE ---")
    for log in parser.steps_log:
        print(f"Paso {log['paso']:02d} | Lookahead: {log['lookahead']:<4} | Símbolo: {log['simbolo']:<3} | Regla: {log['regla']}")

    # 2. Asignar niveles mediante BFS
    niveles = bfs_niveles(root)

    print("\n--- ÁRBOL SINTÁCTICO ESTRUCTURADO EN CONSOLA ---")
    imprimir_arbol_consola(root)

    # 3. Recorridos
    preorden = dfs_preorden(root)
    postorden = dfs_postorden(root)

    print("\n--- RECORRIDOS SOBRE EL ÁRBOL SINTÁCTICO ---")
    print("1. DFS Preorden (Raíz -> Hijos Izq a Der):")
    print("   " + " -> ".join([f"{n.symbol}(#{n.creation_id})" for n in preorden]))

    print("\n2. DFS Postorden (Hijos Izq a Der -> Raíz):")
    print("   " + " -> ".join([f"{n.symbol}(#{n.creation_id})" for n in postorden]))

    print("\n3. BFS (Por Niveles):")
    for lvl in sorted(niveles.keys()):
        simbolos_lvl = [f"{n.symbol}(#{n.creation_id})" for n in niveles[lvl]]
        print(f"   Nivel {lvl}: {', '.join(simbolos_lvl)}")

    secuencia_bfs = []
    for lvl in sorted(niveles.keys()):
        secuencia_bfs.extend(niveles[lvl])
    print("   Secuencia completa BFS:")
    print("   " + " -> ".join([f"{n.symbol}(#{n.creation_id})" for n in secuencia_bfs]))

    # 4. Análisis estructural con el algoritmo del punto 5.7
    stats = analizar_arbol_sintactico(root)
    print("\n--- MÉTRICAS DEL ÁRBOL SINTÁCTICO (ALGORITMO 5.7) ---")
    print(f" - Total de nodos: {len(preorden)}")
    print(f" - Nodos no terminales: {stats['no_terminales']}")
    print(f" - Nodos terminales: {stats['terminales']}")
    print(f" - Producciones vacías (ε): {stats['epsilons']}")
    print(f" - Altura del árbol (aristas): {stats['altura_aristas']}")
    print(f" - Niveles totales de nodos: {stats['niveles_nodos']}")

    print("\n--- diagramas ---")
    generar_diagramas(root, "arbol_sintactico")
    print("\n¡Ejecución finalizada con éxito!")


if __name__ == "__main__":
    main()
