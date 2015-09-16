import string
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

# There have been some comments that the wording in the instructions is ambiguous. To be more precise W(a, b) = W(b, a) = P(contains A and contains B | contains A or contains B);

#from marvel import marvel, characters
import random
import cPickle

marvel = cPickle.load(open("smallG.pkl",'rb'))
characters = cPickle.load(open("smallChr.pkl",'rb'))

def create_weighted_graph(bipartiteG, characters):
    G = {}
    # your code here
    for char1 in characters:
        for char2 in characters:
            if char1!=char2:
                w = weight(bipartiteG, char1, char2)
                G = make_link(G,char1,char2,w)

    return G

def make_link(G,u,v,w):
    if not w: return G
    if u not in G: G[u] = {}
    if v not in G: G[v] = {}

    G[u][v] = w
    G[v][u] = w

    return G

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
    for ch in G.keys():
        print "\t%s\n%s" % (ch, G[ch])
    # three comics contain charA or charB
    # charA and charB are together in one of them
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA', None) == None
    assert G['charA'].get('charC', None) == None

def test2():
    G = create_weighted_graph(marvel, characters)
    s = random.sample(G.keys(),10)
    for i in s:
        ss = random.sample(G[i].keys(),3)
        for sq in ss:
            w = weight(marvel,i,sq)
            print "G[%s][%s] = %5.3s - %5.3s" % (string.capwords(i[:10]), string.capwords(sq[:10]), G[i][sq],w)


def weight(G,char1,char2):
    coapperances = 0
    char1books = G[char1].keys()
    char2books = G[char2].keys()
    for book in char1books:
        if char2 in G[book].keys():
            coapperances +=1
    if coapperances==0: return False
    d = len(set(char1books+char2books))
    w = float((0.0+coapperances)/d)
    #print "%s was in %s out of %s books with %s (%s)" % (char1, coapperances, len(char1books), char2,w)
    return w

print test()