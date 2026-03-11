from preprocessing import load_corpus, preprocess, preprocess_db
from index import build_index, search_frequency, search_bm25


def run_search(query, index_type):
    documents = load_corpus()
    documents_processed = preprocess_db(documents)
    query_tokens = preprocess(query)
    query_processed = " ".join(query_tokens)
    ix = build_index(documents, documents_processed)

    if index_type == "frequency":
        results = search_frequency(query_processed, ix)

    elif index_type == "bm25":
        results = search_bm25(query_processed, ix)

    else:
        raise ValueError("Неправильный тип поиска")

    return results


if __name__ == "__main__":
    query = input("Введите поисковый запрос: ").strip()
    index_type = input("Выберите тип поиска (frequency / bm25): ").strip().lower()

    results = run_search(query, index_type)

    print("\nРезультаты поиска:\n")
    for doc_id, score, text in results:
        print(f'{text}\n')
