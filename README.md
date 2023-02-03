
## Twitter OSINT - Replies and mentions scrapper

El objetivo de este programa es obtener información sobre las interacciones de uno o varios usuarios de Twitter.

En resumen, se trata conseguir un mapa visual de las relaciones que mantiene un usuario en la plataforma, scrapeando las respuestas y menciones en sus últimos tweets.

        1 - Obtención de datos -> DataScrapper()
        2 - Transformación de datos: pd.DataFrame => Tree()
        3 - Manejo y análisis de datos: GraphManager()
        

### CÓMO FUNCIONA
1) Se usa la librería SNScrape (llamadas/queries en la clase DataScrapper) para buscar al usuario 'victima' y guardar sus últimos tweets.

2) Se crea un árbol (clase Tree) seleccionando un nodo raíz - usuario a scrapear o víctima - y opcionalmente el número de tweets y profundidad a calcular. En cada iteración se calculan y guardan los hijos del nodo actual (que serán los nodos encontrados en menciones y respuestas) y se expande recursivamente el árbol desde cada hijo.

3) Se usa la clase GraphManager para cargar y manejar los grafos creados. Incluye alguna función auxiliar como get_friends() o add_edges()

4) Si se quiere scrapear varias víctimas a la vez, para ver el grafo conjunto de relaciones, se crea una instancia de MultiG. Esta clase calcula varios grafos en principio disjuntos, y los une en un grafo resultado final.


## Información representada
La representación de los resultados será visual, representando un grafo o árbol cuyos nodos serán los usuarios encontrados en las respuestas relacionadas, y las aristas las relaciones entre nodos. Las aristas del grafo serán las menciones o repuestas de un usuario a otro y los pesos de las mismas intentarán dar un peso a la calidad de relación de ambos usuarios en Twitter. 

## TODO:

- Añadir colores y formato en el grafo - mejorar la claridad de la representación

    -- Relacionar el tamaño de los nodos a las interacciones que tengan
    -- En rojo aristas output de víctima, en azul aristas input de víctima, el resto en verde

- Filtrar nodos: limpiar los que tengan sólo inputs, o sean muy lejanos/innecesarios / marcas no personales... etc

- Añadir la opción de filtrar por nodo

- Añadir pesos a las aristas. Los pesos vendrán dados por:
    1) Frecuencia de menciones 
    
    2) Análisis de sentimientos de los tweets entre los nodos 
    
    3) Interacciones de los tweets en común(likes+rts)
    
    4) Número total de menciones

- Estaría bien saber qué personas tienen en común dos cuentas en el grafo explorado

- Buscar caminos directos no implícitos en el árbol - scrapear en profunidad los nodos candidatos a ser clique

- Filtrar subgrafos por usuario - solo devolver los hijos directos
