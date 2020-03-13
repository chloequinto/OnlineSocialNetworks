import csv
import networkx as nx 

class Graph: 
    def __init__(self, reviewer, reviewee, trustLevel):
        self.reviewer = reviewer
        self.reviewee = reviewee
        self.trustLevel = trustLevel 


class Info: 
    def __init__ (self, selfLoops): 
        self.selfLoops = 1

def openAndPrint(fileName): 
    with open(fileName) as csvFile: 
        for row in csvFile: 
            row = row.replace("\n", "") # get rid of new line breaks 
            line = row.split(",") # split into an array 
    

            Graph.reviewer = line[0]
            Graph.reviewee = line[1]
            Graph.trustLevel = line[2]

            if (Graph.reviewer == Graph.reviewee): 
                # this is a self loop 
                print("We found a self loop!")
                Info.selfLoops += 1 
 
    # print(Info())
    return None
if __name__ == "__main__":

    print("=====================================")
    fileName = input("Enter the name of the file: \n")
    openAndPrint(fileName)
    print("=====================================")
