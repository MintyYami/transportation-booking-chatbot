import random
from datetime import datetime
from util import util_func
import identity_management
import booking
import small_talk
import QA
import discovery
import farewell

if __name__ == "__main__":
    # start with uninitialised name
    name = None
    ignore_input = False

    # introduction
    greet = "Good morning" if datetime.now().hour < 13 else "Good afternoon" if datetime.now().hour < 18 else "Good evening"
    print(
        f"Hadley: {greet}! My name is Hadley, your friendly chatbot. I am mainly here to assist you in making transportation bookings.")
    print("        However, I can also assist you in other simple chatbot tasks :)")
    print("        Note - when you are done with me, just say \"goodbye\" to let me know!")

    while True:
        # check if new input needed
        if (not ignore_input):
            # get user input
            user_input = util_func.get_input(name)
        # reset ignore input
        ignore_input = False

        # INTENT MATCHING: check greeting
        if (identity_management.check_hello(user_input)):
            name = identity_management.reply_hello(name)
            continue

        # INTENT MATCHING: check identity management
        identity = identity_management.check_identity(user_input)
        if (identity):
            # ask for identity
            if (identity == 1):
                name = identity_management.reply_identity1(name)
            elif (identity == 2):
                name = identity_management.reply_identity2(user_input)
            continue

        # INTENT MATCHING: check transportation booking
        answer_type, confidence = booking.check(user_input)
        if (answer_type == 1): # intent: user want to make reservation
            if confidence <= 0.80:
                # check if user wants to make reservation if confidence level lower than 85%
                print("Hadley: I predict that you are trying to make a transportation reservation. Is this correct? (y/n)")
                confirmation = util_func.get_confirmation(name)
                # to skip confirmation and process new input
                if (isinstance(confirmation, str)):
                    ignore_input = True
                    user_input = confirmation
                    continue
                # skip back to beginning of input loop if confirmation is denied
                if not confirmation:
                    continue
            # if confidence is high or user explicitly confirmed, start resservation
            booking.startTransaction(user_input, name)
            continue
        elif (answer_type == 2): # intent: user want to view reservation
            if confidence <= 0.80:
                # check if user wants to view reservation if confidence level lower than 80%
                print("Hadley: I predict that you are trying to view a transportation reservation. Is this correct? (y/n)")
                confirmation = util_func.get_confirmation(name)
                # to skip confirmation and process new input
                if (isinstance(confirmation, str)):
                    ignore_input = True
                    user_input = confirmation
                    continue
                # skip back to beginning of input loop if confirmation is denied
                if not confirmation:
                    continue
            # if confidence is high or user explicitly confirmed, start resservation
            booking.viewTransaction(user_input, name)
            continue

        # INTENT MATCHING: check small talk
        answer, ask_user_back = small_talk.check(user_input)
        if (answer != None):
            print("Hadley: " + answer)
            if (ask_user_back):
                # randomly ask user back
                if (random.randint(0, 4)):
                    print("        How about yourself?")
                    input_new = util_func.get_input(name)
                    small_talk.check_sentiment(input_new, 0.65, 0.60)
            continue

        # INTENT MATCHING: check QA
        answer = QA.check(user_input)
        if (answer != None):
            if (isinstance(answer, str)):
                print("Hadley: " + answer)
            else:
                print(f"Hadley: I found the question \"{answer[0]}\" in my database. Is that what you mean? (y/n)")
                user_input = util_func.get_confirmation(name)
                # to skip confirmation and process new input
                if (isinstance(user_input, str)):
                    ignore_input = True
                    continue
                # confirmation: answer printed to user
                if user_input:
                    print(f"Hadley: Okay! {answer[1]}")
            continue

        # INTENT MATCHING: check discoverability
        if (discovery.check(user_input)):
            discovery.reply()
            continue

        # INTENT MATCHING: check for "goodbye" command
        if farewell.check(user_input):
            farewell.reply(name)
            break

        # INTENT MATCHING: exit commands synonym error handling
        if farewell.bye_syn(user_input):
            print("Hadley: I predict that you want to exit my program. Is that true? (y/n)")
            user_input = util_func.get_confirmation(name)
            # to skip confirmation and process new input
            if (isinstance(user_input, str)):
                ignore_input = True
                continue
            # confirmation: system is exited
            if user_input:
                break
            print("        Reminder that you can say 'goodbye' directly to exit my program!")
            continue

        # unknown intent found
        print("Hadley: I'm sorry, I don't quite understand what you mean.")

        # show a discoverability to help user
        print(discovery.get_discovery_hint())

    # give farewell to user
    print("Hadley: Thank you for keeping me company. I hope you found me useful :)")
    print("        See you later!")
