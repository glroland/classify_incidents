""" Create Data Set Content Component """
from datetime import datetime
import streamlit as st
from commands.create_space import CreateSpaceCommand

def create_new():
    st.header("Create New Evaluation")

    # evaluation name
    now = datetime.today()
    now_str = now.strftime("%m-%d-%Y @ %I:%M:%S %p")
    eval_name_input = st.text_input("Name of evaluation space:", now_str, max_chars=25, width=400)

    # evaluation description
    eval_desc_input = st.text_input("(Optional) Description:", "", max_chars=25, width=400)

    # submit button
    if st.button("Create", type="primary"):
        if eval_name_input is None or len(eval_name_input) == 0:
            st.error("Name is a required field and cannot be empty!")
        else:
            st.success("Inputs validated.  Creating space...")

            # create the space
            command = CreateSpaceCommand()
            command.name = eval_name_input
            command.description = eval_desc_input
            command.go()

            st.success("Evaluation space created!")
