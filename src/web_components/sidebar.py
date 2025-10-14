""" Sidebar Web Component """
import streamlit as st
from commands.get_spaces import GetSpacesCommand
from gateways.object_storage_gateway import ObjectStorageGateway
from web_components.actions import actions

def get_spaces():
    """ Pulls a list of spaces from Object Storage. """
    # pull list of objects from storage
    command = GetSpacesCommand()
    command.go()

    return command.spaces

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
    if st.button("Create New...", type="primary", width="stretch"):
        st.query_params.action = actions.CREATE_EVALUATION

    # Data set header
    st.header("Prior Evaluations")

    # Display available data sets for selection
    spaces = get_spaces()
    if spaces is None or len(spaces) == 0:
        st.write("Empty")
    else:
        index = 0
        for space in spaces:
            index += 1
            if st.button(f"{space.name}", type="tertiary", width="stretch"):
                st.query_params.space_id = space.id
                st.query_params.action = actions.VIEW_EVALUATION
