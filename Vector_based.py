from langchain_community.document_loaders import CSVLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import os
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBngXwICYwR-vYEul1s0_XZFicHEt9paMs"

embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

loader = CSVLoader("banklist.csv", encoding="windows-1252")
documents = loader.load()

db = Chroma.from_documents(documents, embedding_function)
retriever = db.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=1)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print(chain.invoke("What bank failed in North Carolina?"))

