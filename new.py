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

print(chain.invoke("""
        For the following query, if it requires drawing a table, reply as follows:
                  The Data column can only have numerical value
        {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}} 

        If the query requires creating a bar chart, reply as follows:
        {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}
        
        If the query requires creating a line chart, reply as follows:
        {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}

        If the query requires creating a scatter plot, reply as follows:
        {"scatter": {"columns": ["X", "Y"], "data": [[x1, y1], [x2, y2], ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}

        There can only be three types of charts: "bar", "line", and "scatter".

        If the query is asking a question that requires neither chart nor calculation, reply as follows:
        {"answer": "answer"}
        Example:
        {"answer": "The title with the highest rating is 'Gilead'"}

        If the query is asking for some calculation or reasoning, provide the answer along with the proof and description.
        Example:
        {"answer": "The sum of the numbers is 10. Here's how it was calculated: 1 + 2 + 3 + 4 = 10"}

        If you do not know the answer, reply as follows:
        {"answer": "I do not know."}

        Return all output as a string.

        All strings in "columns" list and data list should be in double quotes,

        For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

        Let's think step by step.

        Below is the query.
        Query: 
        """
        + "make some sort of bar chart from bank data"))
