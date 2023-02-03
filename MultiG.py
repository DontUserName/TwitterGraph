import networkx as nx
from graphmanager import GraphManager 


# politica españa:
# derecha : vox_es, santi_abascal, macarena_olona, ivanedlm
# izquierda: irenemontero, podemos, agarzon, pabloiglesias, sanchezcastejon

# política eeuu: 
# derecha: realdonaldtrump, speakermccarthy, repmikegarcia
# izquierda: joebiden, barackobama, hillaryclinton  

# actores eeuu:
# aaronpaul_8, bryancranston, breakingbad


class MultiG:

    def __init__(self, victims, tweets=10) -> None:
        self.victims = victims
        self.path    = ''.join([s[0] for s in self.victims])+'_multi'
        self.graph   = nx.DiGraph()
        for v in victims:
            act = nx.DiGraph(GraphManager(v, tweets).nx)
            self.graph = nx.compose(self.graph, act)
        nx.nx_pydot.write_dot( self.graph, self.path + '.dot')
        self.manager = GraphManager('', -1, -1, self.path + '.dot')
    
    # get_friends -> return bidirectional relation nodes
    def get_friends(self):
        return self.manager.get_bidir()

    # save -> save graph to .dot and .png
    def save(self):
        nx.nx_pydot.write_dot(self.manager.nx, self.path + '.dot')   # SAVE .dot
        g = nx.nx_agraph.to_agraph(self.manager.nx)
        g.draw( self.path  + '.png', prog='circo') # SAVE .png

    # save_friends -> save bidir/friends to .png
    def save_friends(self):
        amigos = self.get_friends()
        g = nx.nx_agraph.to_agraph(self.manager.nx.subgraph(amigos))
        g.draw(path=self.path + '_amigos.png', prog='circo')
