'''
Chloe Quinto 
CS 581 A05 
Objective: Parse through CSV files to calculate key attributes such as triads and their expected and actual distrubtion
How to run:
    In terminal, run `python3 main.py`

'''

import csv
import networkx as nx 
from tabulate import tabulate
from itertools import combinations as comb
import pandas as pd 
import time


class CSVdata: 

    def __init__(self, edges, selfLoops, totEdges, trustEdges, distrustEdges, prob_p, prob_n, 
                triad, col_format, aTTT_num, aTTD_num, aTDD_num, aDDD_num, 
                EpTTT, EpTTD, EpTDD, EpDDD, 
                aTTT_percent,aTTD_percent, aTDD_percent, aDDD_percent, 
                eTTT_num, eTTD_num, eTDD_num, eDDD_num): 
        '''
            Each CSV has these following attributes 
        '''
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
        '''
            Prints what we see in the terminal 
        '''
        print("\nEdges in network: " + str(self.edges))
        print("Self-Loops: "+ str(self.selfLoops ))
        print("Edges used - TotEdges: " + str(self.totEdges))
        print("Trust Edges: " +  str(self.trustEdges) + " |  probability p: " + str(self.prob_p))
        print("Distrust Edges: " +  str(self.distrustEdges) + " |  probability 1-p: " + str(self.prob_n))
        print("Triangles: " + str(self.triad))

        print("\nExpected Distribution")
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
    '''
        Function: Classifies a specific triangle with a trust 
        For example, given (('5', '20'), '1'), (('5', '50'), '1'), (('20', '50'), '1')
        We see that all the weights are 1, then this is classified as TTT
    '''
    cat = {
        ("1","1","1") : "TTT",
        ("-1","1","1") : "TTD",
        ("-1","-1","1") : "TDD",
        ("-1","-1","-1") : "DDD"
    }
    return cat[tuple(sorted([x[1] for x in triangle]))]


def findSelfLoops(G):
    '''
        Function: finds self loops in the graph
    '''
    nodes_in_selfloops = []
    for i, v in G.edges(): 
        if i == v: 
            nodes_in_selfloops.append(i)
    return len(nodes_in_selfloops)


def cleanAndFind(fileName):
    '''
        Function: reads csv file and calculates the attributes necessary 
    '''
    start = time.time() 
    G = nx.Graph()
    try: 
        with open(fileName) as csvFile: 
            for row in csvFile: 
                row = row.replace("\n", "") # get rid of new line breaks 
                line = row.split(",") # split into an array 
                G.add_edge(line[0], line[1], weight = line[2])
    except: 
        print("[ERROR] File does not exist. Ending script")
        return

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


    # Let's put it all one one pandas table 
    col = tuple(zip(*tri_weights))
    table = pd.DataFrame({
        "trustCategory": col[3],
        "edgeOne": tuple(zip(*col[0]))[0],
        "trustOne": tuple(zip(*col[0]))[1],
        "edgeTwo": tuple(zip(*col[1]))[0],
        "trustTwo": tuple(zip(*col[1]))[1],
        "edgeThree": tuple(zip(*col[2]))[0],
        "TrustThree": tuple(zip(*col[2]))[1]
    })

    triad_table = table.sort_values(['trustCategory'],ascending=False).reset_index(drop=True)
    triad_table.trustCategory.unique()

    # Actual Distribution
    aTTT_num = len(triad_table[triad_table['trustCategory']=='TTT'])
    aTTD_num = len(triad_table[triad_table['trustCategory']=='TTD'])
    aTDD_num = len(triad_table[triad_table['trustCategory']=='TDD'])
    aDDD_num = len(triad_table[triad_table['trustCategory']=='DDD'])
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


    myData = CSVdata(edges, selfLoops, totEdges, pos, neg, round(prob_p,2), round(prob_n,2), triad, col, 
                                        aTTT_num, aTTD_num, aTDD_num, aDDD_num, 
                                        round(eTTT_percent*100,1), round(eTTD_percent*100, 1), round(eTDD_percent*100, 1), round(eDDD_percent*100,1), 
                                        aTTT_percent,aTTD_percent, aTDD_percent, aDDD_percent, 
                                        eTTT_num, eTTD_num, eTDD_num, eDDD_num)
    myData.show()

    with pd.option_context('display.max_columns', None):
        print("\n\n")
        print(triad_table)
        print("\n")
    print("Total Time for Program to Run: ", round(time.time() - start, 2))


if __name__ == "__main__":
    print("=====================================")
    fileName = input("Enter the name of the file: \n")
    print("Attempting to read: " + fileName)
    cleanAndFind(fileName)
    print("=====================================")
