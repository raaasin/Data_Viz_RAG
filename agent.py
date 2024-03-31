from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os 
import warnings
warnings.filterwarnings("ignore")
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBngXwICYwR-vYEul1s0_XZFicHEt9paMs"
def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).
    Args:
        filename: The path to the CSV file that contains the data.
    Returns:
        An agent that can access and use the LLM.
    """
    # Create an Gemini object.
    llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)
    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)
def query_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = (
        """
        For the following query, if it requires drawing a table, reply as follows:
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
        + query
    )


    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    print(response.__str__() + "\n")
    return response.__str__()
