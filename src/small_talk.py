import random
from bs4 import BeautifulSoup
from urllib import request
from util import util_classifier, util_text_process


# INTENT MATCHING: check if user is trying to make small talk
def check(user_input):
    id, content, confidence = util_text_process.process_query_with_matrix(user_input.lower(), "small_talk", ".csv", 0.85)
    if (id != None):
        return reply(content, id, confidence)
    return None, False

# REPLY: respond to small talk appropriately
def reply(content, id, confidence):
    ansID = content["AnswerID"].iloc[id]
    reply = ""
    if ansID == 1:
        if(confidence < 0.95):
            reply = "I think you are asking me how I am!\n        "
        return reply+get_reply1(), True
    if ansID == 2:
        if (confidence < 0.95):
            reply = "I think you are asking me about the weather, so here it is:\n        "
        return reply+get_reply2(), False
    if ansID == 3:
        return get_reply3(), False

# get reply for small take with AnswerID 1
def get_reply1():
    response = [
        "I'm doing great, thank you!",
        "I'm not too shabby!",
        "I'm doing really well now that I'm talking to you :)",
        "I'm doing good. Thanks for asking!"
    ]

    id = random.randint(0, len(response)-1)
    return response[id]

# get reply for small take with AnswerID 2
def get_reply2():
    temp1, temp2 = readWeather()
    response = f"The temperature in Nottingham today ranges between {temp1}ºC and {temp2}ºC."

    if int(temp2) < 15:
        response += "\n        That is pretty cold isn't it!"
    elif int(temp1) > 15:
        response += "\n        That is pretty warm isn't it!"
    else:
        response += "\n        I think the weather today feels quite nice!"

    return response

# get reply for small take with AnswerID 3
def get_reply3():
    response = [
        "No worries!",
        "It's my pleasure :)",
        "Not a problem!",
        "It's my job, after all!",
        "I'm happy to help.",
        "Happy to assist."
    ]

    id = random.randint(0, len(response)-1)
    return response[id]

# check for sentiment of user input, using a classifier
def check_sentiment(user_input, threshold_high, threshold_low):
    label_dir = {
        "positive": ["data/sentiment/positive"],
        "negative": ["data/sentiment/negative"]
    }
    pred, confidence = util_classifier.input_check_classifier(user_input, "train_sentiment", label_dir)

    if confidence >= threshold_high:
        if pred == "positive":
            print("Hadley: I'm glad to hear you are good!")
        else:
            print("Hadley: I'm sorry if you're not feeling too awesome right now :( Maybe booking a trip to somewhere fun can help?")
    elif confidence >= threshold_low:
        if pred == "positive":
            print("Hadley: I predicted that you are doing well! I hope that's true!")
        if pred == "negative":
            print("Hadley: I'm sensing possible negativity in your reply. If it is correct, then I am sorry :/")
    else:
        print("Hadley: Sadly, I'm just a robot who's not very good at understanding emotions. I do hope you are well, and if not, hope you feel better soon!")

# scrape weather temperatures from the Met Office website
def readWeather():
    url = "https://www.metoffice.gov.uk/weather/forecast/gcrjm8jf7"
    content = BeautifulSoup(request.urlopen(url).read(), 'html.parser').get_text()

    textContent = []
    for line in content.splitlines():
        if line.strip() != '':
            textContent.append(line.strip())
    i = textContent.index("Today")
    temps = textContent[i+1].split("   ")

    return (temps[1].split(" ")[0]), (temps[0].split(" ")[0])