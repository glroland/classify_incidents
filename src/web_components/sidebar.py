""" Sidebar Web Component """
import streamlit as st
from gateways.object_storage_gateway import ObjectStorageGateway
from web_components.actions import actions

def get_data_sets():
    """ Pulls a list of datasets from Object Storage. """
    # pull list of objects from storage
    gateway = ObjectStorageGateway()
    list_of_files = gateway.list()

    return list_of_files

def sidebar():
    """ Dynamically render sidebar. """

    st.markdown(
                """
                <style>
                [data-testid=stSidebar] {
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

    # display title logo
    st.markdown(
        '<a href="." target="_self"><img src="/app/static/title.png" alt="HTML image" style="max-width: 100%;"></a>',
        unsafe_allow_html=True
    )

    # Create new data set button
    if st.button("Import New Data Set", type="primary", width="stretch"):
        st.query_params.action = actions.CREATE_DATA_SET

    # Data set header
    st.header("Data Sets")

    # Display available data sets for selection
    dataset_list = get_data_sets()
    if dataset_list is None or len(dataset_list) == 0:
        st.write("Empty")
    else:
        index = 0
        for dataset in dataset_list:
            index += 1
            if st.button(f"{index}.) {dataset}", type="tertiary"):
                st.query_params.dataset = dataset
                st.query_params.action = actions.VIEW_DATA_SET
