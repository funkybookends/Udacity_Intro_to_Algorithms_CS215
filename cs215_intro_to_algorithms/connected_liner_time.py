#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#

def process_graph(G):
    """preprocess the graph G, and puts all the nodes in a set

        sets may be accessed to tell if two nodes are reachable
        if sets[node1] == sets[node2]: node 2 is reachable from node 1

        sets is only a global variable because of the way udacity is marking the test
    """

    unvisted_nodes = G.keys()
    global sets ##creates the global variable
    sets = {}
    while unvisted_nodes: #while not all nodes have been given a set
        start = unvisted_nodes.pop() ##take out an unvisited node
        sets[start] = start ##put it in it's own set
        open_list = [start] ##start a list to find all the nodes reachable by it
        while open_list: ##does a depth first search of all nodes it can find
            this = open_list.pop() #take out one from the list
            for neigbour in G[this].keys(): ##get all it's neghbours
                if neigbour in unvisted_nodes: # if we haven't visited it yet
                    unvisted_nodes.remove(neigbour) #Mark it as visited (by removing it from unvisited)
                    open_list.append(neigbour) #add it to the ones to check
                    sets[neigbour] = start #put it in the set

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    """for a graph preproccessed by process_graph it will 
        tell you if j is reachable by i in constant time"""
    # your code here
    return sets[i] == sets[j]

#######
# Testing
#
def test():
    G = {'a':{'b':1},
         'b':{'a':1},
         'c':{'d':1},
         'd':{'c':1},
         'e':{}}
    process_graph(G)
    assert is_connected('a', 'b') == True
    assert is_connected('a', 'c') == False

    print "\n\n"
    G = {'a':{'b':1, 'c':1},
         'b':{'a':1},
         'c':{'d':1, 'a':1},
         'd':{'c':1},
         'e':{}}
    process_graph(G)
    assert is_connected('a', 'b') == True
    assert is_connected('a', 'c') == True
    assert is_connected('a', 'e') == False

test()
