""" View Data Set Content Component """
import logging
import streamlit as st
from commands.load_space import LoadSpacesCommand
from web_components.actions import actions
from web_components.evaluation_tab_summary import view_evaluation_summary
from web_components.evaluation_tab_analysis import view_evaluation_analysis
from web_components.evaluation_tab_automation import view_evaluation_automation
from web_components.evaluation_tab_import import view_evaluation_import
from web_components.evaluation_tab_advanced import view_evaluation_advanced
from web_components.evaluation_tab_heat_maps import view_evaluation_heat_map_by_server, view_evaluation_heat_map_by_issue

logger = logging.getLogger(__name__)

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

    # render page tabs
    summary_tab, import_tab, analysis_tab, heat_map_server_tab, heat_map_issue_tab, automation_tab, advanced_tab = st.tabs( \
            ["Summary",
                "Import Incidents",
                "Incident-Level Analysis",
                "Heat Map by Server",
                "Heat Map by Issue",
                "Automation",
                "Advanced"],
            width="stretch", default=None)

    with summary_tab:
        view_evaluation_summary(space_id, command)

    with import_tab:
        view_evaluation_import(space_id, command)

    with analysis_tab:
        view_evaluation_analysis(space_id, command)

    with heat_map_server_tab:
        view_evaluation_heat_map_by_server(space_id, command)

    with heat_map_issue_tab:
        view_evaluation_heat_map_by_issue(space_id, command)

    with automation_tab:
        view_evaluation_automation(space_id, command)

    with advanced_tab:
        view_evaluation_advanced(space_id, command)
