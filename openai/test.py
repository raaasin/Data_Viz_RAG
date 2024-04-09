from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import CSVLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from secrects import key
import os

os.environ["OPENAI_API_KEY"] = key
embedding_function = OpenAIEmbeddings()
loader = CSVLoader("./retail_data.csv", encoding="windows-1252")
documents = loader.load()

db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke("What bank failed in North Carolina?"))