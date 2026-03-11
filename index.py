from whoosh.filedb.filestore import RamStorage
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.scoring import Frequency, BM25F


def build_index(documents, documents_processed):
    schema = Schema(
        doc_id=ID(stored=True),
        content=TEXT(stored=True),
        content_processed=TEXT(stored=True)
    )

    storage = RamStorage()
    ix = storage.create_index(schema)
    writer = ix.writer()

    for i, (text, processed_tokens) in enumerate(zip(documents, documents_processed)):
        processed_text = " ".join(processed_tokens)

        writer.add_document(
            doc_id=str(i),
            content=text,
            content_processed=processed_text
        )

    writer.commit()

    return ix


def search_frequency(user_text, ix):
    results = []

    with ix.searcher(weighting=Frequency()) as searcher:
        parser = QueryParser("content_processed", ix.schema)
        query = parser.parse(user_text)
        result = searcher.search(query, limit=5)

        for i in result:
            results.append(
                (int(i["doc_id"]), i.score, i["content"])
            )

    return results


def search_bm25(user_text, ix):
    results = []

    with ix.searcher(weighting=BM25F()) as searcher:
        parser = QueryParser("content_processed", ix.schema)
        query = parser.parse(user_text)
        result = searcher.search(query, limit=5)

        for i in result:
            results.append(
                (int(i["doc_id"]), i.score, i["content"])
            )

    return results