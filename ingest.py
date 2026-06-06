from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import warnings
import os
import sys
warnings.filterwarnings("ignore")

studies_folder = "studies"
pdf_files = [f for f in os.listdir(studies_folder) if f.endswith('.pdf')]

if not pdf_files:
    print("No PDFs found in studies folder.")
    sys.exit()

print(f"Found {len(pdf_files)} PDF(s): {', '.join(pdf_files)}\n")

all_chunks = []
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for filename in pdf_files:
    path = os.path.join(studies_folder, filename)
    print(f"Loading {filename}...")
    loader = PyPDFLoader(path)
    documents = loader.load()
    chunks = splitter.split_documents(documents)
    print(f"  → {len(documents)} pages, {len(chunks)} chunks")
    all_chunks.extend(chunks)

print(f"\nTotal chunks: {len(all_chunks)}")
print("Storing in database...")

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(all_chunks, embeddings, persist_directory="./db")
print("Done! Database ready.")

