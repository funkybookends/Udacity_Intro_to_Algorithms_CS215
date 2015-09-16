# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs 
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
# 
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1}, 
#      'b': {'a': 1, 'd': 1}, 
#      'c': {'a': 1, 'd': 1}, 
#      'd': {'c': 1, 'b': 1, 'e': 1}, 
#      'e': {'d': 1, 'g': 1, 'f': 1}, 
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1} 
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'}, 
#      'b': {'a': 'green', 'd': 'red'}, 
#      'c': {'a': 'green', 'd': 'green'}, 
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'} 
#      }
#

def make_link(G,node1,node2,color):
    if node1 not in G: G[node1] = {}
    if node2 not in G: G[node2] = {}
    G[node1][node2] = color
    G[node2][node1] = color
    return G

def create_rooted_spanning_tree(G, root):
    """Creates a rooted spanning tree from root of graph G"""
    S = {}
    open_list = [root]
    while open_list:
        node = open_list.pop(0)
        for neighbour in G[node]:
            if neighbour not in S:
                S = make_link(S,node,neighbour,"green")
                open_list.append(neighbour)
            elif neighbour not in S[node]:
                S = make_link(S,node,neighbour,"red")

    return S

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'}, 
                 'b': {'a': 'green', 'd': 'red'}, 
                 'c': {'a': 'green', 'd': 'green'}, 
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'} 
                 }

###########

import itertools
def post_order(S, root):
    """returns a mapping of the post orders of the nodes in S"""
    # return mapping between nodes of S and the post-order value
    # of that node
    PO = {}
    c = itertools.count(1)
    l = [root]
    while l:
        n = l[-1]
        decendents = False #if the node has decendents we add them to the list to mark first and move on
        for d in S[n].keys():
            if S[n][d] == "green" and d not in l and d not in PO:
                l.append(d)
                decendents = True
        if not decendents: #else we give it a number, pop it from the list and move on
            l.pop()
            PO[n] = next(c)
    return PO



# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

##############

def number_of_descendants(S, root):
    """returns a mapping of the number of decscendents in S"""
    # return mapping between nodes of S and the number of descendants
    # of that node
    #print "S = ", S
    ND = {}
    l = [root]
    while l:
        node = l[-1]
        parent = False
        for neighbour in S[node].keys(): #  if unvisited decendents, we can't count yet
            if neighbour not in l and neighbour not in ND and S[node][neighbour] == "green":
                l.append(neighbour)
                parent = True
        if not parent:
            l.pop() #so we remove it from the list
            ##and count it's decendents including itself
            #it's a decendent if it's got a green connection and its not in l
            ND[node] = 1 + sum(ND[decendent] for decendent in S[node].keys() if S[node][decendent] == "green" and decendent not in l) # for itself
    return ND

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'}, 
          'b': {'a': 'green', 'd': 'red'}, 
          'c': {'a': 'green', 'd': 'green'}, 
          'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
          'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'} 
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

###############

def lowest_post_order(S, root, po):
    """Returns the lowest post order of the node"""
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    l = [root]
    LPO = {}
    while l:
        node = l[-1]
        parent_with_unmarked_children = False
        for neighbour in S[node].keys():
            if neighbour not in l and neighbour not in LPO:
                parent_with_unmarked_children = True
                l.append(neighbour)
        if not parent_with_unmarked_children:
            l.pop()
            LPO[node] = min([po[node]] + [LPO.get(neighbour,po[neighbour]) for neighbour in S[node].keys() ])
    return LPO


def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}


################

def highest_post_order(S, root, po):
    """returns the highest post order of the node"""
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    l = [root]
    HPO = {}
    while l:
        node = l[-1]
        parent_with_unmarked_children = False
        for neighbour in S[node].keys():
            if neighbour not in l and neighbour not in HPO:
                parent_with_unmarked_children = True
                l.append(neighbour)
        if not parent_with_unmarked_children:
            l.pop()
            ##the hights is a max between :
            HPO[node] = max([po[node]] +  #it's own post order
                [HPO.get(neighbour,0) for neighbour in S[node].keys()] + ##the post orders in it's neighebours that have already been marked
                                        ##i.e. it's parent won't have been marked yet.
                [HPO.get(neighbour,po[neighbour]) for neighbour in S[node].keys() if S[node][neighbour] == "red"]) #and any of its red neighbours
    return HPO

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}
    
#################

def bridge_edges(G, root, fancy_output = False):
    """Calcualtes tbe brige edges in a graph G

        Keyword Arguments:
        G -- The graph to search
        root -- some node to check from
        fancy_output - displays the results of the searches and highlights the identified bridges"""
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    S = create_rooted_spanning_tree(G,root)
    PO = post_order(S,root)
    ND = number_of_descendants(S,root)
    LPO = lowest_post_order(S,root, PO)
    HPO = highest_post_order(S,root, PO)
    bridges = []
    l = [root]
    checked = []

    while l:
        node = l.pop()
        checked.append(node)
        for d in S[node].keys():
            if S[node][d] == "green" and d not in checked:
                l.append(d)
                if HPO[d] <= PO[d] and LPO[d] > (PO[d]-ND[d]):
                    bridges.append((node,d))

    if fancy_output:
        print "\nTesting Graph:"
        print G
        print "\nBridges:", bridges

        print "\nResults:"
        print "node\tPO\tND\tLPO\tHPO\tHPO<=PO\tLPO>PO-ND\tBRIDGE"
        for node in G.keys():
            if HPO[node] <= PO[node] and LPO[node] > (PO[node]-ND[node]) and node != root:
                b = "True"
            else:
                b = ""
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s" % (node, PO[node], ND[node], LPO[node], HPO[node],HPO[node] <= PO[node],LPO[node] > (PO[node]-ND[node]), b)

    return bridges

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    bridges = bridge_edges(G, 'a')
    assert bridges == [('d', 'e')]

test_create_rooted_spanning_tree()
test_post_order()
test_number_of_descendants()
test_lowest_post_order()
test_highest_post_order()
test_bridge_edges()

def my_test():
    a,b,c,d,e,f,g,h,i = "a b c d e f g h i".split()
    edges = ((a,c),(c,b),(b,d),(d,i),(d,e),(c,e),(e,g),(g,f),(g,h), (a,b), (f,h), (i,b))
    G = {}
    for node1,node2 in edges:
        G = make_link(G,node1,node2,1)

    bridge_edges(G,b)

my_test()