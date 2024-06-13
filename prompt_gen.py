from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
#if statement and whatever the user is asked is the user question
if user_question := st.chat_input():
    #Creating an object to access the class methods
    client = OpenAI(api_key=openai_api_key)
    #get the similar docs based on the question, k = pages to retrieve
    docs = faiss_index.similarity_search(user_question, k=4)
    #importing the prompt template, passing user question (question) and context (similarity seach)
    prompt = PromptTemplate.from_template(
        ("Address the question '{question}' by crafting a response based on the context provided. Please format your answer by: Starting with a concise summary, detailing each relevant aspect in individual, well-punctuated sentences, and ensuring the text is easy to read and understand with appropriate spacing. Finally, conclude with any implications or conclusions that can be drawn from the information:\n\n{context}"))
    #format the prompt
    prompt.format(question = 'question', context = 'context')
    #sent to gpt model - can shange to gpt-4.0-turbo and other models
    #price will increase if model quality is increased
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
