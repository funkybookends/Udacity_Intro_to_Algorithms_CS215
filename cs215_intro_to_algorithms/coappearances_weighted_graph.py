#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

from marvel import marvel, characters

def create_weighted_graph(bipartiteG, characters):
    """Creates a weighted graph for the charecters in a bipartite graph
        uses the weight function to caluclate the weight"""
    G = {}
    for char1 in characters:
        for char2 in characters:
            if char1!=char2:
                w = weight(bipartiteG, char1, char2) ##weight returns false if there is no shared appearences
                G = make_link(G,char1,char2,w) ##a link will not be made if w == False
    return G

def make_link(G,u,v,w):
    """makes a link in G between u and v with weight w if w"""
    if not w: return G
    if u not in G: G[u] = {}
    if v not in G: G[v] = {}

    G[u][v] = w
    G[v][u] = w

    return G

def weight(G,char1,char2):
    """calculates the number of coapperances of two chars
       in the set of all books they both appeard in"""
    coapperances = 0
    char1books = G[char1].keys()
    char2books = G[char2].keys()
    for book in char1books: ##go through the books of on char
        if char2 in G[book].keys(): ##if the second appeard in it
            coapperances += 1 #add the coappearence
    #no need to repeat this for the second char
    if coapperances == 0: return False ##if they had no coappearances, there is no connection
    total_appearances = len(set(char1books+char2books)) ##the number of books they have both been in, no duplicates
    w = float((0.0+coapperances)/total_appearances)
    return w

######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    # three comics contain charA or charB
    # charA and charB are together in one of them
    assert G['charA']['charB'] == 1.0 / 3
    print G
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

def test2():
    G = create_weighted_graph(marvel, characters)
   
    
print test()