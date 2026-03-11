from collections import Counter
import math

# частотный индекс через словари
def inverted_index_frequency(documents_processed):
    index = {}

    for doc_id, doc in enumerate(documents_processed):
        counts = Counter(doc)

        for word, tf in counts.items():
            if word not in index:
                index[word] = {}

            index[word][doc_id] = tf

    return index


def calculate_df(frequency_index):
    return {word: len(index) for word, index in frequency_index.items()}


def calculate_idf(df, doc_n):
    idf = {}
    for word, doc_freq in df.items():
        idf[word] = math.log((doc_n - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

    return idf

# BM25 через словари
def inverted_index_bm25(documents_processed):
    index = inverted_index_frequency(documents_processed)
    doc_len = {doc_id: len(doc) for doc_id, doc in enumerate(documents_processed)}
    avgdl = sum(doc_len.values()) / len(doc_len)
    doc_n = len(documents_processed)
    df = calculate_df(index)
    idf = calculate_idf(df, doc_n)

    return {
        "index": index,
        "doc_length": doc_len,
        "avgdl": avgdl,
        "df": df,
        "idf": idf
    }