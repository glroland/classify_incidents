""" View Data Set Content Component """
import logging
import streamlit as st
import pandas as pd
from io import StringIO
from commands.load_space import LoadSpacesCommand
from commands.from_space import FromSpaceCommand
from web_components.actions import actions
from web_components.import_data_set import import_data_set
from gateways.object_storage_gateway import ObjectStorageGateway

logger = logging.getLogger(__name__)

def import_incidents(space_id):
    """ Imports data.
    
        space_id - space id
    """

def run_analysis(space_id):
    """ Runs AI Analysis against uploaded data set.
    
        space_id - space id
    """
    command = FromSpaceCommand()
    command.space_id = space_id
    command.go()
    st.success("Analysis Complete!")

@st.dialog("View raw data file", width="large", on_dismiss="ignore", dismissible=True)
def view_raw_data_file(gateway, filename):
    # download file
    contents = gateway.download(filename)

    # special handling for csvs
    if filename.lower().endswith(".csv"):
        # create dataframe for file contents
        contents_s = StringIO(contents)
        df = pd.read_csv(contents_s)

        st.dataframe(data=df)
    else:
        # raw text
        st.code(contents, language=None)

def view_evaluation():
    # get evaluation id
    space_id = st.query_params.space_id

    # load space
    command = LoadSpacesCommand()
    command.space_id = space_id
    command.go()
    metadata = command.metadata
    raw_data_files = command.raw_data_files

    # page header
    st.title(f"Evaluation '{metadata.name}'")
    st.write(metadata.description)

    gateway = ObjectStorageGateway()

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
            st.rerun()
    with col4:
        if st.button("Delete Evaluation", type="primary"):
            gateway.delete_root_dir(space_id)
            st.query_params.action = actions.HOME
            st.rerun()

    # render rest of page
    if "subaction" in st.query_params and st.query_params.subaction == actions.view_subactions.IMPORT:
        import_data_set(space_id)
    else:
        # default content
        summary_tab, drill_down_tab, raw_data_tab, automation_tab = st.tabs( \
            ["Summary", "Drill Down", "Raw Data", "Automation"], \
                width="stretch", default=None)

        with summary_tab:
            st.header("Summary")
        with drill_down_tab:
            st.header("Drill Down into Findings")
        with raw_data_tab:
            st.header("View Uploaded Incident Data Sets")
            if len(raw_data_files) == 0:
                st.write("No files...")
            else:
                filenames = []
                paths = []
                selected = []
                for data_file in raw_data_files:
                    filenames.append(data_file.filename)
                    paths.append(data_file.path)
                    selected.append(False)
                raw_file_list = {
                    "Filename": filenames,
                    "Path": paths,
                    "Selected": selected,
                }
                df = pd.DataFrame(raw_file_list)

                # Display the editable table with checkboxes
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "Selected": st.column_config.CheckboxColumn(
                            "Select Items",
                            help="Select items to view or delete",
                            default=False,
                        )
                    },
                    hide_index=True
                )
                selected_items = edited_df[edited_df['Selected']]
                no_items_selected = len(selected_items) == 0
                one_item_not_selected = len(selected_items) != 1

                col1, col2 = st.columns([0.2, 0.8])

                # View Button
                with col1:
                    if st.button("View File", type="secondary", disabled=one_item_not_selected):
                        for index, row in selected_items.iterrows():
                            view_raw_data_file(gateway, row["Path"] + "/" + row["Filename"])

                # Delete Button
                with col2:
                    if st.button("Delete Files", type="secondary", disabled=no_items_selected):
                        for index, row in selected_items.iterrows():
                            st.write(f"Deleting file: {row["Full Path"]}")
                            gateway.delete(row["Path"] + "/" + row["Filename"])
                            st.write("File deleted...")
                        st.success("Files deleted!  Please refresh page.")

        with automation_tab:
            st.header("Recommended Automation")
