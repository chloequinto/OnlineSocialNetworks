import csv
import networkx as nx 
from tabulate import tabulate
from itertools import combinations as comb
import pandas as pd 

class CSVdata: 
    def __init__(self, edges, selfLoops, totEdges, trustEdges, distrustEdges, prob_p, prob_n, 
                triad, col_format, aTTT_num, aTTD_num, aTDD_num, aDDD_num, 
                EpTTT, EpTTD, EpTDD, EpDDD, 
                aTTT_percent,aTTD_percent, aTDD_percent, aDDD_percent, 
                eTTT_num, eTTD_num, eTDD_num, eDDD_num): 
        self.edges = edges
        self.selfLoops = selfLoops
        self.totEdges = totEdges
        self.trustEdges = trustEdges
        self.distrustEdges = distrustEdges
        self.prob_p  = prob_p 
        self.prob_n = prob_n
        self.triad = triad 
        self.col_format = col_format
        self.aTTT_num = aTTT_num
        self.aTTD_num =  aTTD_num
        self.aTDD_num = aTDD_num
        self.aDDD_num = aDDD_num
        self.EpTTT = EpTTT
        self.EpTTD = EpTTD
        self.EpTDD = EpTDD
        self.EpDDD = EpDDD
        self.aTTT_percent = aTTT_percent
        self.aTTD_percent = aTTD_percent
        self.aTDD_percent = aTDD_percent
        self.aDDD_percent  = aDDD_percent
        self.eTTT_num =  eTTT_num
        self.eTTD_num = eTTD_num
        self.eTDD_num = eTDD_num
        self.eDDD_num = eDDD_num

    def show(self): 
        print("\nEdges in network: " + str(self.edges))
        print("Self-Loops: "+ str(self.selfLoops ))
        print("Edges used - TotEdges: " + str(self.totEdges))
        print("Trust Edges: " +  str(self.trustEdges) + " |  probability p: " + str(self.prob_p))
        print("Distrust Edges: " +  str(self.distrustEdges) + " |  probability 1-p: " + str(self.prob_n))
        print("Triangles: " + str(self.triad))

        print("\n\nExpected Distribution")
        print(tabulate([
                        ["TTT", self.EpTTT, self.eTTT_num ], 
                        ["TTD", self.EpTTD,self.eTTD_num ], 
                        ["TDD", self.EpTDD, self.eTDD_num], 
                        ["DDD", self.EpDDD, self.eDDD_num],
                        ["Total", self.EpTTT+self.EpTTD+ self.EpTDD+self.EpDDD,  self.eTTT_num + self.eTTD_num+ self.eTDD_num+ self.eDDD_num]
                        
                        ], headers = ["Type", "percent", "number"]))

        print("\n\nActual Distribution")
        print(tabulate([
                        ["TTT", self.aTTT_percent, self.aTTT_num], 
                        ["TTD", self.aTTD_percent, self.aTTD_num],
                        ["TDD", self.aTDD_percent, self.aTDD_num], 
                        ["DDD", self.aDDD_percent, self.aDDD_num],
                        ["Total", round(self.aTTT_percent+ self.aTTD_percent+self.aTDD_percent+self.aDDD_percent), round(self.aTTT_num+self.aTTD_num+self.aTDD_num+self.aDDD_num)]
                        
                        ], headers = ["Type", "percent", "number"]))

def typesOfTrust(triangle):
    cat = {
        ("1","1","1") : "TTT",
        ("-1","1","1") : "TTD",
        ("-1","-1","1") : "TDD",
        ("-1","-1","-1") : "DDD"
    }
    return cat[tuple(sorted([x[1] for x in triangle]))]


def findSelfLoops(G):
    nodes_in_selfloops = []
    for i, v in G.edges(): 
        if i == v: 
            nodes_in_selfloops.append(i)
    return len(nodes_in_selfloops)


def openAndPrint(fileName): 
    G = nx.Graph()
    with open(fileName) as csvFile: 
        for row in csvFile: 
            row = row.replace("\n", "") # get rid of new line breaks 
            line = row.split(",") # split into an array 
            G.add_edge(line[0], line[1], weight = line[2])

    edges = len(G.edges())

    selfLoops = findSelfLoops(G)

    totEdges = edges - selfLoops

    pos, neg = 0, 0 

    for i in G.edges.data(): 
        if i[2].get("weight") == '1': 
            pos += 1
        else: 
            neg += 1 

    trustEdges = pos
    distrustEdges = neg 
    prob_p = pos / totEdges
    prob_n = 1 - prob_p

  
    cliq_list = list(nx.clique.enumerate_all_cliques(G))
    triad_list = [ x for x in cliq_list if len(x)==3 ] 
    triad = len(triad_list)

    weights = nx.get_edge_attributes(G, 'weight') # will look like {'0', '1'} : '-1'


    tri_weights = list(map(lambda x: list(map(lambda x: (x, weights[x]), comb(x, 2))), triad_list)) 

    #Tri_Weights will look like 
    #(('5', '20'), '1'), (('5', '50'), '1'), (('20', '50'), '1')]

    # we want to classify it as 
    # (('5', '20'), '1'), (('5', '50'), '1'), (('20', '50'), '1'), "TTT"]
    for i in range(len(tri_weights)):
        tri_weights[i].append(typesOfTrust(tri_weights[i]))



    col_format = tuple(zip(*tri_weights))
    table = pd.DataFrame({
        "trust_category": col_format[3],
        "edge_1": tuple(zip(*col_format[0]))[0],
        "trust_1": tuple(zip(*col_format[0]))[1],
        "edge_2": tuple(zip(*col_format[1]))[0],
        "trust_2": tuple(zip(*col_format[1]))[1],
        "edge_3": tuple(zip(*col_format[2]))[0],
        "trust_3": tuple(zip(*col_format[2]))[1]
    })

    triad_table = table.sort_values(['trust_category'],ascending=False).reset_index(drop=True)
    triad_table.trust_category.unique()

    # Actual Distribution
    aTTT_num = len(triad_table[triad_table['trust_category']=='TTT'])
    aTTD_num = len(triad_table[triad_table['trust_category']=='TTD'])
    aTDD_num = len(triad_table[triad_table['trust_category']=='TDD'])
    aDDD_num = len(triad_table[triad_table['trust_category']=='DDD'])
    aTotal_num = aTTT_num + aTTD_num + aTDD_num + aDDD_num

    aTTT_percent = round((aTTT_num/aTotal_num)*100, 0)
    aTTD_percent = round((aTTD_num/aTotal_num)*100, 0)
    aTDD_percent = round((aTDD_num/aTotal_num)*100, 0)
    aDDD_percent = round((aDDD_num/aTotal_num)*100, 0)

    # Expected Distrubtion 
    eTTT_percent = prob_p * prob_p * prob_p
    eTTD_percent = 3 * (prob_p * prob_p * prob_n)
    eTDD_percent = 3 * (prob_p * prob_n * prob_n)
    eDDD_percent = prob_n * prob_n * prob_n

    eTTT_num = round(eTTT_percent * aTotal_num,1)
    eTTD_num = round(eTTD_percent * aTotal_num,1)
    eTDD_num = round(eTDD_percent * aTotal_num,1)
    eDDD_num = round(eDDD_percent * aTotal_num,1)



    n_triads = len(triad_table)
    type_1 = len(triad_table[triad_table['trust_category'] == 'TTT'])
    type_2 = len(triad_table[triad_table['trust_category'] == 'TTD'])
    type_3 = len(triad_table[triad_table['trust_category'] == 'TDD'])
    type_4 = len(triad_table[triad_table['trust_category'] == 'DDD'])


    myData = CSVdata(edges, selfLoops, totEdges, pos, neg, round(prob_p,2), round(prob_n,2), triad, col_format, 
                                        aTTT_num, aTTD_num, aTDD_num, aDDD_num, 
                                        round(eTTT_percent*100,1), round(eTTD_percent*100, 1), round(eTDD_percent*100, 1), round(eDDD_percent*100,1), 
                                        aTTT_percent,aTTD_percent, aTDD_percent, aDDD_percent, 
                                        eTTT_num, eTTD_num, eTDD_num, eDDD_num)
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
