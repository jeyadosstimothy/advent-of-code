import sys

def expand_clique(graph, clique):
    next_nodes = []
    for node in clique:
        next_nodes.extend(graph[node])
    
    cliques = []
    for next_node in next_nodes:
        if clique == clique.intersection(graph[next_node]):
            cliques.append(clique.union(set([next_node])))
    return cliques

def find_max_clique(graph, nodes):
    max_clique = None
    visited = set()
    for i in range(len(nodes)):
        print(i)
        node = nodes[i]
        start_clique = set([node])
        queue = [start_clique]
        while len(queue) != 0:
            clique = queue[0]
            queue = queue[1:]
            vkey = tuple(sorted(clique))
            if vkey in visited:
                continue
            visited.add(vkey)
            if max_clique is None or len(clique) > len(max_clique):
                max_clique = clique
            new_cliques = expand_clique(graph, clique)
            queue.extend(new_cliques)
    return max_clique

if __name__ == '__main__':

    edge_list = [line.strip().split('-') for line in sys.stdin]
    
    nodes = set()
    graph = dict()
    for a, b in edge_list:
        nodes.add(a)
        nodes.add(b)
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)
        if b not in graph:
            graph[b] = set()
        graph[b].add(a)
    nodes = list(sorted(nodes))
    print(','.join(sorted(find_max_clique(graph, nodes))))