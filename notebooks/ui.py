import boto3
import streamlit as st
from generation_service import GenerationService
from retrieval_service import RetrievalService
from elasticsearch import Elasticsearch

session = boto3.Session(profile_name="private")
bedrock_runtime = session.client("bedrock-runtime", region_name="eu-central-1")
ELASTIC_SEARCH_URL = "http://elasticsearch:9200"
SEARCH_FILTER_TERM = "data-engineering-zoomcamp"
INDEX_NAME = "course-questions"

# Initialize services
retrieval_service = RetrievalService()
es = Elasticsearch(ELASTIC_SEARCH_URL)
retrieval_service = RetrievalService()
generation_service = GenerationService()

# Create a list to store history of questions and answers
if "history" not in st.session_state:
    st.session_state.history = []

# Create a text input for user question
user_question = st.text_input("Enter your question:")

if st.button('Generate Answer'):
    # Generate answer
    retrieval_result = retrieval_service.get_retrival_result(user_question, SEARCH_FILTER_TERM, INDEX_NAME, es)
    context = generation_service.create_context(retrieval_result)
    prompt = generation_service.create_prompt(user_question, context)
    answer = generation_service.get_answer(prompt, bedrock_runtime)

    # Display the answer
    st.text_area("Answer:", value=answer, height=200)

    # Add the question and answer to the history
    st.session_state.history.append((user_question, answer))

# Display the history of questions and answers
st.subheader("History")
for i, (question, answer) in enumerate(st.session_state.history):
    st.text(f"Q{i+1}: {question}")
    st.text_area(f"A{i+1}:", value=answer, height=100)
