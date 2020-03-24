import csv
import networkx as nx 

class CSVdata: 
    def __init__(self, edges, selfLoops, TotEdges): 
        self.edges = edges
        self.selfLoops = selfLoops
        self.TotEdges = TotEdges

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

    CSVdata.edges = len(G.edges())

    CSVdata.selfLoops = findSelfLoops(G)

    CSVdata.TotEdges = CSVdata.edges - CSVdata.selfLoops

    # val = [for i in G.edges.data]

    pos = 0 
    neg = 0
    for i in G.edges.data(): 
        if i[2].get("weight") == '1': 
            pos += 1
        else: 
            neg += 1 


    CSVdata.trustEdges = pos
    CSVdata.distrustEdges = neg 

def printResults(): 
    print("Edges in network: ", CSVdata.edges)
    print("Self-Loops: ", CSVdata.selfLoops )
    print("Edges used - TotEdges: ", CSVdata.TotEdges)
    print("Trust Edges: ",  CSVdata.trustEdges)
    print("Distrust Edges: ",  CSVdata.distrustEdges)

if __name__ == "__main__":

    print("=====================================")
    '''
    Row looks like: 221363,261079,1
    '''
    # fileName = input("Enter the name of the file: \n")
    fileName = "epinions96.csv"
    openAndPrint(fileName)
    printResults()
    print("=====================================")
