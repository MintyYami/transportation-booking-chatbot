import random
from util import util_func, util_text_process

# get greeting synonyms
synonyms = util_func.get_synonyms("hi")
synonyms.append("hey")

# INTENT MATCHING: check if user is greeting chatbot
def check_hello(input):
    if input.lower() in synonyms:
        return True
    return False

# REPLY: respond to greeting and get name is uninitialised
def reply_hello(name):
    if name == None:
        print(f"Hadley: {get_hi()}! What is your name?")
        name = set_name()
        print(f"Hadley: Nice to meet you {name}. I'm Hadley - but you already know that :)")
    else:
        print(f"Hadley: {get_hi()}, {name}.")
    return name

# INTENT MATCHING: check if input is about user identity
def check_identity(user_input):
    # check for name-changing commands
    input_tokens = util_text_process.preprocess_small(user_input)
    change = len([word for word in input_tokens if word in ["rename", "change", "set"]]) == 0

    # return 1 if intent is asking for name (only if name-changing commands not in user_input)
    if(change):
        id, content, confidence = util_text_process.process_query_with_matrix(user_input, "ask_name", ".csv", 0.9)

        if(id != None):
            return 1

    # return 2 if intent is asking to rename
    rename_commands = ["rename", "change", "set", "call", "me", "my", "name", "as"]
    if util_text_process.process_query_with_list(user_input, rename_commands, 0.6):
        return 2

    # return 0 if not asking identity
    return 0

# REPLY: respond to asking for name
def reply_identity1(name):
    if(name == None):
        print(f"Hadley: I'm not sure... What should I call you?")
        name = set_name()
        print(f"Hadley: Okay, let me write that down! Nice to meet you, {name} :)")
    else:
        print(f"Hadley: Your name is {name}!")
    return name

# REPLY: respond to asking for name change
def reply_identity2(user_input):
    name = util_func.get_name_from_input(user_input)
    if(name == None):
        print(f"Hadley: What would you like me to call you?")
        name = set_name()
    print(f"Hadley: Okay! Your name is now {name}.")
    return name

# get a greeting synonym
def get_hi():
    hi = synonyms[random.randint(0, len(synonyms)-1)]
    hi = hi[0].capitalize() + hi[1:]
    return hi

# get and set user's name
def set_name():
    name = None
    while name == None:
        user_input = util_func.get_input(name)
        user_preprocessed = util_text_process.preprocess_small(user_input)
        # get only the name
        if(len(user_preprocessed) == 1):
            name = user_input
        else:
            name = util_func.get_name_from_input(user_input)
        # ERROR HANDLING: reprompt for name
        if(name == None):
            print("Hadley: Sorry... I didn't quite get your name.")
            print("        Can you please more clearly state your name?")
        # disallow bad words be being set as names
        elif(util_func.is_swear(name)):
            print("Hadley: Haha, very funny... But you can't use inappropriate words as your name!")
            print("        Can you please state your actual name?")
            name = None
    return name
