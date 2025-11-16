import streamlit as st
from web_components.actions import actions
from gateways.object_storage_gateway import ObjectStorageGateway

def view_evaluation_advanced(space_id, command):

    gateway = ObjectStorageGateway()

    # delete evaluation button
    if st.button("Delete Evaluation", type="primary"):
        gateway.delete_root_dir(space_id)
        st.query_params.action = actions.HOME
        st.rerun()
