# Eulerian Tour Ver 1
#
# Write a function, `create_tour` that takes as
# input a list of nodes
# and outputs a list of tuples representing
# edges between nodes that have an Eulerian tour.
#

def create_simple_tour(nodes):
    """creates a simple tour thats a roundtrip through all the nodes"""
    number_of_nodes = len(nodes)
    tour = [(nodes[0],nodes[-1])]
    for i in range(number_of_nodes-1):
        tour.append((nodes[i],nodes[i+1]))
    
    return tour

def create_tour(N = 20):
    """
        Returns a list of edges represented as tuples, where there is always
        eulerian tour through the nodes

        Keyword Arguments:
        N -- Represents the number of nodes to be in the list or a list of nodes

        Firstly it connects two random nodes
        Then it connects a random unconnected node to a random connected node
        Then it goes through the odd degree nodes
            connecting in pairs any that are not connected
            if it can't connect any because they are already connected
                it connects it to another random node and tries again
    """
    from random import randint


    unconnected_nodes = range(N) if type(N) == int else N[:]
    connected_nodes = []
    degree = {}
    edges = []

    n1 = unconnected_nodes.pop(randint(0,len(unconnected_nodes)-1))
    n2 = unconnected_nodes.pop(randint(0,len(unconnected_nodes)-1))

    edges.append((n1,n2))

    degree[n1] = 1
    degree[n2] = 1
    connected_nodes.append(n1)
    connected_nodes.append(n2)

    def Con(n1,n2,edges):
        if (n1,n2) in edges: return True
        if (n2,n1) in edges: return True
        return False

    while unconnected_nodes:
        n1 = unconnected_nodes.pop(randint(0,len(unconnected_nodes)-1))
        n2 = connected_nodes[randint(0,len(connected_nodes)-1)]

        edges.append((n1,n2))
        degree[n1] = degree.get(n1,0) + 1
        degree[n2] = degree.get(n2,0) + 1

        connected_nodes.append(n1)

    odd_nodes = [n for n,d in degree.items() if d%2 == 1]

    while odd_nodes:
        n1 = odd_nodes.pop()
        available_odd_nodes = [n2 for n2 in odd_nodes if (n1!=n2 and not Con(n1,n2,edges))]
        if not available_odd_nodes:
            ##choose another random node, that's evenly connected
            even = [n for n,d in degree.items() if (d%2==0 and n!=n1 and not Con(n1,n,edges))]
            n2 = even.pop(randint(0,len(even)-1))

            edges.append((n1,n2))
            degree[n1] += 1
            degree[n2] += 1

            odd_nodes.append(n2)

        else:
            n2 = available_odd_nodes.pop(randint(0,len(available_odd_nodes)-1))
            odd_nodes.remove(n2)

            edges.append((n1,n2))
            degree[n1] += 1
            degree[n2] += 1

    return edges


#########

def get_degree(tour):
    degree = {}
    for x, y in tour:
        degree[x] = degree.get(x, 0) + 1
        degree[y] = degree.get(y, 0) + 1
    return degree

def check_edge(t, b, nodes):
    """
    t: tuple representing an edge
    b: origin node
    nodes: set of nodes already visited

    if we can get to a new node from `b` following `t`
    then return that node, else return None
    """
    if t[0] == b:
        if t[1] not in nodes:
            return t[1]
    elif t[1] == b:
        if t[0] not in nodes:
            return t[0]
    return None

def connected_nodes(tour):
    """return the set of nodes reachable from
    the first node in `tour`"""
    a = tour[0][0]
    nodes = set([a])
    explore = set([a])
    while len(explore) > 0:
        # see what other nodes we can reach
        b = explore.pop()
        for t in tour:
            node = check_edge(t, b, nodes)
            if node is None:
                continue
            nodes.add(node)
            explore.add(node)
    return nodes

def is_eulerian_tour(nodes, tour):
    # all nodes must be even degree
    # and every node must be in graph
    degree = get_degree(tour)
    for node in nodes:
        try:
            d = degree[node]
            if d % 2 == 1:
                print "Node %s has odd degree" % node
                return False
        except KeyError:
            print "Node %s was not in your tour" % node
            return False
    connected = connected_nodes(tour)
    if len(connected) == len(nodes):
        return True
    else:
        print "Your graph wasn't connected"
        return False

def test():
    nodes = [20, 21, 22, 23, 24, 25]
    tour = create_tour(nodes)

    return is_eulerian_tour(nodes, tour)

test()
