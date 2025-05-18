import requests
import time

def get_id_from_user(user):
    url = "https://users.roblox.com/v1/usernames/users"
    response = requests.post(url, json={"usernames": [user], "excludeBannedUsers": False})

    if response.status_code == 200:

        data = response.json()
        if data["data"]:
            return data["data"][0]["id"]
        else:
            print("Username not found.")
    else:
        print("API Error: " + response.status_code)
    
    return -1

def check_inv_public(userid): 
    invPublic = requests.get("https://inventory.roblox.com/v1/users/" + str(userid) + "/can-view-inventory")
    invPublic = invPublic.json()

    if "errors" in invPublic:
        print((invPublic["errors"])[0]["message"]) 
    elif "canView" in invPublic:
        print(invPublic["canView"])
    else:
        print("Unknown error") 

def calculate_rap(userid):
    nextPage = True
    cursor = 0
    rap = 0

    limiteds = requests.get("https://inventory.roblox.com/v1/users/" + str(userid) + "/assets/collectibles")
    limiteds = limiteds.json()

    if "errors" in limiteds:
        if limiteds["errors"][0]["code"] == 11:
            print("Private inv")
        elif limiteds["errors"][0]["code"] == 1:
            print("User doesnt exist")
        else:
            print("Unknown error")
        rap = -1
    elif "data" in limiteds:
        if len(limiteds["data"]) > 0:
            for x in limiteds["data"]:
                rap = rap + x["recentAveragePrice"]
    
        if limiteds["nextPageCursor"] == None:
            nextPage = False
        else:
            cursor = limiteds["nextPageCursor"]

    while nextPage == True:
        time.sleep(0.5)

        limiteds = requests.get("https://inventory.roblox.com/v1/users/" + str(userid) + "/assets/collectibles?cursor=" + cursor)
        limiteds = limiteds.json()

        if "errors" in limiteds:
            if limiteds["errors"][0]["code"] == 11:
                print("Private inv")
            elif limiteds["errors"][0]["code"] == 1:
                print("User doesnt exist")
            else:
                print("Unknown error")
            rap = -1
        elif "data" in limiteds:
            if len(limiteds["data"]) > 0:

                for x in limiteds["data"]:
                    rap = rap + x["recentAveragePrice"]

            if limiteds["nextPageCursor"] == None:
                nextPage = False
            else:
                cursor = limiteds["nextPageCursor"]
                

    return rap

def get_user_rap(username):
    userId = get_id_from_user(username)

    if userId == -1:
        return "N/A"
    else:
        userRap = calculate_rap(userId)
        if userRap == -1:
            return "N/A"
        else:
            return(str(userRap))
            
