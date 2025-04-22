import nltk
import pandas as pd
from nltk.corpus import wordnet
from nltk import word_tokenize
from . import util_text_process

swear_list = set()

# get user input with error handling
def get_input(name):
    while True:
        # get user input
        if name != None:
            user_input = input(f"{name}: ")
        else:
            user_input = input("User: ")

        # ERROR HANDLING: ignore empty input until not empty
        if (user_input != ""):
            return user_input

# retrieve confirmation or new user input
def get_confirmation(name):
    user_input = get_input(name)
    if (user_input.lower() in ["y", "yes"]):
        return True
    if (user_input.lower() in ["n", "no"]):
        print("Hadley: Let's not do that then!")
        return False
    else:
        return user_input

# check if word is in the bad word list
def is_swear(word):
    # get swear words into set, if haven't done so
    if len(swear_list) == 0:
        content = pd.read_csv(('data/badwords.csv'), index_col=False)
        for swear in content['Swears']:
            swear_list.add(swear)

    return True if word.lower() in swear_list else False

# find name from input using tagger
def get_name_from_input(user_input):
    user_preprocessed = util_text_process.preprocess_small(user_input)
    none_names = ["name", "rename", "change", "set", "call"]

    # use tagging to help identify the name
    post = nltk.pos_tag(user_preprocessed, tagset='universal')
    for i in range(len(post)):
        word, tag = post[i]
        if (tag == "NOUN") and (word not in none_names):
            # get the unprocessed token to account for capitalisation of input
            name = [n for n in word_tokenize(user_input) if n.lower() == word][0]
            if(not is_swear(name)):
                return name
    return None

# get synonyms of a word
def get_synonyms(word):
    synonyms = []

    # fetch synonyms from WordNet
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    # remove duplicates
    synonyms = list(set(synonyms))

    # remove capital letters and replace "-", "_"
    for i in range(len(synonyms)):
        newSym = synonyms[i].lower()
        newSym = newSym.replace("-", " ")
        newSym = newSym.replace("_", " ")
        synonyms[i] = newSym
    return list(set(synonyms))  # remove repetition