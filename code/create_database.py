#to read text files and convert them into a format the langchain can undertstand
from langchain_community.document_loaders import TextLoader
#to cut long document into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
#to convert text into numbers
from langchain_huggingface import HuggingFaceEmbeddings
#import the chroma vector store
from langchain_chroma import Chroma
#to load the API key from the .env file
from dotenv import load_dotenv
#to handle file paths and directories
import os
import shutil

#set up 
load_dotenv()

CHROMA_PATH = "chroma" #where the vector database will be stored
DATA_PATH = "data/books" 


def main():
    generate_data_store()

#3 steps in order: Load the documents, split them into chunks and save to the database
def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

#loading the documents 
def load_documents():
    #check if the folder exists
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data folder not found: {DATA_PATH}")

    documents = []
    #loop through every file in the folder
    for file in os.listdir(DATA_PATH):
        #only pick the .md files 
        if file.endswith(".md"):
            file_path = os.path.join(DATA_PATH, file)
            print(f"Loading: {file_path}")
            #read each file and convert it to a Langchain doecument
            loader = TextLoader(file_path, encoding="utf-8")
            #add them to the list 
            documents.extend(loader.load())

    if not documents:
        raise ValueError(f"No .md files found in {DATA_PATH}")

    return documents

#splitting text 
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(

        #Overlap to ensure the AI always has enough context.
        chunk_size=300, #each chunk is max 300 characters
        chunk_overlap=100, #chunks share 100 characters with the next chunk so context isn't lost at the edges
        length_function=len, #use character count to measure size
        add_start_index=True, #save the position of each chunk in the original document
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    if len(chunks) > 10:
        document = chunks[10]
        print(document.page_content)
        print(document.metadata)

    return chunks

#Saving to Chroma
def save_to_chroma(chunks: list[Document]):
    #delete old database to start fresh
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    #convert each chunk into a vector
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma.from_documents( #save all the vectors into the Chroma database on disk
        chunks, embedding, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()