#Take in imdb-1 and calculate the top 20 central actors
# using tha average centrality measurement
#centraility is defined as the average distance to all the other nodes

f = "imdb-4.tsv"
debug = False
debug_max_import = 3000

## imdb-1 through 4, each with a larger graph
##contains tab seperated values of the form
#Bloom, Orlando The Lord of the Rings: The Return of the King   2003

input_data = open(f)

IMDB = {} ##container for the bipartite graph
actors = []
movies = []

def make_link(G,x,y):
    if x not in G: G[x] = {}
    if y not in G: G[y] = {}
    G[x][y] = 1
    G[y][x] = 1
    return G

##read in the data
for i,line in enumerate(input_data):
    name,title,year = line.split("\t") ##get the data

    movie = title+year

    make_link(IMDB,name,movie) ##add it to the dictionary and lists
    if name not in actors: actors.append(name)
    if title+year not in movies: movies.append(movie)

    if debug == True and i > debug_max_import: break #print and debug info
    if i!=0 and i%5000 == 0: print "imported %s lines from %s" % (i,f)

print "imported %s actors and %s movies from from %s (len(IMDB) = %s" % (len(actors), len(movies),f, len(IMDB))

##in this new method of find the top 20 actors we calculate the centrality
#for 20 random actors, and thrn go through, and if we find an actor 
#with a better centrality we remove the worst from the list and insert the new one.

#When the centrality is being caluculated we pass in a break point 
#which is the worst centrality in our top 20 so far so that hopefully we can save time


def new_centrality(G, v, max_sum = float("inf")):
    """Finds the centrality of a node if it is less than max_sum
        does not do the division at the end"""
    dfs = {} #distance_from_start
    open_list = [v]
    dfs[v] = 0
    s = 0
    while len(open_list) > 0 and s <= max_sum:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in dfs:
                dfs[neighbor] = dfs[current] + 1
                s += dfs[current]+1
                open_list.append(neighbor)
    if sum(dfs.values())> max_sum: return None
    return sum(dfs.values())
#len(dfs) is constant so i can caulculate it for 20 people, and then as soon as the sum is over the 


##calcualate centrality for the best 20 actors
Actor_Centralities = []
ms = [] #during the initilization holds all the centralities of the actors


from random import randint

n = 20 ##top how many to find

while len(Actor_Centralities)<n: #chooses n randomly and calculates there centrality
    actor = actors.pop(randint(0,len(actors)-1)) #choose actor
    c = new_centrality(IMDB,actor)               #calculate centrality
    Actor_Centralities.append((actor,c))         #add the (actor,centrality)
    ms.append(c)                                 #append the centrality

ms = max(ms) #change it to just hold the worst centrality found so far
Actor_Centralities = sorted(Actor_Centralities, key = lambda a: a[1]) #sort them

print Actor_Centralities #the first random n
rejects = 0 ##used to count how many were ignored

for i,actor in enumerate(actors):
    #goes through the actors and calculates the centrality
    c = new_centrality(IMDB,actor,ms) #uses the current worst as the cut off
    if c and c<ms: ##if one was found - it should be better than ms
        #print "\tadding %s %s" % (actor, c)
        olda, oldc = Actor_Centralities.pop() #take out the old words
        Actor_Centralities.append((actor,c)) ##and in the new better one
        Actor_Centralities = sorted(Actor_Centralities, key = lambda a: a[1]) ##sort them again
        ms = Actor_Centralities[-1][1] ##update the now worst centrality
        print "%s, %5.0f < %5.0f - %s with %5.0f - %3.0f rejected before" % (actor[:7], c,oldc, Actor_Centralities[-1][0][:7], Actor_Centralities[-1][1], rejects)
        rejects = 0 ##reset the counter
    else:
        rejects +=1 ##one was ignored
    
    if i %1000 == 0: ##progress update
        print "checked", i,"actors"

i = 1  ##display the most central actors
for actor,centrality in Actor_Centralities:
    print "%2.0f. %s %s" % (i,actor,float(centrality)/len(IMDB))
    i +=1


##find the top 20 actors
#the old method, that calculates it for all actors and then partitions the list
#to find the top 20


##calcualate centrality
# def old_centrality(G, v):
# dfs = {} #distance_from_start
# open_list = [v]
# dfs[v] = 0
# while len(open_list) > 0:
#     current = open_list[0]
#     del open_list[0]
#     for neighbor in G[current].keys():
#         if neighbor not in dfs:
#             dfs[neighbor] = dfs[current] + 1
#             open_list.append(neighbor)
# return float(sum(dfs.values())/len(dfs))
# def dict_partition(tpl,v, sp = 1):
#     """partitions a list of tuples around 
#        a value v on sort position sp"""
#     less = []
#     more = []

#     for val in tpl:
#         if val[sp] < v[sp]: less.append(val)
#         if val[sp] >= v[sp]: more.append(val)

#     return (less,v,more)

# def dict_top_k(tpl,k,sp = 1):
#     """
#         Returns the top k of list of tuples

#         Keyword Arguments:
#         L -- the list to be partitioned
#         k -- the number of values wanted
#         sp - Sort Position - the item in the tuple to sort on
#            usually dict.items() therefore defaults to the value
#     """
#     from random import randint

#     if len(tpl) == 0: return []
#     i = randint(0,len(tpl)-1)
#     v = tpl.pop(i)
#     (less,v,more) = dict_partition(tpl,v,sp)

#     if len(less)     == k: return less
#     if len(less) + 1 == k: return less+[v]
#     if len(less)     >  k: return dict_top_k(less, k, sp)

#     return less+[v]+dict_top_k(more,k-len(less)-1, sp)

# n = 20
# top_n = sorted(dict_top_k(Actor_Centralities.items(),n), key=lambda p: p[1])

# for i in range(len(top_n)):
#   print "%2.0f. %s %7.5f" % (i,top_n[i][0], top_n[i][1])