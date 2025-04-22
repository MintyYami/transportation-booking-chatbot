import os
import pandas as pd
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import resample
from sklearn.naive_bayes import MultinomialNB

# load training data from directory 'label_dir', using each sub-folder as label for each data
def loadData(label_dir):
    data = []
    labels = []

    for label in label_dir.keys():
        for sub_dir in label_dir[label]:
            for file in os.listdir(sub_dir):
                filepath = sub_dir + os.sep + file
                with open(filepath, encoding='utf8', errors='ignore', mode='r') as review:
                    content = review.read()
                    data.append(content)
                    labels.append(label)

    return data, labels

# stemmer for CountVectorizer
def stemmed_words(doc):
    from nltk.stem.snowball import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer
    from nltk.corpus import stopwords

    p_stemmer = PorterStemmer()
    analyzer = CountVectorizer(stop_words=stopwords.words("english"), ngram_range=(1, 2)).build_analyzer()
    return (p_stemmer.stem(word.lower()) for word in analyzer(doc.lower()))

# load or create classifier or data in directory 'label_dir'
def get_classifier(classifier_name, label_dir):
    if not (os.path.isfile(f"classifier/{classifier_name}_classifier.joblib") or
                os.path.isfile(f"classifier/{classifier_name}_transformer.joblib")):
        # get data to train
        data, labels = loadData(label_dir)

        # bootstrap to get more data (sample size = 50%)
        data_sample, label_sample = resample(data, labels, n_samples=int(len(data) * 0.50), random_state=1)

        # text preprocessing and vectorisation
        vectoriser = TfidfVectorizer(analyzer=stemmed_words)
        data_tfidf = vectoriser.fit_transform(data+data_sample)

        # create classifier
        classifier = MultinomialNB().fit(data_tfidf, labels+label_sample)


        # dump classifier, countVectorizer and transformer
        dump(classifier, f"classifier/{classifier_name}_classifier.joblib")
        dump(vectoriser, f"classifier/{classifier_name}_transformer.joblib")
    # load classifier, countVectorizer and transformer
    classifier = load(f"classifier/{classifier_name}_classifier.joblib")
    vectoriser = load(f"classifier/{classifier_name}_transformer.joblib")

    return classifier, vectoriser

# use a classifier and data from directory 'label_dir' to label new user input
def input_check_classifier(user_input, classifier_name, label_dir):
    classifier, vectoriser = get_classifier(classifier_name, label_dir)

    data_tfidf = vectoriser.transform([user_input])

    pred = classifier.predict(data_tfidf)[0]
    confidence = classifier.predict_proba(data_tfidf)[0, 0] if pred == "negative" else classifier.predict_proba(data_tfidf)[0, 1]

    return classifier.predict(data_tfidf), confidence