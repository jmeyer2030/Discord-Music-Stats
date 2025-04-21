import json
import sys
import re
from pathlib import Path


'''
Get list of json file names
'''
def get_json_file_paths():
    return list(Path(__file__).parent.glob("*.json"))

'''
gets all messages from the .jsons as a list
'''
def get_messages_as_list(pathList):
    allDataList = []
    for path in pathList:
        # Open file from path
        with open(path, "r", encoding = "utf-8-sig") as fileData:
            # Load as list
            jsonData = json.load(fileData)
            
            # If file parsed as lsit, add it to the cumulative list
            if isinstance(jsonData, list):
                allDataList.extend(jsonData)
            else: 
                print("Data is not a list!\n")

    return allDataList

'''
Clears out messages that are not song requests
'''
def remove_non_song_request_messages(dataList):
    i = 0
    while i < len(dataList):
        entry = dataList[i];
        if exclude_entry(entry):
            dataList.pop(i)
            continue

        i = i + 1
    return dataList

'''
Helper for clean_data
Returns true if an entry should be excluded, and false otherwise
An entry should be excluded if:
    - it isn't from FlaviBot
    - it doesn't have "interaction" field (response to user request)
    - it doesn't have "embeds" field (stores song info)
    - embeds doesn't have description (song info)
'''
def exclude_entry(entry):
    sender = entry["author"]["username"]
    if sender != "FlaviBot":
        return True 
    
    if "interaction" not in entry:
        return True
    
    if "embeds" not in entry:
        return True
    
    if len(entry["embeds"]) == 0:
        return True

    if "description" not in entry["embeds"][0]:
        return True

    if len(from_request_get_item(entry['embeds'][0]['description'])) == 0:
        return True
        

    return False

'''
Converts the description into just the song title with a regex
'''
def from_request_get_item(request):
    matches = re.findall('\\[(.*?)\\]', request)
    return matches

'''
Sorts songs by most played, returns it
{
song: 
numPlays:
requesters: {{requester:, numPlays}, ...}
}

'''
def sort_songs_by_most_plays(messageList):
    song_requests_list = []
    for entry in messageList:
        requestedSong = from_request_get_item(entry['embeds'][0]['description'])[0]
        requester = entry['interaction']['user']['username']

        # If it exists already, start false
        foundSong = False
        for d in song_requests_list:
            # for each song, if the songs matches
            if d['song'] == requestedSong:
                # mark as found
                foundSong = True
                # increment total number of plays
                d['numPlays'] = d['numPlays'] + 1
                
                # try to find requester
                foundRequester = False
                for player in d['requesters']:
                    if player['requester'] == requester:
                        foundRequester = True
                        player['numPlays'] = player['numPlays'] + 1
                if not foundRequester:
                    d['requesters'].append({"requester" : requester, "numPlays" : 1})

        if not foundSong:
            song_requests_list.append({"song" : requestedSong, "numPlays" : 1, "requesters" : [{"requester" : requester, "numPlays" : 1}]})
    
    # Sort by total number of plays
    sorted_list = sorted(song_requests_list, key = lambda x : x["numPlays"])
    
    return sorted_list
    
'''
takes the list generated with sort_songs_by_most_played
prints it nicely
'''
def print_songs_by_most_plays(songPlaysList):
    # For each entry
    for entry in songPlaysList:
        print(f"Song: {entry['song']}\nTotal Plays: {entry['numPlays']}")
        for requester in entry['requesters']:
            print(f"    User: {requester['requester']}\n        Times Queued: {requester['numPlays']}")
        print("\n\n------------------------------------------------------------------\n\n")


'''
creates user requests, a list of dictionaries
It's contents have the form:
{
'user' : String user
'numPlays' : int total plays
'songs' : [{'title' : string songTitle, 'numPlays' : int songNumPlays}]
}

Sorts and iterates, and prints from this list
'''
def sort_by_user_plays(messageList):
    user_requests_list = []

    # for each discord message
    for entry in messageList:
        # get requester and the song
        requestItem = from_request_get_item(entry['embeds'][0]['description'])[0]
        requester = entry['interaction']['user']['username']
        
        # try to find the requester
        foundUser = False
        for d in user_requests_list:
            # If we find the requester
            if d['user'] == requester:
                foundUser = True

                #Increment number of user plays
                d['numPlays'] = d['numPlays'] + 1

                # try to find song
                foundSong = False
                for song in d['songs']:
                    if song['title'] == requestItem:
                        foundSong = True
                        song['numPlays'] = song['numPlays'] + 1
                if not foundSong:
                    d['songs'].append({"title" : requestItem, "numPlays" : 1})
        if not foundUser:
            user_requests_list.append({"user" : requester, "numPlays" : 1, "songs" : [{"title" : requestItem, "numPlays" : 1}]})

    # Sort by total number of plays
    sorted_list = sorted(user_requests_list, key = lambda x : x["numPlays"])

    return sorted_list

def print_by_user_plays(userList):
    # For each entry
    for entry in userList:
        print(f"User: {entry['user']}\nTotal Plays: {entry['numPlays']}\nUnique Songs : {len(entry['songs'])}")
        # sort song listing
        entry['songs'] = sorted(entry['songs'], key = lambda x : x["numPlays"], reverse = True)
        print("numPlays | songInfo")
        for song in entry['songs'][:50]:
            print(f"{song['numPlays']}  |  {song['title']}")
        print("\n\n------------------------------------------------------------------\n\n")


def user_mode():
    pathList = get_json_file_paths()
    messageList = get_messages_as_list(pathList)
    songRequestList = remove_non_song_request_messages(messageList)
    songsByUser = sort_by_user_plays(songRequestList)
    print_by_user_plays(songsByUser)


def total_mode():
    pathList = get_json_file_paths()
    messageList = get_messages_as_list(pathList)
    songRequestList = remove_non_song_request_messages(messageList)
    songsByMostPlays = sort_songs_by_most_plays(songRequestList)
    print_songs_by_most_plays(songsByMostPlays)



def main():
    if len(sys.argv) < 2:
        print("Usage: python songRequests.py <mode>\nmodes: user, total")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "user":
        user_mode()
    elif mode == "total":
        total_mode()
    else:
        print(f"Unknown mode: {mode}, use either 'user' or 'total'")






if __name__ == '__main__':
    main()
