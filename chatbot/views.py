import openai
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from uploadreports.models import Reports
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .serializers import ReportSerializer
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from decouple import config
GeminiKey = config('GeminiKey', cast=str)
genai.configure(api_key=GeminiKey)
from langchain_community.chat_models import ChatOpenAI

from include.DocumentStoreRetriveEmbed import DocumentStore

document_store = DocumentStore()

os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY', cast=str)


def load_user_data(user_id):
    user_dir = os.path.join(settings.MEDIA_ROOT, str(user_id))
    vector_file_path = os.path.join(user_dir, 'embeddings.txt')
    summary_file_path = os.path.join(user_dir, 'summaries.txt')

    embeddings = {}
    summaries = {}

    with open(vector_file_path, 'r') as vector_file:
        for line in vector_file:
            parts = line.strip().split(': ', 1)
            if len(parts) == 2:
                filename, vector_str = parts
                try:
                    vector = np.array([float(x) for x in vector_str.split(',')])
                    embeddings[filename] = vector
                except ValueError:
                    print(f"Error parsing vector for file: {filename}")
            else:
                print(f"Skipping malformed line in embeddings file: {line.strip()}")

    with open(summary_file_path, 'r') as summary_file:
        for line in summary_file:
            parts = line.strip().split(': ', 1)
            if len(parts) == 2:
                filename, summary = parts
                summaries[filename] = summary
            else:
                print(f"Skipping malformed line in summaries file: {line.strip()}")

    return embeddings, summaries


def find_most_relevant_documents(user_id, query, top_k=3):
    embeddings, summaries = load_user_data(user_id)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode(query)

    similarities = []
    for filename, vector in embeddings.items():
        similarity = cosine_similarity([query_vector], [vector])[0][0]
        similarities.append((filename, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    top_documents = similarities[:top_k]

    return [(filename, summaries[filename]) for filename, _ in top_documents]
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        user_message = data.get('message', '')
        question = user_message

        vectorstore = document_store.get_vectorstore(request.user.id)
        retrieved_docs = vectorstore.similarity_search_with_score(question, k=5)
        # Extract context and summary
        context = "\n".join([doc.page_content for doc, _ in retrieved_docs])
        summary = retrieved_docs[0][0].metadata.get('summary', '')  # Get summary from the first retrieved document

        #llm = get_gemini_llm()
        # Combine context and summary
        full_context = f"Summary:\n{summary}\n\nDetailed Context:\n{context}"


        #llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GeminiKey)
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.2)
        prompt_template = """
                You are a medical assistant tasked with answering questions based on OCR-extracted and LLM-formatted medical reports. 
                Use the following information to answer the question. Pay special attention to laboratory results, diagnoses, and any mentions of specific diseases or viruses.

                Information:
                {context}

                Question: {question}

                Provide a concise and accurate answer based on the given information. If the information contains multiple relevant pieces, synthesize them into a coherent answer. Always maintain medical accuracy and relevance. If the answer is clearly stated in the context or summary, quote it directly.

                If asked about a specific condition, test result, or virus, always check both the context and summary for any mentions, even if it's not the primary diagnosis.

                Answer:
                """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": PROMPT}
        )

        result = qa_chain({"query": question, "context": full_context})
        bot_response = result['result']


        return JsonResponse({'message': bot_response})

    return JsonResponse({'error': 'Invalid request method'})

def chat_page(request):
    return render(request, 'chatbot/chat.html')


def chat_partial(request):
    return render(request, 'chatbot/chat_partial.html')