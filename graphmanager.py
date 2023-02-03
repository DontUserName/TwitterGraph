from os import path
from tree import Tree
import networkx as nx
import time
import os


class GraphManager:

    def __init__(self, victim_, n_tweets=10, depth_=1, ruta=None) -> None:
        self.victim = victim_
        self.n_tweets = n_tweets
        self.depth = depth_

        # RUTA - CARPETA Y ARCHIVO
        if ruta is None:
            self.dir  = f'{os.getcwd()}/VICTIMS/{self.victim}'
            self.path = f'/tweets_{self.n_tweets}_depth_{self.depth}.dot'
        else:
            self.path, self.dir = ruta, ''
        
        # SI EXISTE EL ARCHIVO - SE CARGA
        if path.exists(self.dir + self.path):
            self.nx = nx.nx_pydot.read_dot(self.dir + self.path)
        else:
            # SI NO EXISTE EL DIRECTORIO - SE CREA
            if self.dir != '' and not os.path.exists(self.dir):
                os.makedirs(self.dir, mode=0o777)
            # SE CALCULA EL GRAFO Y SE GUARDA
            t = Tree(self.victim, self.n_tweets, self.depth)
            self.nx = t.nx
            self.save(self.dir+self.path)
            

    def save(self, s=None):
        s = self.dir+self.path if s is None else s
        nx.nx_pydot.write_dot(self.nx, s)   # SAVE .dot
        g = nx.nx_agraph.to_agraph(self.nx)
        g.draw(s[:-4]+'.png', prog='circo') # SAVE .png


    #get_friends -> devuelve nodos 'amigos' - aquellos con los que víctima tiene comunicación bidireccional
    def get_friends(self):
        return [n for n in self.nx.nodes if n != self.victim and self.nx.has_edge(self.victim, n)
               and self.nx.has_edge(n, self.victim)]

    # get bidir -> devuelve los nodos del grafo que tienen alguna comunicación bidireccional entre sí
    def get_bidir(self):
        bidir = []
        nodes = list(self.nx.nodes)
        for n1 in range(len(nodes)-1):
            for n2 in range(n1+1, len(nodes)):
                if self.nx.has_edge(nodes[n1], nodes[n2]) and self.nx.has_edge(nodes[n2], nodes[n1]):
                    bidir += [nodes[n1]] + [nodes[n2]]
        return list(set(bidir))

    # save_friends -> save bidir/friends to .png
    def save_friends(self):
        if self.victim:
            amigos = self.get_friends() + [self.victim]
        else:
            amigos = self.get_bidir()
        g = nx.nx_agraph.to_agraph(self.nx.subgraph(amigos))
        g.draw(path=self.dir+self.path[:-4]+'_amigos.png', prog='circo')



# EXAMPLE: SCRAPPING VOX HEADERS ON TWITTER
if __name__ == '__main__':

    tim = time.time()
 
    victims = ['santi_abascal','macarena_olona','ivanedlm']
    for v in victims:
        manager = GraphManager(v, 10)

    print("TimeStamp: ", time.time()-tim, '\n')
