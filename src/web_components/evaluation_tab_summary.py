import streamlit as st
from utils.space_metadata import load_metadata

def view_evaluation_summary(space_id, command):
    st.header("Summary")

    # load the space metadata file
    metadata = load_metadata(space_id)

    # display instructions if analysis has not yet occurred
    if metadata.summary is None or len(metadata.summary) == 0:
        st.write("After creating a space, import incident data and then run analysis using the other tabs.")
    else:
        st.write(metadata.summary)
