import streamlit as st
import pandas as pd
import json
import assemblyai as aai
from agent import query_agent, create_agent

def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list


def decode_response(response: str) -> dict:
    return json.loads(response)


def write_response(response_dict: dict):
    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.bar_chart(df.set_index("Area"))  # Set "Area" column as index for bar chart
        if "facts" in data:
            st.write("Interesting Fact: " + data["facts"][0])

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.line_chart(df.set_index("Area"))  # Set "Area" column as index for line chart
        if "facts" in data:
            st.write("Interesting Fact: " + data["facts"][0])

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
        if "facts" in data:
            st.write("Interesting Fact: " + data["facts"][0])

    # Check if the response is a scatter plot.
    if "scatter" in response_dict:
        data = response_dict["scatter"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.scatter_chart(df)
        if "facts" in data:
            st.write("Interesting Fact: " + data["facts"][0])

st.title("Databot")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    agent = create_agent(data)
    response = query_agent(agent=agent, query=query)
    decoded_response = decode_response(response)
    write_response(decoded_response)
