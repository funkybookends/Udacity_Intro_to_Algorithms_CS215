#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists
    def lovliest_path(G):
        """finds the edge with the highest value and returns the two nodes"""
        m = 0
        ma = None
        mb = None
        for node in G.keys():
            for conn in G[node].keys():
                if G[node][conn] > m:
                    m = G[node][conn]
                    ma = node
                    mb = conn
        print "found lovliest_path of %s to %s with weight %s" % (ma,mb,m)
        return (ma,mb)
                
    ma, mb = lovliest_path(G)
    #so we want to use the path between ma and mb in our path
    # so we find i -> ma and mb -> j and we return them
    # if either fails, then we return none
    path1 = dij(G,i,ma)
    path2 = dij(G,mb,j)
    if path1 and path2: return path1+path2
    else: return None

def dij(G,i,j):
    open_list = [[i]]
    searched_nodes = [i]
    while open_list:
        path = open_list.pop()
        node = path[-1]
        for ne in G[node].keys():
            if ne==j:
                return path + [j]
            if ne not in searched_nodes:
                open_list.append(path + [ne])
                searched_nodes.append(ne)
    return False



#########
#
# Test

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

def test():
    G = {'a':{'c':1},
         'b':{'c':1},
         'c':{'a':1, 'b':1, 'e':1, 'd':1},
         'e':{'c':1, 'd':2},
         'd':{'e':2, 'c':1},
         'f':{}}
    path = feel_the_love(G, 'a', 'b')
    assert score_of_path(G, path) == 2

    path = feel_the_love(G, 'a', 'f')
    assert path == None

test()