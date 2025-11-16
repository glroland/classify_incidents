import streamlit as st
from commands.from_space import FromSpaceCommand
from utils.space_metadata import load_metadata

def run_analysis(space_id):
    """ Runs AI Analysis against uploaded data set.
    
        space_id - space id
    """
    command = FromSpaceCommand()
    command.space_id = space_id
    command.go()
    st.success("Analysis Complete!")

def view_evaluation_analysis(space_id, command):
    analysis_df = command.analysis_df
    metadata = load_metadata(space_id)

    last_analysis_from = ""
    if metadata.last_analysis_date is not None:
        last_analysis_from = f" from {metadata.last_analysis_date.strftime("%m-%d-%Y at %-I:%M %p")}"
        
    st.header(f"AI Analysis Results{last_analysis_from}")

    # actions list
    if st.button("(Re-) Run Analysis", type="primary"):
        run_analysis(space_id)

    if analysis_df is None:
        st.write("Please click the 'Run Analysis' button to view analysis findings here.")
    else:
        st.dataframe(data=analysis_df, hide_index=True,
                        column_config={
                        "Incident_File": None,
                        "Row": None
                    })
