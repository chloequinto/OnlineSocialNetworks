import csv
import networkx as nx 

class CSVdata: 
    def __init__(self, edges, selfLoops, totEdges, trustEdges, distrustEdges, prob_p, prob_n, triangles): 
        self.edges = edges
        self.selfLoops = selfLoops
        self.totEdges = totEdges
        self.trustEdges = trustEdges
        self.distrustEdges = distrustEdges
        self.prob_p  = prob_p 
        self.prob_n = prob_n
        self.triangles = triangles 

    def show(self): 
        print("Edges in network: " + str(self.edges))
        print("Self-Loops: "+ str(self.selfLoops ))
        print("Edges used - TotEdges: " + str(self.totEdges))
        print("Trust Edges: " +  str(self.trustEdges) + " |  probability p: " + str(self.prob_p))
        print("Distrust Edges: " +  str(self.distrustEdges) + " |  probability 1-p: " + str(self.prob_n))
        print("Triangles: " + str(self.triangles))
    



def findSelfLoops(G):
    nodes_in_selfloops = []
    for i, v in G.edges(): 
        if i == v: 
            nodes_in_selfloops.append(i)
    return len(nodes_in_selfloops)


def openAndPrint(fileName): 
    global selfLoops
    G = nx.Graph()
    with open(fileName) as csvFile: 
        for row in csvFile: 
            row = row.replace("\n", "") # get rid of new line breaks 
            line = row.split(",") # split into an array 
            G.add_edge(line[0], line[1], weight = line[2])

    edges = len(G.edges())

    selfLoops = findSelfLoops(G)

    totEdges = edges - selfLoops


    pos = 0 
    neg = 0
    for i in G.edges.data(): 
        if i[2].get("weight") == '1': 
            pos += 1
        else: 
            neg += 1 

    trustEdges = pos
    distrustEdges = neg 
    prob_p = pos / totEdges
    prob_n = 1 - prob_p

    # Need to find triangles where cliques > 3 
    triangles = 0     
    cliq_list = list(nx.clique.enumerate_all_cliques(G))
    traingle_list = [ x for x in cliq_list if len(x)==3 ]
    triangles = len(traingle_list)
  
    myData = CSVdata(edges, selfLoops, totEdges, pos, neg, round(prob_p,2), round(prob_n,2), triangles )
    myData.show()

if __name__ == "__main__":

    print("=====================================")
    '''
    Row looks like: 221363,261079,1
    '''
    # fileName = input("Enter the name of the file: \n")
    fileName = "epinions96.csv"
    openAndPrint(fileName)
    print("=====================================")
