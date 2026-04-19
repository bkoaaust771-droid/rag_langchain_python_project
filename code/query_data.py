#to accept input from the terminal
import argparse
#to load the secret API keys from the .env file 
from dotenv import load_dotenv
#the same Chroma database built in create_database.py now opening it to search it.
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
#to use the Groq LLM to answer questions based on the retrieved context
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

#set up
load_dotenv()

CHROMA_PATH = "chroma"


#Prompt Template
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context} 

---

Question: {question}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str)
    args = parser.parse_args()


    #Open the Chroma database from disk and use the same embedding model as before (very important to
    #use the same model to search as the one used to store, otherwise the vectors won't match)
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

    #Search the database for the 3 most similar chunks
    results = db.similarity_search_with_relevance_scores(args.query_text, k=3)

    #quality Check
    if len(results) == 0 or results[0][1] < 0.3:
        print("No good match found.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    #build the Prompt
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context_text,
        question=args.query_text
    )

    #invoke the Groq LLM with the prompt and get the response
    model = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
    )
    response = model.invoke(prompt)

    
    #printing the results
    sources = [doc.metadata.get("source", None) for doc, _ in results]

    print(f"\nResponse:\n{response.content}")
    print(f"\nSources:")
    for source in set(sources):
        print(f"  - {source}")

if __name__ == "__main__":
    main()