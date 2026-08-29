import requests
import mariadb
from bs4 import BeautifulSoup 

# builds a url with the given user for tracker.gg
# allSeasons is the check for anything if the account hasn't played this season
def urlBuild(valorantAccount, allSeasons):
    unbuiltUrl = "https://tracker.gg/valorant/profile/riot/"
    valName = ""
    valID = ""
    valNameComplete = False

    for i in range (0, len(valorantAccount)):
        if (valorantAccount[i] == " "):
            valNameComplete = True
        if (valorantAccount[i] and valNameComplete == False):
            valName += valorantAccount[i]  
        if ((valorantAccount[i] != " " and valorantAccount[i] != "#") and valNameComplete == True):
            valID += valorantAccount[i]

    builtUrl = unbuiltUrl + valName + "%23" + valID + "/overview"

    if (allSeasons == True):
        builtUrl += "?playlist=competitive&season=all"

    print("Checking URL: [ " + builtUrl + " ]")

    return builtUrl

# to pull valorant info offline given a url
def rankPull(url):
    try:
        result = requests.get(url)
        valorantHTML = BeautifulSoup(result.text, "html.parser")

        # beautiful soup returns html as a list with usually one element being the entire thing
        # this function seaches for the 1rst instance of valorant-rank, and call upon the lists
        # first element[0] to then call upont the .string within it, setting it equal to valorantRank
    
        valorantRank = (valorantHTML.find_all("div", class_="valorant-rank-bg", limit=1))[0].string
    except:
        valorantRank = "failed"

    return valorantRank

# fixes the stupid spaces
#(takes advantage that just the ends that need deleting)
def rankFix(rank):
    fixedRank = ""
    for i in range(0, len(rank)):
        if (i > 0 and i < len(rank) - 1):
            fixedRank += rank[i]
    return fixedRank

# tests to see if it can pull anything from the website
# calls addAccount (message is for the user ID)
def accountVerify(valorantAccount):
    verifiedAccount = [False, "", ""]
    accountUrl = urlBuild(valorantAccount, False)
    accountRank = rankPull(accountUrl)

    # looking for account if they havent played in the current season
    if (accountRank == "failed"):
        accountUrl = urlBuild(valorantAccount, True)
        accountRank = rankPull(accountUrl)

    if (accountRank != "failed"):
        verifiedAccount[0] = True
        verifiedAccount[1] = accountUrl
        verifiedAccount[2] = rankFix(accountRank)

    return verifiedAccount

def connectMaria():
    print("\n--- Logging Into Database ---")
    try:
        connection = mariadb.connect( # temp for development
            user="",
            password="",
            host="",
            port="3306",
            database="ranksDatabase")
        print("[ Database Connection Successful ]")
        return connection
    except:
        print("Connection Faliure: [ Database Login Failed ]")

def disconnectMaria(connection):
    connection.close()

# to check if theres a table for the current server if not make one
def guildCheck(cursor, currentGuild):
    print("[ Checking for Guild Table ]")
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + str(currentGuild) + "`(" 
                   + "temporary varchar(100)"
                   + ")")
    
    cursor.execute("SHOW TABLES") 
    for i in cursor:
        print(str(i))

def deleteGuild():
    print("delete guild table")

def addAccount(guildID, userID, accountArray):
    connection = connectMaria()
    cursor = connection.cursor()
    guildCheck(cursor, guildID)

# wont take argument connection but will probably get a new one
def updateRole(connection):
    print("Update Role")

    if (connection != None):
        disconnectMaria(connection)

# will generate a report of updated account, showing successes
# and failiures, also will run on a clock
def updateAll():
    print("update all")
