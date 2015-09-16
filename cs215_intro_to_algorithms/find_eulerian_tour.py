# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]


def find_eulerian_tour(graph):
    """Finds an eulerian tour through the a graph represented as list of tuples"""

    ##confirm that it has a tour, and find the start and end nodes if there are any
    edges = [] #a dictionary of with keys as the edges (n1,n2)
    degree = {} #a dictionary of the degree of each node
  
    for n1,n2 in graph:
        if (n1,n2) in edges: return None #no repeat edges please
        if (n2,n1) in edges: return None
        edges.append((n1,n2))
        degree[n1] = degree.get(n1,0) + 1 #increments the degrees of the nodes
        degree[n2] = degree.get(n2,0) + 1

    if [n for n,d in degree.items() if d%2==1]: return None #No odd degree nodes please

    
    ##functions used during the search
    def eulerian_tour(path):
        """Checks if a path is a valid eulerian tour"""
        if path[0] != path[-1]: return False #must start and end in the same place
        if len(path)-1!=len(edges): return False#path must be the correct length
        return not Available_Edges(path) #check that every edge was used

    def Available_Edges(path):
        """Returns a list of available_edges i.e. ones that have not been used in the path"""
        if len(path) == 1: return edges
        used_edges = [(path[i],path[i+1]) for i in range(len(path)-1)]
        return [(x,y) for (x,y) in edges if not ((x,y) in used_edges or (y,x) in used_edges)]

    ##Start at a starting node
    l = [[degree.keys()[0]]] #creates a starting search list of some random node
    loops = 0
    while not eulerian_tour(l[-1]):
        if loops%1000==0 and loops!=0: print loops, "loops, ", len(degree), "nodes", len(graph), "edges", len(l), "in the list"
        loops +=1
        path = l.pop() ##performs a depth first search used pop(0) for a breadth first search, 
        remaining_edges = Available_Edges(path)
        for edge in remaining_edges:
            if path[-1] in edge: #if the last node in the path is part of the edge
                if edge[0] != path[-1]: l.append(path+[edge[0]]) #append the adjacent edge
                else: l.append(path+[edge[1]])

    return l.pop()

from create_graph_with_eulerian_tour import create_tour

def retest():
    for i in range(10,100):
        e =  create_tour(i)
        tour = find_eulerian_tour(e)

        if not tour:
            print e
            break

        print "found a tour for %s nodes with %s edges" % (i,len(e))

retest()