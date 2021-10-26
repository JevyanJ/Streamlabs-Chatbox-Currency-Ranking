from System.Collections.Generic import List
import json
import os
import codecs

ScriptName = "Currerncy Ranking"
Website = "twitch.tv/jevyanj"
Description = "Currency Ranking"
Creator = "JevyanJ"
Version = "0.1.0"

configFile = "config.json"
settings = {}
command = "!test"
currentRanking = None


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
            "output": "output.txt",
            "margin": 20,
            "title": 'Ranking'
        }
    currentRanking = getCurrentRanking()
    writeRanking(currentRanking)
    return


def Execute(data):
    global currentRanking
    if data.GetParam(0) != '!test':
        return
    ranking = getCurrentRanking()
    currentRanking = ranking
    writeRanking(ranking)
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


def getCurrentRanking():
    """Return current ranking sorted by Time Watched
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

    currencyUsers = Parent.GetCurrencyUsers(mylist)
    currencyUsersSorted = sorted(
        currencyUsers, key=lambda d: d.TimeWatched, reverse=True)
    return currencyUsersSorted


def writeRanking(ranking):
    """Write ranking on a file
    Args:
        ranking (List<CurrencyUsers>)
    """
    location = os.path.join(os.path.dirname(__file__), settings['output'])

    with open(location, 'w') as f:
        f.write('\n' * settings['margin'])
        f.write('== {} ==\n'.format(settings['title']))
        for user in ranking:
            line = '{} - {}({})'.format(user.UserName,
                                        user.Rank, user.TimeWatched)
            f.write(line)
            f.write('\n')
