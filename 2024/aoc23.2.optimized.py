import sys

def maximize_clique(graph, clique, memoized):
    mem_key = tuple(sorted(clique))
    if mem_key in memoized:
        return memoized[mem_key]

    next_nodes = []
    for node in clique:
        next_nodes.extend(graph[node])
    
    max_clique = clique
    for next_node in next_nodes:
        if clique == clique.intersection(graph[next_node]):
            clique.add(next_node)
            maximized_clique = maximize_clique(graph, clique, memoized)
            clique.remove(next_node)
            if len(maximized_clique) > len(max_clique):
                max_clique = maximized_clique
    memoized[mem_key] = set(max_clique)
    return memoized[mem_key]

def find_max_clique(graph, nodes):
    max_clique = None
    memoized = dict()
    for node in nodes:
        maximized_clique = maximize_clique(graph, set([node]), memoized)
        if max_clique is None or len(maximized_clique) > len(max_clique):
            max_clique = maximized_clique
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