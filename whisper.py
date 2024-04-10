import assemblyai as aai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import os
import sys
import datetime
aai.settings.api_key = "4822f34dd0bb40e9a1be096507478a73"

# URL of the file to transcribe
FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"


def save_audio_file(audio_bytes, file_extension):

    file_name = f"audio.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name

audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    save_audio_file(audio_bytes, "mp3")
    FILE_URL = "audio.mp3"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    
    if transcript.status == aai.TranscriptStatus.error:
        print(st.text("I couldn't Hear you :("))
    else:
        print(st.text_area(transcript.text))
