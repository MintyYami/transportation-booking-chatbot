from util import util_text_process

# INTENT MATCHING: check if user is trying to ask question from the dataset
def check(user_input):
    id, content, confidence = util_text_process.process_query_with_matrix(user_input.lower(), "QA_dataset", ".csv", 0.70)

    if (id != None):
        return reply(content, id, confidence)
    return None

# REPLY: retrieve the correct answer for a question
def reply(content, id, confidence):
    # return answer confidently
    if (confidence >= 0.90):
        return content["Answer"].iloc[id]
    # return answer with implicit confirmation
    if (confidence >= 0.80):
        return (f"To answer \"{content["Question"].iloc[id]}\", {content["Answer"].iloc[id]}")
    # return both question and answer, to be explicitly asked to user when confidence level between 70-80%
    return (content["Question"].iloc[id], content["Answer"].iloc[id])