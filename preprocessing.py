import pandas as pd
import string
import pymorphy3
import nltk
from nltk.corpus import stopwords

morph = pymorphy3.MorphAnalyzer()
stop_words = set(stopwords.words("russian"))

# загружаем датасет
def load_corpus(path="quok.csv"):
    df = pd.read_csv(path)
    return df["line"].tolist()

#предобработка текстов
def preprocess(text):
    text=text.lower()
    exclude = set(string.punctuation + "«»—")
    text = ''.join(i for i in text if i not in exclude)
    tokens = text.split()
    lemmas = [morph.parse(word)[0].normal_form for word in tokens]
    tokens_clear = [word for word in lemmas if word not in stop_words]

    return tokens_clear


def preprocess_db(documents):
    return [preprocess(doc) for doc in documents]


