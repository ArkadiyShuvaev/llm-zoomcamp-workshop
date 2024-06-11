from typing import List
from retrieval_result import RetrievalResult
from elasticsearch import Elasticsearch


class RetrievalService:

    def get_retrival_result(
        self,
        user_question: str,
        search_filter_term: str,
        index_name: str,
        es: Elasticsearch
    ):

        search_query = {
            "size": 5,
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": user_question,
                            "fields": ["question^3", "text", "section"],
                            "type": "best_fields",
                        }
                    },
                    "filter": {"term": {"course": search_filter_term}},
                }
            },
        }

        response = es.search(index=index_name, body=search_query)

        result: List[RetrievalResult] = []
        for hit in response["hits"]["hits"]:
            doc = hit["_source"]
            retrieval_result = RetrievalResult(
                hit["_score"], doc["section"], doc["course"], doc["question"], doc["text"]
            )

            result.append(retrieval_result)
        
        return result
