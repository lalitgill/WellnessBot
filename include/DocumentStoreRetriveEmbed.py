from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings()
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

def get_gemini_llm():
    model = genai.GenerativeModel('gemini-pro')
    generation_config = GenerationConfig(
        temperature=0.3,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
    )

    class GeminiLLM:
        def __call__(self, prompt):
            try:
                response = model.generate_content(prompt, generation_config=generation_config)
                if response.text:
                    return response.text
                else:
                    # If the response is blocked, return a placeholder message
                    return "Unable to process the content due to safety concerns."
            except Exception as e:
                print(f"Error in Gemini LLM: {str(e)}")
                return "An error occurred while processing the content."

    return GeminiLLM()


def format_medical_text(extracted_text):
    llm = get_gemini_llm()
    prompt = f"""
    You are a medical document formatting assistant. Your task is to take the following OCR-extracted text from a medical report and format it into a structured, easy-to-read format. 
    Identify key sections such as Patient Information, Medical History, Diagnosis, Medications, Laboratory Results, and Recommendations. 
    If a section is not present, do not include it. Use appropriate headers and maintain the original information and values.

    Here's the extracted text:

    {extracted_text}

    Please format this text into a structured medical report:
    """

    formatted_text = llm(prompt)
    return formatted_text


def simple_format_medical_text(text):
    # A simple rule-based formatting function
    sections = ["Patient Information", "Medical History", "Diagnosis", "Medications", "Laboratory Results",
                "Recommendations"]
    formatted_text = ""
    current_section = "Other"

    for line in text.split('\n'):
        line = line.strip()
        if any(section.lower() in line.lower() for section in sections):
            current_section = line
            formatted_text += f"\n\n{current_section}:\n"
        else:
            formatted_text += f"{line}\n"

    return formatted_text.strip()

def generate_summary(text):
    llm = get_gemini_llm()
    prompt = f"""
    Summarize the following medical report in a concise manner. Include key patient information, 
    primary diagnosis, significant test results, and main recommendations if present. 
    The summary should be brief but capture the essential medical information:

    {text}

    Summary:
    """

    summary = llm(prompt)
    #formatted_text = llm(prompt)
    if summary == "Unable to process the content due to safety concerns.":
        # If LLM formatting fails, use a simple rule-based formatting
        summary = simple_format_medical_text(text)
    return summary

class DocumentStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.vectorstores = {}
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def get_vectorstore(self, user_id):
        collection_name = f"user_{user_id}_documents"
        if collection_name not in self.vectorstores:
            self.vectorstores[collection_name] = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=self.persist_directory
            )
        return self.vectorstores[collection_name]

    def store_document(self, user_id, filename, extracted_text, metadata):
        vectorstore = self.get_vectorstore(user_id)

        # Format the extracted text
        formatted_text = format_medical_text(extracted_text)
        # Generate a summary
        summary = generate_summary(formatted_text)
        # Update metadata with summary
        metadata['summary'] = summary

        chunks = self.text_splitter.split_text(formatted_text)

        docs = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk": i,
                "total_chunks": len(chunks)
            })
            docs.append(Document(page_content=chunk, metadata=chunk_metadata))

        vectorstore.add_documents(docs)

    def persist_all(self):
        for vectorstore in self.vectorstores.values():
            vectorstore.persist()