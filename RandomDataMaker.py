from Graph import *
import numpy as np
from itertools import product
import pandas as pd


class RandomDataMaker:
    """
    This purpose of this class is to generate, for a linear SCM WITHOUT
    feedback loops, a synthetic dataset with: (1) column labels= the names
    of the nodes graph.ord_nodes, (2)instances of node values in each row.
    To generate this, we require 'alpha_mat', 'graph' and 'sigma_eps'.


    Attributes
    ----------
    alpha_mat: np.array of shape=(dim,dim), where dim = number of nodes.
        The matrix of alphas (i.e., gains \alpha_{i|j})
    graph: Graph
        information about DAG structure
    sigma_eps: list[float]
        the standard deviations of \epsilon_j, which is the external root
        node pointing into x_j. The entries in this list are ordered
        according to 'graph.ord_nodes'

    """

    def __init__(self, graph, sig_eps, alpha_mat=None, alpha_bound=1.0):
        """
        Constructor.

        In this constructor, an alpha_mat not equal to 'None' can be
        submitted, or, if alpha_mat == None, an alpha_mat will be generated
        randomly. If generated randomly, each non-zero gain \alpha_{ i|j} is
        chosen from the uniform distribution over the interval [ -alpha_bound,
        alpha_bound]

        Parameters
        ----------
        graph: Graph
        sig_eps: list[float]
        alpha_mat: np.array of shape=(dim, dim)
        alpha_bound: float
            must be a positive number.
        """
        self.graph = graph
        dim = graph.num_nds
        assert len(sig_eps) == dim
        self.sigma_eps = sig_eps
        if alpha_mat is None:
            self.alpha_mat = self.generate_random_gains(
                graph, alpha_bound)
        else:
            assert alpha_mat.shape == (dim, dim)
            self.alpha_mat = alpha_mat

    @staticmethod
    def generate_random_gains(graph, alpha_bound=1.0):

        """
        In this internal method, the gains \alpha_{i|j} are generated
        randomly. Each non-zero \alpha_{ i|j} is chosen from the uniform
        distribution over the interval [-alpha_bound, alpha_bound].

        Parameters
        ----------
        alpha_bound: float
            must be a positive number.

        Returns
        -------
        np.array of shape=(dim, dim)

        """
        assert alpha_bound > 0
        dim = graph.num_nds
        alpha_mat = np.zeros((dim, dim))
        for row, col in product(range(dim), range(dim)):
            row_nd = graph.ord_nodes[row]
            col_nd = graph.ord_nodes[col]
            if row > col and (col_nd, row_nd) in graph.arrows:
                alpha_mat[row, col] = np.random.uniform(-alpha_bound, alpha_bound)
        return alpha_mat

    def generate_one_random_instance(self):
        """
        This internal method returns an array with random values for the
        nodes 'graph.ord_nodes'.

        Returns
        -------
        np.array of shape=(dim,)

        """

        dim = self.graph.num_nds
        eps_values = [np.random.normal(loc=1.0, scale=self.sigma_eps[i])
                      for i in range(dim)]
        nd_values = [0]*dim
        for i in range(dim):
            nd_values[i] += eps_values[i]
            for j in range(dim):
                if i > j:
                    nd_values[i] += self.alpha_mat[i, j]*nd_values[j]

        return nd_values

    def generate_dataset_csv(self, num_rows, path):
        """
        This method writes a file which contains a dataset in the
        comma-separated-values (csv) format. The dataset has (1) column
        labels= the names of the nodes graph.ord_nodes, (2)instances of node
        values in each row.

        Parameters
        ----------
        num_rows: int
            number of rows of the dataset
        path: str
            path to the destination of the output file

        Returns
        -------
        None

        """
        df = pd.DataFrame(columns=self.graph.ord_nodes)
        for row in range(num_rows):
            df.loc[row] = self.generate_one_random_instance()
        df.to_csv(path, index=False)


if __name__ == "__main__":
    def main(draw):
        dot = "digraph G {\n" \
              "a->b;\n" \
              "a->s;\n" \
              "n->s,a,b;\n" \
              "}"
        with open("tempo13.txt", "w") as file:
            file.write(dot)
        dot_path = 'tempo13.txt'
        # path = 'dot_atlas/good_bad_trols_G1.dot'
        graph = Graph(dot_path)
        if draw:
            graph.draw(jupyter=False)
        dim = graph.num_nds
        sig_eps = [2]*dim
        dmaker = RandomDataMaker(graph, sig_eps=sig_eps)
        data_path = "test_data.csv"
        num_rows = 5
        dmaker.generate_dataset_csv(num_rows, data_path)
        print(pd.read_csv(data_path))
        print("------------------------------")
        alpha_mat = np.zeros((dim, dim))
        alpha_mat[1, 0] = 4
        alpha_mat[2, 0], alpha_mat[2, 1] = 2, -3
        alpha_mat[3, 0], alpha_mat[3, 1] = 1, -1
        sig_eps = [0.0]*dim
        dmaker = RandomDataMaker(graph, sig_eps=sig_eps,
                                 alpha_mat=alpha_mat)
        data_path = "test_data.csv"
        num_rows = 5
        dmaker.generate_dataset_csv(num_rows, data_path)
        print(pd.read_csv(data_path))

    main(True)
