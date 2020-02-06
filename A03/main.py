"""
Chloe Quinto 
CS - 581 WS 
Online Social Networks 
Assignment 3 
I pledge my honor that I have abided by the Stevens Honor System - Chloe Quinto

main.py - A Python program that makes an API call to youtube given a query and number of results. The program 
also writes the result to CSV and 
"""

from apiclient.discovery import build 
import csv 

API_KEY = "AIzaSyAAgQB9UpJXqvdYfHAiyW6nfz94FVSP5tQ"
API_NAME = "youtube"
API_VERSION = "v3"

YouTubeObject = build(API_NAME, API_VERSION, developerKey = API_KEY)


def OutputVideoCount(resultVidCount):
    #Function sorts and prints out title, videocount and id onto the console based on the highest view count. 
    print("--------- Ranking View Count -------------")
    viewCount = sorted(resultVidCount.items(), key=lambda x: int(x[0]), reverse=True)
    rank = 1 
    for key, value in viewCount: 
        print("Rank: " + str(rank) +  " Title:  " +str(value.get("title")) + " Video ID: "  + str(value.get("videoId")) + " ViewCount: " + str(key))
        rank+=1 
        if rank == 6:
            break
    print("\n")
    return None

def OutputLikesCount(resultLikes):
    #Function sorts and prints out title, videocount and id onto the console based on the highest percentage of likes. 
    print("--------- Ranking Like Count -------------")
    likeCount = sorted(resultLikes.items(), key=lambda x: float(x[0])*100, reverse=True)
    rank = 1 
    for key, value in likeCount: 
        percent = round((value.get("percentLikes") * 100), 5)
        print("Rank: " + str(rank) +  " Title:  " +str(value.get("title")) + " Video ID: "  + str(value.get("videoId")) + " Percent Likes: " + str(percent))
        rank+=1 
        if rank == 6: 
            break
    print("\n")
    return None

def OutputDislikesCount(resultDislikes): 
    #Function sorts and prints out title, videocount and id onto the console based on the highest percentage of dislikes. 
    print("--------- Ranking Dislikes Count -------------")
    dislikeCount = sorted(resultDislikes.items(), key=lambda x: float(x[0])*100, reverse=True)
    rank = 1 
    for key, value in dislikeCount: 
        percent = round((value.get("percentDislikes") * 100), 5)
        print("Rank: " + str(rank) +  " Title:  " +str(value.get("title")) + "  Video ID:  "  + str(value.get("videoId")) + "  Percent Dislikes:  " + str(percent))
        rank+=1 
        if rank == 6: 
            break
    print("\n")
    return None

def ranking(results, numResults): 
    #Function takes the results from the API call and number of searches and partitions data 

    printVidCount, printLikes, printDislikes = {}, {}, {}
    items = results["items"] # A list of activities, or events, that match the request criteria.
    for i in range(len(items)): 
        videoNum = items[i]

        title = videoNum["snippet"]["title"]
        videoId = videoNum["id"]["videoId"]

        videoResponse = YouTubeObject.videos().list(id=videoId, part="statistics").execute()

        videoItems = videoResponse["items"][0]
        viewCount = videoItems["statistics"]["viewCount"]
        likes = videoItems["statistics"]["likeCount"]
        dislikes = videoItems["statistics"]["dislikeCount"]
        percentLikes = (int(likes)/int(viewCount))
        percentDislikes = (int(dislikes)/int(viewCount))


        printVidCount[viewCount] = {"title": title, "videoId" : videoId, "viewCount ": viewCount}
        printLikes[percentLikes] = {"title": title, "videoId": videoId, "percentLikes":percentLikes}
        printDislikes[percentDislikes] = {"title": title, "videoId":videoId, "percentDislikes":percentDislikes}
    

    return OutputVideoCount(printVidCount), OutputLikesCount(printLikes), OutputDislikesCount(printDislikes)


def writeToCSV(results):
    #Function takes the results from the API call and writes to CSV
    content, header, vals = [], [], []
    
    for key in results: 
        header.append(key)
        vals.append(results[key])

    with open("results.csv", "w") as csvfile: 
        filewriter = csv.writer(csvfile)
        filewriter.writerow(header)
        filewriter.writerow(vals)
    return None 



def searchYoutube(term, max_results): 
    # Function takes in the term queried and number of results and makes an API call. 
    response = YouTubeObject.search().list(q = term, part="id, snippet", maxResults = max_results).execute()

    print("Search Term: " + term)
    print("Search Max: " + max_results)
    print("Results:\n" + str(response))

    print("-----------End of Searching-----------\n")
    return response 

if __name__ == "__main__":

    query = input("What would you like to search?\n")

    if len(query)== 0:
        raise Exception("Sorry, you need to search at least something.")

    numResults = input("How many results would you like?\n")
    if int(numResults) == 0 or int(numResults) < 0: 
        raise Exception("Sorry, we need you to choose a number > 0.")

    print("-----------Searching-----------")

    resultQuery = searchYoutube(query, numResults)
    writeToCSV(resultQuery)
    ranking(resultQuery, numResults)

