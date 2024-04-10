import streamlit as st
import pandas as pd
import json
from agent import query_agent, create_agent
# Import libraries for audio recording and saving
import sounddevice as sd
from scipy.io.wavfile import write

# Flag to track recording state
is_recording = False


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

def record_audio():
  """Records audio from microphone based on recording state flag."""
  global is_recording, fs
  if not is_recording:
    try:
      # Sample rate and number of channels
      fs = 44100
      channels = 2
      print("Recording...")
      with sd.InputStream(samplerate=fs, channels=channels):
        while is_recording:
          sd.sleep(100)  # Adjust sleep time for responsiveness (milliseconds)
      print("Recording stopped!")
    except Exception as e:
      st.error(f"Error recording audio: {e}")

st.title("Databot")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")

record_button = st.button("Record Audio", type="primary")

if st.button("Submit Query", type="primary"):
    agent = create_agent(data)
    response = query_agent(agent=agent, query=query)
    decoded_response = decode_response(response)
    write_response(decoded_response)

if record_button:
  is_recording = not is_recording  # Toggle recording state on button click
  if not is_recording:
    recording = sd.get_stopped_data()  # Access recorded data after stopping
    # Save recording as mp3 file (if any data captured)
    if recording is not None:
      filename = "recording.mp3"
      write(filename, fs, recording)
      st.success(f"Audio recording saved as {filename}")