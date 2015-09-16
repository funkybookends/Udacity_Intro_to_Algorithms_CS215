# Finding a Favor v2 
#
# Each edge (u,v) in a social network has a weight p(u,v) that
# represents the probability that u would do a favor for v if asked.
# Note that p(v,u) != p(u,v), in general.
#
# Write a function that finds the right sequence of friends to maximize
# the probability that v1 will do a favor for v2.
# 

#
# Provided are two standard versions of dijkstra's algorithm that were
# discussed in class. One uses a list and another uses a heap.
#
# You should manipulate the input graph, G, so that it works using
# the given implementations.  Based on G, you should decide which
# version (heap or list) you should use.
#

# code for heap can be found in the instructors comments below
from heap import * ##functions provided by udacity
from operator import itemgetter

def make_link(G,n1,n2,val):
    if n1 not in G: G[n1]={}
    G[n1][n2] = val
    return G

import math
def maximize_probability_of_favor(G, v1, v2):
    """
        Calculates the best route through the graph from v1 to v2
        when the edge weights should be multiplied.

        Uses either a heap or a list depending on which is more efficient
        for the size of the graph

        first it transforms the graph, taking -log(weight) of each node
        and then it Calculates the path, and then it returns the path
        and the probability. We use -log instead of log since weights are
        decimal percentages (i.e. less than 1) and dijkstra needs positive
        weights.

    """
    if v1 not in G or v2 not in G: return (None, None) #if either node is not in G

    P = {} #a new graph to hold the -log of the weights

    vertices = len(G.keys()) #to decide on heap or list search
    edges = 0 #to decide on heap or list search

    #Transform G to P
    for node in G.keys():
        P[node] = {}
        for conn in G[node].keys():
            edges += 1
            P = make_link(P,node,conn,-math.log(G[node][conn]))

    #determine which is better, heap or list - and calculate the best path
    if vertices**2 < (vertices+edges)*math.log(vertices):
        fd = dijkstra_list(P,v1)
    else:
        fd = dijkstra_heap(P,v1)

    if v2 not in fd: return (None, None) #if the node is not reachable, return None

    ##now that I have the number I need to find the path

    path = [v2] #start the path off - calculated in reverse beacause each node remembers its parent

    while v1 not in path: #until we reach the start
        path = [fd[path[0]][1]] + path #add the parent to the beginning of the list

    prob = math.exp(-fd[v2][0]) #calculate the probability
    print "path", path
    print "prob", prob
    return (path,prob)

#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry} 
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} #keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

##########
#
# Test

def test():
    G = {'a':{'b':.9, 'e':.5},
         'b':{'c':.9},
         'c':{'d':.01},
         'd':{},
         'e':{'f':.5},
         'f':{'d':.5}}
    path, prob = maximize_probability_of_favor(G, 'a', 'd')
    assert path == ['a', 'e', 'f', 'd']
    assert abs(prob - .5 * .5 * .5) < 0.001

    
test()