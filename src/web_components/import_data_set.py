""" Import Data Set Content Component """
from datetime import date, timedelta
import streamlit as st

def import_from_snow():
    """ Display form to import data from Service Now """
    col1, col2 = st.columns([0.275, 0.735])

    # start date
    with col1:
        today = date.today()
        ninety_days_ago = today - timedelta(days=90)
        ninety_days_ago_str = ninety_days_ago.strftime('%Y-%m-%d')
        start_date = st.date_input("Start date", value=ninety_days_ago_str, format="MM/DD/YYYY", width=150)

    # end date
    with col2:
        end_date = st.date_input("End date", value="today", format="MM/DD/YYYY", width=150)

    # limit results
    limit_option_testing = "1 - For testing purposes"
    limit_option_basic = "10 - For basic exploration"
    limit_option_all = "No limit - Pull everything"
    limit_results = st.selectbox(
        "Limit the data extract",
        [limit_option_testing, limit_option_basic, limit_option_all],
        index=None,
        placeholder="Select a predefined limit or enter a new one",
        accept_new_options=True,
        width=510,
    )

    # submit button
    st.button("Download from Service Now", type="primary")

def import_file():
    """ Display form to import data from csv file. """
    # data set name
    data_set_input = st.text_input("Short description of data set:", "", max_chars=25, width=400)

    # submit button
    st.button("Upload", type="primary")

def import_data_set():
    st.header("Import New Data Set")

    # display upload process selection radio button
    snow_option = ":rainbow[Service-Now]"
    file_option = "Import File :movie_camera:"
    data_set_source_radio = st.radio(
        "To begin, please select the source of the new data set:",
        [snow_option, file_option],
        captions=[
            "Retrieve directly from SNOW using REST API",
            "Upload a comma delimited file.",
        ],
        horizontal=True,
    )

    # display appropriate web form
    if data_set_source_radio == snow_option:
        import_from_snow()
    elif data_set_source_radio == file_option:
        import_file()
