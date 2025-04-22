import random
from util import util_text_process

# tasks of chatbot
tasks = {
    "Main task": "assist you in making transportation bookings (type \"make / view reservation\").",
    "Intent matching": "I can identify and match similarity-based intent matching.",
    "Identity management": "I can keep track of who you are!",
    "Question answering": "I can answer factual questions you have using information from my dataset.",
    "Small talk": "I cam reply to simple greetings and answer questions about the weather!"
}

# INTENT MATCHING: check if user wants to discover more
def check(user_input):
    discover = ["do", "task", "help"]
    return util_text_process.process_query_with_list(user_input, discover, 0.7)

# REPLY: respond to discovery query
def reply():
    print(f"Hadley: My main task is to {tasks["Main task"]}")
    print("        However, I can also assist you in other simple chatbot tasks, such as...")
    for task in tasks:
        if(task != "Main task"):
            print(f"        • {task} - {tasks[task]}")

# return one discovery point or hint to user
def get_discovery_hint():
    id = random.randint(0, len(tasks))
    # hint to discover more
    if(id == len(tasks)):
        return "        To discover what I can help you with, type 'help'."

    task_key = list(tasks.keys())[id]

    if (id == 0):
        connect = ", as it is my"
    else:
        connect = " through"

    # a task the chatbot can do
    return f"        Something I can do: {tasks[task_key][:-1]}{connect} {task_key.lower()}."