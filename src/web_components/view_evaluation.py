""" View Data Set Content Component """
import logging
import streamlit as st
from commands.load_space import LoadSpacesCommand

logger = logging.getLogger(__name__)

def delete_evaluation(space_id):
    """ Delete the specified evaluation. 
    
        space_id - uuid of evaluation to delete
    """
    st.success("Deleted evaluation")

def import_incidents(space_id):
    """ Imports data.
    
        space_id - space id
    """

def run_analysis(space_id):
    """ Runs AI Analysis against uploaded data set.
    
        space_id - space id
    """

def view_evaluation():
    # get evaluation id
    space_id = st.query_params.space_id

    # load space
    command = LoadSpacesCommand()
    command.space_id = space_id
    command.go()
    metadata = command.metadata

    # page header
    st.title(f"Evaluation '{metadata.name}'")
    st.write(metadata.description)

    # actions list
    col1, col2, col3 = st.columns([0.33, 0.33, 0.34])
    with col1:
        if st.button("Run Analysis", type="primary"):
            run_analysis(space_id)
    with col2:
        if st.button("Import Incidents", type="primary"):
            import_incidents(space_id)
    with col3:
        if st.button("Delete Evaluation", type="primary"):
            delete_evaluation(space_id)
