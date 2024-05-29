!pip install langchain_openai
!pip install pypdf
!pip install langchain
!pip install faiss-cpu

%env OPENAI_API_KEY=sk-proj-w3zdbtQ4zBDNjkcno474T3BlbkFJpIefe0DwAYft2Dc01ZuT

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

loader = PyPDFLoader("/content/Syllabus_example.pdf")
pages = loader.load_and_split()
pages[3]

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
docs = faiss_index.similarity_search("What is the Professional Draft?", k=4)
print(docs)
