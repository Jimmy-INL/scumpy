from Graph import *

class FBackGraph(Graph):
    """

    Attributes
    ----------
    dag_arrows: list[(str, str)]
        arrows that form a DAG. Their arrow gains are represented by \beta_{
        i|j}.
    fback_arrows: list[(str, str)]
        feedback arrows that connect 2 adjacent time-slices. Their arrow
        gains are represented by \alpha_{i|j}.
    """

    def __init__(self,
                dot_file_path,
                amputated_arrows=None):
        Graph.__init__(self,
                       dot_file_path,
                       amputated_arrows=amputated_arrows,
                       is_DAG=False)
        self.dag_arrows, self.fback_arrows = self.get_dag_and_fback_arrows()
        self.nx_graph = nx.DiGraph()
        self.nx_graph.add_edges_from(self.dag_arrows)
        # this bombs if not DAG
        self.ord_nodes = list(nx.topological_sort(self.nx_graph))

    def get_dag_and_fback_arrows(self):
        dag_arrows = []
        fback_arrows = []
        with open(self.path) as f:
            in_lines = f.readlines()
            for line in in_lines:
                if "->" not in line:
                    continue
                else:
                    green_arrow = False
                    if "green" in line:
                        green_arrow = True
                    pa, ch_list = FBackGraph.get_pa_and_ch_list(line)
                    for ch in ch_list:
                        if green_arrow:
                            fback_arrows.append((pa, ch))
                        else:
                            dag_arrows.append((pa, ch))
        # print("ccvbb---------------", fback_arrows)
        return dag_arrows, fback_arrows

    def draw(self, jupyter=False, slices=1, point_right=False):
        """
        This method draws the graph either on the console (jupyter=False) or
        in a jupyter notebook (jupyter=True). Amputated arrows are drawn in
        red, non-amputated ones in black.

        Parameters
        ----------
        jupyter: bool
        slices: int
            number of slices to draw. slices=1 draws one time-slice with
            feedback loops as dashed green arrows. slices=2 draws 2
            time-slices with feedback arrows in solid green.
        point_right: bool
            If point_right=False, time points down (the default
            orientation). If point_right=True, time points right.

        Returns
        -------
        None

        """
        new_dot = ""
        with open(self.path) as f:
            in_lines = f.readlines()
            for line in in_lines:
                if "->" not in line:
                    new_dot += line
                    if "{" in line and point_right:
                        new_dot += "rankdir=LR;\n"
                else:
                    green_arrow = False
                    if "green" in line:
                        green_arrow = True
                    pa, ch_list = Graph.get_pa_and_ch_list(line)
                    for ch in ch_list:
                        if slices == 1:
                            new_dot += pa + " -> " + ch
                            if (pa, ch) in self.amputated_arrows:
                                new_dot += " [color=red];\n"
                            elif green_arrow:
                                new_dot += " [color=green, style=dashed];\n"
                            else:
                                new_dot += ";\n"
                        elif slices>1:
                            for sli in range(slices):
                                long_pa = pa + "[" + str(sli) + "]"
                                long_pa = '"' + long_pa + '"'
                                if green_arrow:
                                    long_ch = ch + "[" + str(sli + 1) + "]"
                                else:
                                    long_ch = ch + "[" + str(sli) + "]"
                                long_ch = '"' + long_ch + '"'
                                if green_arrow:
                                    if sli != slices-1:
                                        new_dot += long_pa + " -> " + long_ch
                                        new_dot += "[color=green];\n"
                                else:
                                    new_dot += long_pa + " -> " + long_ch
                                    new_dot += ";\n"
                        else:
                            assert False
        with open("tempo1389.dot", "w") as file:
            file.write(new_dot)
        DotTool.draw('tempo1389.dot', jupyter)
if __name__ == "__main__":

    def main(draw):
        path = 'dot_atlas/fback-2node.dot'
        g = FBackGraph(path)
        print('fback_arrows:', g.fback_arrows)
        print('dag_arrows:', g.dag_arrows)
        if draw:
            g.draw(jupyter=False, slices=1)
            g.draw(jupyter=False, slices=3, point_right=True)

    main(True)
