""" View Data Set Content Component """
import logging
import streamlit as st
from commands.load_space import LoadSpacesCommand
from web_components.actions import actions
from web_components.import_data_set import import_data_set

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
    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
    with col1:
        if st.button("View Evaluation", type="primary"):
            st.query_params.space_id = metadata.id
            st.query_params.subaction = actions.view_subactions.HOME
            st.query_params.action = actions.VIEW_EVALUATION
    with col2:
        if st.button("Run Analysis", type="primary"):
            run_analysis(space_id)
    with col3:
        if st.button("Import Incidents", type="primary"):
            st.query_params.space_id = metadata.id
            st.query_params.subaction = actions.view_subactions.IMPORT
            st.query_params.action = actions.VIEW_EVALUATION
    with col4:
        if st.button("Delete Evaluation", type="primary"):
            delete_evaluation(space_id)

    # render rest of page
    if "subaction" in st.query_params and st.query_params.subaction == actions.view_subactions.IMPORT:
        import_data_set()
    else:
        # default content
        st.write("Default Content")
