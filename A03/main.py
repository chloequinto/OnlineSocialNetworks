"""
Chloe Quinto 
CS - 581 WS 
Online Social Networks 
Assignment 3 
I pledge my honor that I have abided by the Stevens Honor System - Chloe Quinto
"""

from apiclient.discovery import build 
import csv 

API_KEY = "AIzaSyAAgQB9UpJXqvdYfHAiyW6nfz94FVSP5tQ"
API_NAME = "youtube"
API_VERSION = "v3"

YouTubeObject = build(API_NAME, API_VERSION, developerKey = API_KEY)



def OutputVideoCount(resultVidCount):
    print("Before: \n")
    print(resultVidCount)
    print("After: \n")
    resultVidCount = sorted(resultVidCount.keys())
    print(resultVidCount[key])
    # for key, value in sorted(resultVidCount.items()):
    #     print("%s:" % resultVidCount[key])

def ranking(results, numResults): 
    '''
    Functions takes the result from the API call  
    Returns title, videoId, viewCount, likes, dislikes 
    '''
    printVidCount, printLikes, printDislikes = {}, {}, {}
    print("--------viewsRanking---------")

    items = results["items"] # A list of activities, or events, that match the request criteria.
    print("LengthOfResults: " + str(numResults))
    print('-----')
    for i in range(len(items)): 
        videoNum = items[i]

        title = videoNum["snippet"]["title"]
        videoId = videoNum["id"]["videoId"]

        videoResponse = YouTubeObject.videos().list(id=videoId, part="statistics").execute()
        videoItems = videoResponse["items"][0]
        viewCount = videoItems["statistics"]["viewCount"]
        likes = videoItems["statistics"]["likeCount"]
        dislikes = videoItems["statistics"]["dislikeCount"]

        print("Title: " + str(title))
        print("VideoId: " + str(videoId))
        print("ViewCount: " + str(viewCount))
        print("Likes: " + str(likes))
        print("Dislikes: " + str(dislikes))
        percentLikes = int(likes)/int(viewCount)
        percentDislikes = int(dislikes)/int(viewCount)

        print('--------')

        printVidCount[viewCount] = {title, videoId, viewCount}
        printLikes[likes] = {title, videoId, percentLikes}
        printDislikes[dislikes] = {title, videoId, percentDislikes}
    print("--------- Ranking Videos -------------")
    print(printVidCount)
    OutputVideoCount(printVidCount)
    # print('----hue------')
    # print(printLikes)
    # print('----hue------')
    # print(printDislikes)
    # print('----hue------')



def createCSV(results):
    header = []
    for key, value in results.items(): 
        header.append(key)
    with open("results.csv", "w") as csvfile: 
        filewriter = csv.writer(csvfile)
        filewriter.writerow(header)

def searchYoutube(term, max_results): 
    '''
    Executes YouTube API call given the search term "term" and the number of results "max_results"
    Returns response body 
    '''
    response = YouTubeObject.search().list(q = term, part="id, snippet", maxResults = max_results).execute()
    print("Search Term: " + term)
    print("Search Max: " + max_results)
    print("Results:\n" + str(response))

    print("-----------End of Result-----------")
    return response 

if __name__ == "__main__":
    query = input("What would you like to search?\n")
    numResults = input("How many results would you like?\n")
    print("-----------Searching-----------")
    resultQuery = searchYoutube(query, numResults)
    createCSV(resultQuery)
    ranking(resultQuery, numResults)

    """
    To Do 
    1. List the rank (1 to 5), the title, id, and views for top 5 videos with the highest views 
    """