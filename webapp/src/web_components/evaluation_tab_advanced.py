import streamlit as st
import pandas as pd
from io import StringIO
from web_components.actions import actions
from gateways.object_storage_gateway import ObjectStorageGateway

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

def view_evaluation_advanced(space_id, command):

    gateway = ObjectStorageGateway()

    st.header("Purge Data Set")

    # delete evaluation button
    if st.button("Delete Evaluation", type="primary"):
        gateway.delete_root_dir(space_id)
        st.query_params.action = actions.HOME
        st.rerun()

    metadata = command.metadata
    raw_data_files = command.raw_data_files

    st.header("View Raw Incident Data")

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
                    full_path = row["Path"] + "/" + row["Filename"]
                    st.write(f"Deleting file: {full_path}")
                    gateway.delete(full_path)
                    st.write("File deleted...")
                st.success("Files deleted!  Please refresh page.")
