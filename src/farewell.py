import random
from util import util_func

# get goodbye synonyms
synonyms = util_func.get_synonyms("goodbye")
synonyms.append("exit")

# INTENT MATCHING: check if user wants to exit the system
def check(input):
    # exit
    if input.lower() == "goodbye":
        return True

# REPLY: respond to "goodbye" command
def reply(name):
    # say goodbye to user
    name_string = ""
    if (name != None):
        name_string = f", {name}"
    print("Hadley: " + getBye() + name_string + "! See you again later!")

# get a farewell synonym
def getBye():
    bye = synonyms
    bye.remove("exit")
    bye.remove("good by")
    bye.remove("goodby")
    bye = bye[random.randint(0, len(bye)-1)]
    bye = bye[0].capitalize() + bye[1:]
    return bye

# check if input is a synonym of the "goodbye" command
def bye_syn(input):
    # remind user to use 'goodbye'
    if input.lower() in synonyms:
        return True
    return False