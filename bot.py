# ----- Imports ------- #
import random
# --------------------- #

# This is the function that is going to return bots answer back to the client, which sends it to server
# We start with getting the message to lower caps, so the bots doesn't get confused
# since they are caps-sensitive
# Then we check what bot is going to be used to respond and go to their function
def botRespond(message, botName):
    message = message.lower()
    if botName == 'Chad':
        return f'{botName} : {chad(message, botName)}'
    if botName == 'Elsa':
        return f'{botName} : {elsa(message, botName)}'
    if botName == 'Peter':
        return f'{botName} : {peter(message, botName)}'
    if botName == 'Jarvis':
        return f'{botName} : {jarvis(message, botName)}'
    else:
        return f'{botName} : Something went wrong'

findWord = [['hei', 'hello', 'whatsup', 'greeting', 'hey', 'hi'],
            ['bye', 'see ya', 'goodbye']
            ['how', 'what', 'where', 'when']]

# First we define the bot function
# I chose to use a 2 dimensional list, the way it works is that the first row in findWord, is going to be responded
# with the first row in response. The 2nd row in findWord, is going to be responded with 2nd row in response etc..
def chad(message, botname):

    responseArray = [['Whats\'up', 'A human???!', 'My name is Chad', 'Heyheyyy, Chadmoment lol'],
                     ['Byeeee', "See ya later aligator!"],
                     ['You ask so many questions..', 'Just stop', 'What?']]

    # The message, botName findWord and response is then sent to a function that all the bots share,
    # so the code is less complex
    res = botResponse(message, botname, findWord, responseArray)
    if res is None:
        return 'I didnt understand what you just said'
    else:
        return res

# ------------- This is just repeating with the other 3 bots ------------------------- #
def elsa(message, botname):

    responseArray = [['Heyy', 'Hello:)', 'Hii'],
                     ['Cya!', "Oki, byee"],
                     ['Hm.. idk', 'Heh, I cant answer you right now']]

    res = botResponse(message, botname, findWord, responseArray)
    if res is None:
        return 'I didnt understand what you just said'
    else:
        return res


def peter(message, botname):

    responseArray = [['What', 'I want to go home..'],
                     ['FINALLY! I AM FREE', 'Already? Ok bye']
                     ['Do we plan something?']]

    res = botResponse(message, botname, findWord, responseArray)
    if res is None:
        return 'I didnt understand what you just said'
    else:
        return res


def jarvis(message, botname):

    responseArray = [['At your service, sir', 'Check'],
                     ['Shutting off']
                     ['As you wish']]

    res = botResponse(message, botname, findWord, responseArray)
    if res is None:
        return 'I didnt understand what you just said'
    else:
        return res


# -------------------------------------------------------------------------------------------------- #

# Now the botResponse is simple, i in range from the first row, to the last row
# j in range from first column, to the last column in selected row
# if we find the word we are looking for, we respond with random choice of that row's responses
def botResponse(message, botName, findWordArray, responseArray):
    for i in range(len(findWordArray)):
        for j in range(len(findWordArray[i])):
            if findWordArray[i][j] in message:
                return random.choice(responseArray[i])

# This is functions that is not in use, but they work as intended if I wanted to use them
def checkIfMessageHasWordsToLookFor(message, category, responses):
    for t in category:
        if t in message:
            heiRes = format(t+"ing")
            #return "reponse {} with that".format(heiRes+"ing")
            return f'{random.choice(responses)} {getSenderName(message)}'


def getSenderName(message):
    return(message.split()[0]).replace(':', '')
