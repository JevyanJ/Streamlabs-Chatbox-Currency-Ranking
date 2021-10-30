import codecs
import os
import json
from System.Collections.Generic import List

ScriptName = "Currerncy Ranking"
Website = "twitch.tv/jevyanj"
Description = "Currency Ranking"
Creator = "JevyanJ"
Version = "0.1.0"

configFile = "config.json"
settings = {}
command = "!test"
currentRanking = None

output = "web/index.html"
templates = {
    "index": "templates/index.template",
    "category": "templates/category.template"
}


def Init():
    global settings, currentRanking

    path = os.path.dirname(__file__)

    try:
        with codecs.open(
                os.path.join(path, configFile),
                encoding='utf-8-sig',
                mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except Exception:
        settings = {
        }
    process()
    return


def Execute(data):
    global currentRanking
    if data.GetParam(0) == '!test' and data.UserName == 'JevyanJ':
        process()
        Parent.SendStreamMessage('Ranking file updated')
    return

def log(message):
    Parent.Log(command, str(message))
    return


def ReloadSettings(jsonData):
    Init()

    return


def OpenReadMe():
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)
    return


def Tick():
    return


def process():
    """Main process
    """
    users = getStreamlabsUsers()
    ranking = prepareRanking(users)
    order = getOrderRanking(users)
    writeRanking(ranking, order)

def equalRankin(ranking, other):
    """Compare two rankings
    Args:
        ranking (List<CurrencyUsers>)
        other (List<CurrencyUsers>)

    Return:
        Boolean. True if both ranking are equals.
    """
    if not other or not ranking:
        return False
    if len(ranking) != len(other):
        return False

    for user in ranking:
        user_other = next(
            (item for item in other if item.UserId == user.UserId), None)
        if not user_other or user_other.TimeWatched != user.TimeWatched:
            return False

    return True

def getStreamlabsUsers():
    """Return all users with streamlabs format
    Return:
        List<CurrencyUsers>

        CurrencyUsers:
            string UserId
            string UserName
            long Points
            long TimeWatched (In Minutes)
            string Rank
    """
    top = Parent.GetTopHours(-1)
    users = top.keys()
    mylist = List[str](users)

    return Parent.GetCurrencyUsers(mylist)

def prepareRanking(users):
    """Prepare ranking with a CurrencyUsers list
    Args:
        users (List<CurrencyUsers>): List of streamlabs users
    Return:
        Dict:
        {
            'rank1': [user1, user2,...],
            'rank2': [...]
        }
    """
    output = {}
    for user in users:
        if user.Rank in output.keys():
            output[user.Rank].append(user.UserName)
        else:
            output[user.Rank] = [user.UserName]
    return output

def getOrderRanking(users):
    """Return a ranking ordered list.
    Args:
        users (List<CurrencyUsers>): List of streamlabs users
    Return:
        List<str>
    """

    usersSorted = sorted(
        users, key=lambda d: d.TimeWatched, reverse=True)
    ranking = []
    for user in usersSorted:
        if user.Rank not in ranking:
            ranking.append(user.Rank)
    return ranking

def writeRanking(rankings, order):
    """Write ranking on a file
    Args:
        ranking (Dict)
    """
    location = os.path.join(os.path.dirname(__file__), output)

    category_file = os.path.join(
        os.path.dirname(__file__), templates["category"])
    file = open(category_file, mode='r')
    category_template = file.read()
    file.close()

    rankings_txt = ""
    for ranking in order:
        users = rankings[ranking]
        ranking_users = ""
        for user in users:
            ranking_users += "<p>{}</p>\n".format(user)
        rankings_txt += category_template.format(
                NAME=ranking, ELEMENTS=ranking_users)

    index_file = os.path.join(
        os.path.dirname(__file__), templates["index"])
    file = open(index_file, mode='r')
    index_template = file.read()
    file.close()
    with open(location, 'w') as f:
        f.write(index_template.format(RANKING=rankings_txt))
