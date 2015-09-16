#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    # your code here
    # return a set
    first_node = G.keys().pop()  #grab a first node
    left = [first_node] #nodes in left, only connect to nodes in right
    right = [] # nodes in right only connect to nodes in left, otherwise the graph is not bipartite
    nodes_to_check = [first_node]
    checked_nodes = []
    while nodes_to_check:
        node = nodes_to_check[0]
        print "nodes to check = ",nodes_to_check
        print "checking node = ",node
        nodes_to_check.remove(node)
        neighbours = G[node].keys()
        if node in left:  
            ##all the neighbours must be in right
            for neighbour in neighbours: #check that all the neighbours are on the correct side
                if neighbour in left: return None ##if it's on the same side, not bipartite
                if neighbour not in right: right.append(neighbour) ## append it to the side it should be if it's not there already
                if neighbour not in checked_nodes: nodes_to_check.append(neighbour) ##if it's neighbours haven't been checked, make sure we check it
        elif node in right:
            for neighbour in neighbours:
                if neighbour in right: return None
                if neighbour not in left: left.append(neighbour)
                if neighbour not in checked_nodes: nodes_to_check.append(neighbour)
        checked_nodes.append(node)
    return set(right)


########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None
