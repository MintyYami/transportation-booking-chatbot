import nltk, string, os, random
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)
nltk.download("universal_tagset", quiet=True)

# lemmatise tokens, using tags where possible
def lemmatisation(tokens):
    posmap = {
        'ADJ': 'a',
        'ADV': 'r',
        'NOUN': 'n',
        'VERB': 'v'
    }

    # tag words
    post = nltk.pos_tag(tokens, tagset='universal')

    # lemmatise
    lemmatiser = WordNetLemmatizer()
    lemmaised_tokens = []
    for token in post:
        word, tag = token
        if tag in posmap.keys():
            lemmaised_tokens.append(lemmatiser.lemmatize(word, posmap[tag]))
        else:
            lemmaised_tokens.append(lemmatiser.lemmatize(word))

    return lemmaised_tokens

# tokenise and lemmatise text
def preprocess_text_to_tokens(text):
    # tokenisise
    tokens = word_tokenize(text.lower())

    # remove stopwords and punctuation
    tokens_nsw = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]

    # lemmatise
    if len(tokens_nsw) == 0:
        tokens_preprocessed = lemmatisation(preprocess_small(text))
    else:
        tokens_preprocessed = lemmatisation(tokens_nsw)

    return tokens_preprocessed

# join tokenised text back to string
def preprocess_text(tokens):
    return " ".join(preprocess_text_to_tokens(tokens))

# create document-term matrix with tfidf to compare with input later
def process_question_dataset(file_name, extension):
    if (not os.path.isfile(f"data_processed/{file_name}_preprocess.joblib")):
        # read dataset
        content = pd.read_csv(('data/' + file_name + extension), index_col=False)

        # preprocess question
        content["Question_processed"] = content["Question"].apply(preprocess_text)
        dump(content, ("data_processed/" + file_name + "_preprocess.joblib"))
    content = load("data_processed/" + file_name + "_preprocess.joblib")

    # term weighting (TF-IDF)
    tfidf_vectoriser = TfidfVectorizer(analyzer="word")
    questions_tfidf = tfidf_vectoriser.fit_transform(content["Question_processed"])
    if (not os.path.isfile(f"data_processed/{file_name}_matrix.joblib")):
        QA_matrix = pd.DataFrame(questions_tfidf.toarray(), columns=tfidf_vectoriser.get_feature_names_out())
        dump(QA_matrix, (f"data_processed/{file_name}_matrix.joblib"))
    QA_matrix = load(f"data_processed/{file_name}_matrix.joblib")

    return content, QA_matrix, tfidf_vectoriser

# match input with matrix instance using cosine similarity
def process_query_with_matrix(query, file_name, extension, threshold):
    # get matrix and vectoriser
    content, QA_matrix, tfidf_vectoriser = process_question_dataset(file_name, extension)

    # preprocess query
    query_preprocessed = preprocess_text(query)

    # get cosine similarities
    query_tfidf = tfidf_vectoriser.transform([query_preprocessed]).toarray()[0]
    cos_sim = []
    for i in range(len(QA_matrix)):
        denom = norm(query_tfidf) * norm(QA_matrix.iloc[i])
        if denom != 0:
            cos_sim.append(dot(query_tfidf, QA_matrix.iloc[i]) / denom)
        else:
            cos_sim.append(0)

    # get max cosine
    max_sim_value = max(cos_sim)
    # get randomised
    if (max_sim_value > threshold):
        max_sim_indices = [i for i, value in enumerate(cos_sim) if value == max_sim_value]

        id = max_sim_indices[random.randint(0, len(max_sim_indices) - 1)]

        return id, content, max_sim_value
    return None, content, max_sim_value

# match input with score compared to given list
def process_query_with_list(user_input, list, threshold):
    score = 0
    input_tokens = preprocess_small(user_input)

    if(len(input_tokens) == 0):
        return False

    for token in input_tokens:
        if token in list:
            score += 1
    score /= len(input_tokens)
    return True if score > threshold else False

# small text tokenisation for small user inputs to revent deleting the whole input
def preprocess_small(user_input):
    tokens = word_tokenize(user_input.lower())
    stopwords_small = ["to", "is", "am", "are", "was", "were", "be", "it", "that", "i", "you", "want", "can", "please", "what"]
    tokens_preprocessed = [token for token in tokens if token not in stopwords_small and token not in string.punctuation]
    return tokens_preprocessed