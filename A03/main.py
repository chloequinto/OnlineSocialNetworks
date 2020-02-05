"""
Chloe Quinto 
CS - 581 WS 
Online Social Networks 
Assignment 3 
I pledge my honor that I have abided by the Stevens Honor System - Chloe Quinto
"""

"""
To Do 
1. Complete OutputVideoCount
2. Complete OutputLikesCount
3. Complete OutputDislikesCount
2. Complete function writeToCSV

"""

from apiclient.discovery import build 
import csv 

API_KEY = "AIzaSyAAgQB9UpJXqvdYfHAiyW6nfz94FVSP5tQ"
API_NAME = "youtube"
API_VERSION = "v3"

YouTubeObject = build(API_NAME, API_VERSION, developerKey = API_KEY)


def OutputVideoCount(resultVidCount):
    '''
    Description: 
        Function sorts and prints out title, videocount and id onto the console based on the highest view count. 

    Parameters: 
        resultsVidCount: A dictionary with keys as the videoCount and values as the title, videoCount and ID 

    Returns: 
        str: returns str to be printed  
    '''
    print("Before: \n")
    print(resultVidCount)
    print("After: \n")
    resultVidCount = sorted(resultVidCount.keys())
    print(resultVidCount[key])
    # for key, value in sorted(resultVidCount.items()):
    #     print("%s:" % resultVidCount[key])

def OutputLikesCount(resultLikes):
    '''
    Description: 
        Function sorts and prints out title, videocount and id onto the console based on the highest likes 

    Parameters: 
        resultLikes: A dictionary with keys as the likes and values as the title, videoCount and ID 

    Returns: 
        str: returns str to be printed  
    '''
    return None 

def OutputDislikesCount(resultDislikes): 
    '''
    Description: 
        Function sorts and prints out title, videocount and id onto the console based on the highest dislikes 

    Parameters: 
        resultLikes: A dictionary with keys as the dislikes and values as the title, videoCount and ID 

    Returns: 
        str: returns str to be printed  
    '''
    return None

def ranking(results, numResults): 
    '''
    Description: 
        Function takes in results and number of results and extracts title, videocount, id, likes, dislikes etc. 

    Parameters: 
        results: JSON response from API query 
        numResults: number of queries the user wants 

    Returns: 
        dict: returns dictionary of partitioned data based on videoCount, likes, and dislikes 
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



def writeToCSV(results):
    header = []
    for key, value in results.items(): 
        header.append(key)
    with open("results.csv", "w") as csvfile: 
        filewriter = csv.writer(csvfile)
        filewriter.writerow(header)

def searchYoutube(term, max_results): 
    '''
    Description: 
        Function takes in results and number of results and makes an API call. 

    Parameters: 
        term: query from the user 
        max_results: number of results the user wants 

    Returns: 
        JSON Response: returns json response from API call 
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
    writeToCSV(resultQuery)
    ranking(resultQuery, numResults)

