from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os 
import warnings
from langchain.agents.agent_types import AgentType
from prompt import promp
warnings.filterwarnings("ignore")
from secret import apikey
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = apikey
def create_agent(filename: str):
    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.2)

    df = pd.read_csv(filename)

    return create_pandas_dataframe_agent(llm, df, verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

def query_agent(agent, query):
    prompt = (promp+ query)
    response = agent.run(prompt)
    print(response.__str__() + "\n")
    return response.__str__()
