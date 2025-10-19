import streamlit as st
from web_components.actions import actions
from gateways.object_storage_gateway import ObjectStorageGateway

def view_evaluation_summary(space_id, command):
    metadata = command.metadata

    gateway = ObjectStorageGateway()

    st.header("Summary")

    # actions list
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        if st.button("Import Incidents", type="primary", key="summary_import_btn"):
            st.query_params.space_id = metadata.id
            st.query_params.subaction = actions.view_subactions.IMPORT
            st.query_params.action = actions.VIEW_EVALUATION
            st.rerun()
    with col2:
        if st.button("Delete Evaluation", type="primary"):
            gateway.delete_root_dir(space_id)
            st.query_params.action = actions.HOME
            st.rerun()
