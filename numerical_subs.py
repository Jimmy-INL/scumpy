from Graph import *
from FBackGraph import *
import sympy as sp
from itertools import product

"""

The functions in this file return their input x after performing some 
numerical substitutions of some of the symbols in x. x is usually a sp.Matrix.

"""


def set_to_one_sigma_eps_mat(graph, x):
    """
    This method substitutes \sigma_{\epsilon_j} by 0 for all j.

    Parameters
    ----------
    graph: Graph
    x: sp.Matrix or sp.Symbol

    Returns
    -------
    type(x)

    """
    num_nds = graph.num_nds
    for i in range(num_nds):
        sigma_eps_sb = "sigma_eps_" + str(i)
        x = x.subs({sp.Symbol(sigma_eps_sb): 1})
    return x


def set_to_zero_gains_without_arrows(graph, x):
    """
    This method substitutes gain \alpha_{i|j} by 0 for all i,j such that
    there is no arrow x_j->x_i.

    Parameters
    ----------
    graph: Graph
    x: sp.Matrix or sp.Symbol

    Returns
    -------
    type(x)
    """
    dim = graph.num_nds
    for row, col in product(range(dim), range(dim)):
        row_nd = graph.ord_nodes[row]
        col_nd = graph.ord_nodes[col]

        if row > col and (col_nd, row_nd) not in graph.arrows:
            alp_sb = "alp_" + str(row) + "_L_" + str(col)
            x = x.subs({sp.Symbol(alp_sb): 0})
    return x


def set_to_zero_fback_gains_without_arrows(graph, x):
    """
    This method substitutes feedback gain \beta_{i|j} by 0 for all i,j such
    that there is no arrow x_j->x_i.

    Parameters
    ----------
    graph: FBackGraph
    x: sp.Matrix or sp.Symbol

    Returns
    -------
    type(x)
    """
    dim = graph.num_nds
    for row, col in product(range(dim), range(dim)):
        row_nd = graph.ord_nodes[row]
        col_nd = graph.ord_nodes[col]

        if (col_nd, row_nd) not in graph.fback_arrows:
            beta_sb = "beta_" + str(row) + "_L_" + str(col)
            x = x.subs({sp.Symbol(beta_sb): 0})
    return x


if __name__ == "__main__":
    from core_matrices import *

    def main():
        dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "}"
        with open("tempo13.txt", "w") as file:
            file.write(dot)
        path = 'tempo13.txt'
        graph = Graph(path)
        dim = graph.num_nds

        x = sigma_eps_sb_mat(dim)
        print("\n", x)
        x = set_to_one_sigma_eps_mat(graph, x)
        print(x)

        print()
        # dot has 5 arrows out of maximum of 6 possible
        # for 4 nodes. Hence, one of the gains is zero.
        # arrow 2->3 (i.e., "b"->"s") is missing
        # so alp_3_L_2=0
        print(graph.ord_nodes)
        print(graph.arrows)

        x = alp_sb_mat(dim)
        print("\n", x)

        x = set_to_zero_gains_without_arrows(graph, x)
        print(x)

    main()
