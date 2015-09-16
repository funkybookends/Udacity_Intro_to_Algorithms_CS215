#  
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#

##this code was taken from bnsantos on github
def label(tree, node, center, labels):
    print "\tlabelling", node, "with center", center
    for child, dist in tree[node].items():
        if child in labels and center in labels[child]: 
            continue
        if child not in labels:
            labels[child] = {}
        labels[child][center] = dist + labels[node][center]
        print "\t\tlabel[%s][%s] = %s" % (child,center,labels[child][center])
        label(tree, child, center, labels)

##this code was taken from bnsantos on github
def dfs(tree, node, parent=None):
    #print "\t\t\tdfs(tree,", node, ", parent =", parent,")"
    if not len(tree[node]): 
        return 0
    if len(tree[node]) == 1 and parent is not None: 
        return 1
    return 1 + max(dfs(tree, child, node) for child in tree[node] if child != parent)

##this code was taken from bnsantos on github
def make_tree(tree, node, center):
    out = {node: {}}
    frontier = [(node, [child for child in tree[node] if child != center])]
    while frontier:
        node, children = frontier.pop()
        for child in children:
            out[node][child] = tree[node][child]
            if child not in out:
                out[child] = {}
            out[child][node] = tree[child][node]
            frontier.append((child, [c for c in tree[child] if c != node]))
    return out

##this code was taken from bnsantos on github
def remove(tree, center):
    out = []
    for child in tree[center]:
        out.append(make_tree(tree, child, center))
    return out

##this code was taken from bnsantos on github
def create_labels(tree):
    center = None
    labels = {}
    for vertex in tree: #tries to find the center of the tree
        print "vertex", vertex
        labels[vertex] = {vertex: 0} #creeates a label to itself
        max_len = dfs(tree, vertex)
        if center is None or max_len < center[1]: 
            center = (vertex, max_len)
        print "center", center
    center = center[0]
    print "center", center, "confirmed"
    label(tree, center, center, labels)
    print "label function returns", labels
    trees = remove(tree, center)
    for t in trees:
        print "calling create_labels for",t,"in",trees
        nlabels = create_labels(t)
        for k, v in nlabels.items():
            labels[k].update(v)
    print "return labels", labels
    return labels


#######
# Testing
#


def display_all_labels(labels):
    for node in labels.keys():
        print "%s to %s" % (node, labels[node].items())

def get_distances(G, labels): #his code to get the distances from my labels 1
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test(): ##the first simple test
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    distances = get_distances(tree, labels)

    header = "   "
    for i in range(1,13): 
        header += "%2.0f " % i
    print header
    for i in range(1,13):
        line = "%2.0f " % i
        for j in range(1,13):
            line += "%2.0f " % distances[i][j]
        print line

    assert distances[1][2] == 1
    assert distances[1][4] == 2
    print "simple test passed"

from collections import deque

def distance(tree, w, u): ##  a second piece of code to get the distance for random test
    if w==u: return 0

    distances = {w: 0}
    frontier = deque([w])
    while frontier:
        n = frontier.popleft()
        for s in tree[n]:
            if s not in distances: 
                distances[s] = distances[n] + tree[n][s]
                frontier.append(s)
            if s==u:
                return distances[u]

    return None

import math

def max_labels(labels):
    return max(len(labels[u]) for u in labels)

def labels_needed(G):
    return 1 + int(math.ceil(math.log(len(G))/math.log(2)))

def test2():
    # binary tree
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)

    header = "   "
    for i in range(1,13): 
        header += "%2.0f " % i
    print header
    for i in range(1,13):
        line = "%2.0f " % i
        for j in range(1,13):
            line += "%2.0f " % distances[i][j]
        print line

    print "\n testing test 1"
    assert distances[1][2] == 1
    assert distances[1][4] == 2    
    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1   
    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3
    print 'test1 passes'

    # chain graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
             (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels), "labels_needed = %s, max_used = %s" % (labels_needed(tree) , max_labels(labels))
    distances = get_distances(tree, labels)

    header = "   "
    for i in range(1,13): 
        header += "%2.0f " % i
    print header
    for i in range(1,13):
        line = "%2.0f " % i
        for j in range(1,13):
            line += "%2.0f " % distances[i][j]
        print line

    print "testing test 2"
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 12
    assert distances[6][1] == 5
    assert distances[6][13] == 7
    assert distances[8][3] == 5
    assert distances[10][4] == 6
    print 'test2 passes'

    # "star-chain" graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), 
             (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13)]    
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    display_all_labels(labels)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][1] == 0
    assert distances[5][5] == 0
    assert distances[1][2] == 1
    assert distances[1][3] == 2    
    assert distances[1][4] == 3
    assert distances[1][5] == 4
    assert distances[5][6] == 5
    assert distances[5][7] == 6
    assert distances[5][8] == 7
    assert distances[5][9] == 8
    print 'test3 passes'

from math import log, ceil
from random import randint

def random_test(): ##a randomly sized test
    N = 100 ##number of tests
    n0 = 20
    n1 = 100

    for _ in range(N):
        tree = {}
        for w in range(1, n0): #Makes a chain through the graph of size n0
            make_link(tree, w, w+1, randint(1, 1))

        for w in range(n0+1, n1+1):
            make_link(tree, randint(1, w-1), w, randint(1, 1))

        labels = create_labels(tree) #Calls my create labels
        distances = get_distances(tree, labels) # calles first get distances function

        assert max([len(labels[n]) for n in tree]) <= int(ceil(log(len(tree)+1, 2)))

        for _ in range(N):
            w = randint(1, n1)
            u = randint(1, n1)
            assert distance(tree, w, u) == distances[w][u]

    print 'random_test() passed'

test()
#test2()
#random_test()

def my_test():
    a,b,c,d,e,f,g,h,i = "a b c d e f g h i".split()
    edges = [(a,c),(c,b),(b,d),(d,i),(d,e),(c,e),(e,g),(g,f),(g,h), (a,b), (f,h), (i,b)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    distances = get_distances(tree, labels)
    display_all_labels(labels)

#my_test()