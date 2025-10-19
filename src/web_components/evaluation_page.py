""" View Data Set Content Component """
import logging
import streamlit as st
from commands.load_space import LoadSpacesCommand
from web_components.actions import actions
from web_components.import_data_set import import_data_set
from web_components.evaluation_tab_summary import view_evaluation_summary
from web_components.evaluation_tab_analysis import view_evaluation_analysis
from web_components.evaluation_tab_rawdata import view_evaluation_raw_data
from web_components.evaluation_tab_automation import view_evaluation_automation
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

def import_incidents(space_id):
    """ Imports data.
    
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

    # render page
    if "subaction" in st.query_params and st.query_params.subaction == actions.view_subactions.IMPORT:
        import_data_set(space_id)
    else:
        # default content
        summary_tab, drill_down_tab, raw_data_tab, automation_tab = st.tabs( \
            ["Summary", "Drill Down", "Raw Data", "Automation"], \
                width="stretch", default=None)

        with summary_tab:
            view_evaluation_summary(space_id, command)

        with drill_down_tab:
            view_evaluation_analysis(space_id, command)

        with raw_data_tab:
            view_evaluation_raw_data(space_id, command)

        with automation_tab:
            view_evaluation_automation(space_id, command)

