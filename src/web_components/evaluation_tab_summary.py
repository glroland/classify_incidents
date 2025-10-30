import streamlit as st
from utils.space_metadata import load_metadata

def view_evaluation_summary(space_id, command):
    st.header("Summary")

    # load the space metadata file
    metadata = load_metadata(space_id)
    st.write(metadata.summary)
