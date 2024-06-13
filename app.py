import streamlit as st
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import urllib.parse
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

st.title("💬 PDF Chatbot")


# Load environment variables from .env file
load_dotenv()

#username and password
username = <your username>
password = <your password>
#encoded
username_encoded = urllib.parse.quote_plus(username)
password_encoded = urllib.parse.quote_plus(password)
# Access the OpenAI API key
open_api_key = os.getenv("OPENAI_API_KEY")

#user entering open API key, you can edit the sidebar for your preferences
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    user_email = st.text_input('Enter your Email')
    user_password = st.text_input('Enter your Password', type='password')
    if not os.path.exists("docs"):
        os.makedirs("docs")

    def save_pdf(file):
        save_path = os.path.join("docs", "temp.pdf")
        with open(save_path, "wb") as f:
            f.write(file.getbuffer())
        
        return save_path

    st.title("PDF File Uploader")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        saved_path = save_pdf(uploaded_file)
    
        st.success(f"File saved to {saved_path}")

#Enter openai-api-key
if not openai_api_key or not user_email or not user_password or not uploaded_file:
        st.info("Please add your OpenAI API key, Email, Password, and upload a PDF file to continue.")
        st.stop()
print(openai_api_key)
#user_session = st.text_input('What is your session id?') - storegae and memory of user data
chat_message_history = MongoDBChatMessageHistory(
    session_id = user_email,
    connection_string = f"<your connection string{username_encoded}:{password_encoded}the rest of your connection string>",
    database_name = "<your database name>",
    collection_name = "<your collection name>",
)

#retriever code
#Get the PDF document from the path; then it will load it to the loader variable
loader = PyPDFLoader("docs/temp.pdf")
#Chunking through load_and_split() method; 1024 tokens by default
pages = loader.load_and_split()
#from_document() will return VectorStore initialized from documents and embeddings.
faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(api_key = openai_api_key))
#Default session, check is there is a message field in the session state, if not, then create role and content
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
#assigning the role and writing the content
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
#if statement and whatever the user is asked is the user question
if user_question := st.chat_input():
    #Creating an object to access the class methods
    client = OpenAI(api_key=openai_api_key)
    #get the similar docs based on the question, k = pages to retrieve
    docs = faiss_index.similarity_search(user_question, k=4)
    #importing the prompt template, passing user question (question) and context (similarity seach)
    #you can change your prompt, this is what gave me the best answers
    prompt = PromptTemplate.from_template(
        ("Address the question '{question}' by crafting a response based on the context provided. Please format your answer by: Starting with a concise summary, detailing each relevant aspect in individual, well-punctuated sentences, and ensuring the text is easy to read and understand with appropriate spacing. Finally, conclude with any implications or conclusions that can be drawn from the information:\n\n{context}"))
    #format the prompt
    prompt.format(question = 'question', context = 'context')
    #sent to gpt model - you can change model, 4.0 etc
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    #pass the model and the prompt which will be the parameters to go throught our documents to generate an answer for us
    chain = create_stuff_documents_chain(llm, prompt)
    #input the content and question to an output
    msg = chain.invoke({"context": docs, "question": user_question})
    #session.state is for where the user is pointing at currently
    #add to session_state memory
    st.session_state.messages.append({"role": "user", "content": user_question})
    #write the user question that will come up
    st.chat_message("user").write(user_question)
    #append answer into memory
    st.session_state.messages.append({"role": "assistant", "content": msg})
    #write the answer
    st.chat_message("assistant").write(msg)
    #message history, user and ai
    chat_message_history.add_user_message(user_question)
    chat_message_history.add_ai_message(msg)
