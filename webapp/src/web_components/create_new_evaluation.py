""" Create Data Set Content Component """
from datetime import datetime
import streamlit as st
from commands.create_space import CreateSpaceCommand
from web_components.actions import actions

def create_new():
    st.header("Create New Evaluation")

    # evaluation name
    now = datetime.today()
    now_str = now.strftime("%m-%d-%Y @ %I:%M:%S %p")
    st.session_state.setdefault("eval_name_input", now_str)
    eval_name_input = st.text_input("Name of evaluation space:",
                                    value=st.session_state["eval_name_input"],
                                    max_chars=25,
                                    width=400)
    if eval_name_input != st.session_state["eval_name_input"]:
        st.session_state["eval_name_input"] = eval_name_input

    # evaluation description
    eval_desc_input = st.text_input("(Optional) Description:", "", max_chars=25, width=400)

    # submit button
    if st.button("Create", type="primary"):
        name = st.session_state["eval_name_input"]
        if name is None or len(name) == 0:
            st.error("Name is a required field and cannot be empty!")
        else:
            st.success("Inputs validated.  Creating space...")

            # create the space
            command = CreateSpaceCommand()
            command.name = name
            command.description = eval_desc_input
            command.go()

            # clear session state
            del st.session_state.eval_name_input

            st.success("Evaluation space created!")

            # redirect to view the space that was just created
            st.query_params.space_id = command.id
            st.query_params.subaction = actions.view_subactions.HOME
            st.query_params.action = actions.VIEW_EVALUATION
            st.rerun()
