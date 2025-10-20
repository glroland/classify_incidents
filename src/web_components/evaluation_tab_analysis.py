import streamlit as st
import pandas as pd
from io import StringIO
from commands.from_space import FromSpaceCommand
from gateways.object_storage_gateway import ObjectStorageGateway

def run_analysis(space_id):
    """ Runs AI Analysis against uploaded data set.
    
        space_id - space id
    """
    command = FromSpaceCommand()
    command.space_id = space_id
    command.go()
    st.success("Analysis Complete!")

def view_evaluation_analysis(space_id, command):
    analysis = command.analysis

    gateway = ObjectStorageGateway()

    st.header("AI Analysis Results from ______")

    # actions list
    if st.button("(Re-) Run Analysis", type="primary"):
        run_analysis(space_id)

    if analysis is None:
        st.write("Please click the 'Run Analysis' button to view analysis findings here.")
    else:
        analysis_csv = gateway.download(analysis)
        analysis_csv_s = StringIO(analysis_csv)
        df = pd.read_csv(analysis_csv_s)
        st.dataframe(data=df, hide_index=True,
                        column_config={
                        "Incident_File": None,
                        "Row": None
                    })
