import sys

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
    
    start_nodes = [node for node in nodes if node[0] == 't']
    triplets = set()
    for start_node in start_nodes:
        next_nodes = graph[start_node]
        for next_node in next_nodes:
            intersection_nodes = next_nodes.intersection(graph[next_node])
            print(start_node, next_node, intersection_nodes)
            for intersection_node in intersection_nodes:
                triplet = tuple(sorted([start_node, next_node, intersection_node]))
                triplets.add(triplet)
    print(triplets)
    print(len(triplets))