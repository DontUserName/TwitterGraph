from datascrapper import DataScrapper
from networkx import strongly_connected_components as scc
from datascrapper import DataScrapper
import matplotlib.pyplot as plt
import networkx as nx


class Tree():

    def __init__(self, user_0, batch_=10, depth_=1) -> None:
        self.root = user_0
        self.batch = batch_
        self.depth = depth_
        self.path = f'tweets_{self.batch}_depth_{self.depth}'
        self.nx = nx.DiGraph()
        self.build()
        self.add_missing_edges()
        # nx.nx_pydot.write_dot(self.nx, self.path + '.dot')

    def get_tree(self):
        return self.nx

    def build(self, user_=None, batch_=None, depth_=None) -> None:

        # construye recursivamente el grafo de reaciones empezando en el nodo root
        if user_ is None:
            user_ = self.root
            batch_ = self.batch
            depth_ = self.depth
            col = 'red'
        else:
            col = 'black'

        # scrap los últimos outputs de "user"
        df_actual = DataScrapper(user_, batch_).get_outputs()
        replies_dict = {}
        for _, row in df_actual.iterrows():
            if row['Reply_to'] is not None:
                replying_to = row['Reply_to'].username.lower()  # user
                # v = float(self.get_score(row['Tweets']))
                if replying_to in replies_dict.keys():
                    replies_dict[replying_to] += 1
                else:
                    replies_dict[replying_to] = 1
            if row['Mentions'] is not None:
                for m in row['Mentions']:
                    if m is not None:
                        usr = m.username.lower()
                        if usr not in replies_dict.keys():
                            replies_dict[usr] = 1

        # recorrer las respuestas encontradas y sus pesos para generar el árbol
        for k, v in replies_dict.items():
            col = col if self.root != k else 'blue'
            self.nx.add_edge(user_, k, weight=float(v),color=col)
            if depth_ > 0:
                self.build(k, max(batch_//2, 0), depth_-1)

    # add_missing_edges -> añadimos comunicaciones con la víctima no reflejadas de nodos presentes en el grafo
    def add_missing_edges(self):
        for n in self.nx.nodes:
            if n != self.root:
                if self.nx.has_edge(n, self.root) and not self.nx.has_edge(self.root, n):
                    responses = DataScrapper(n).get_mentions_from(self.root)
                    if not responses.empty:
                        self.nx.add_edge(self.root, n)

                elif self.nx.has_edge(self.root, n) and not self.nx.has_edge(n, self.root):
                    responses = DataScrapper(self.root).get_mentions_from(n)
                    if not responses.empty:
                        self.nx.add_edge(n, self.root)



    # TODO: REVISAR 
    def clean_tree(self):
        # limpia los nodos del árbol con input_deg <= 1 si no son adyacentes a victim
        to_remove = [n for n in self.nx.nodes if self.nx.in_degree(
            n) <= 1 and not self.nx.has_edge(self.root, n)]
        self.nx.remove_nodes_from(to_remove)

    def get_shortest_path(self, nodo_1, nodo_2):
        assert (nodo_1 in self.nx.nodes) and (nodo_2 in self.nx.nodes)
        return nx.dijkstra_path(self.nx, nodo_1, nodo_2)

    def get_distance(self, nodo_1, nodo_2):
        return len(self.get_shortest_path(nodo_1, nodo_2))