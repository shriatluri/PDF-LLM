!pip install -U langchain langchain-community

from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
#make variable
question = input('What is your question? ')
#pass variable
docs = faiss_index.similarity_search(question, k=3)
#pass variable
prompt = PromptTemplate.from_template(
    #change the second parameter; format of answer in prompt
    ("Address the question '{question}' by crafting a response based on the context provided. Please format your answer by: Starting with a concise summary, detailing each relevant aspect in individual, well-punctuated sentences, and ensuring the text is easy to read and understand with appropriate spacing. Finally, conclude with any implications or conclusions that can be drawn from the information:\n\n{context}")
)
prompt.format(question = 'question', context = 'context')
llm = ChatOpenAI(model="gpt-3.5-turbo")
chain = create_stuff_documents_chain(llm, prompt)


chain.invoke({"context": docs, "question": question})
