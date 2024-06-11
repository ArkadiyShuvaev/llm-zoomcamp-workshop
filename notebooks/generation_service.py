from typing import List
from retrieval_result import RetrievalResult
import json


class GenerationService:

    def get_answer(self, prompt: str, bedrock_runtime) -> str:
        model = "amazon.titan-text-express-v1"
        
        kwargs = {
            "modelId": model,
            "contentType": "application/json",
            "accept": "*/*",
            "body": json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 500,
                        "stopSequences": [],
                        "temperature": 0.9,
                        "topP": 0.9,
                    },
                }
            ),
        }

        response = bedrock_runtime.invoke_model(**kwargs)
        body_as_plain_text = response.get('body').read()
        response_body = json.loads(body_as_plain_text)

        return response_body["results"][0]["outputText"]

    def create_prompt(self, user_question: str, context: str) -> str:
        return (
            "You are a course teaching assistant. "
            "Read the question first inside <question></question> XML tags. "
            "Then answer the user question based on the given context inside <context></context> XML tags. "
            "The answer is retrieved from the internal FAQ database. "
            "The answers from the internal database always have highest priority. "
            "Try to paraphrase the answer to get it more clear. "
            "If you cannot give the answer, answer 'I cannot answer this question.'. "
            "The context is a collection of items each of them has following properties: "
            "'Answer', 'Question', 'Section' and 'Score'. "
            "The higher the 'Scope', the more relevant the 'Answer' is."
            f"<question>{user_question}</question>. <context>{context}</context>.".strip()
        )

    def create_context(self, documents: List[RetrievalResult]) -> str:
        concatenated_results = ""
        for doc in documents:
            concatenated_results += str(doc)

        stripped = concatenated_results.strip()
        return stripped
