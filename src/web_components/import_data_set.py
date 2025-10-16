""" Import Data Set Content Component """
from datetime import date, timedelta
from io import StringIO
import streamlit as st
from gateways.object_storage_gateway import ObjectStorageGateway
from commands.from_snow import FromServiceNowCommand

def import_from_snow(space_id):
    """ Display form to import data from Service Now """
    col1, col2 = st.columns([0.275, 0.735])

    # start date
    start_date = None
    with col1:
        today = date.today()
        ninety_days_ago = today - timedelta(days=90)
        ninety_days_ago_str = ninety_days_ago.strftime('%Y-%m-%d')
        start_date = st.date_input("Start date", value=ninety_days_ago_str, format="MM/DD/YYYY", width=150)

    # end date
    end_date = None
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
    if st.button("Download from Service Now", type="primary"):
        from_snow_command = FromServiceNowCommand()
        from_snow_command.space_id = space_id
        from_snow_command.min_create_date = start_date
        from_snow_command.max_create_date = end_date
        from_snow_command.row_limit = -1
        if limit_results == limit_option_testing:
            from_snow_command.row_limit = 1
        elif limit_results == limit_option_basic:
            from_snow_command.row_limit = 10
        elif limit_results != limit_option_all and limit_results is not None:
            from_snow_command.row_limit = int(limit_results)
        from_snow_command.go()
        st.success("Successfully imported data from Service-Now!")


def import_file(space_id):
    """ Display form to import data from csv file. """
    # upload file
    csv_file = st.file_uploader("Choose CSV files to upload.")

    # submit button
    if st.button("Upload", type="primary"):
        if csv_file is not None:
            # receiving file status
            st.write(f"Receiving file upload...  {csv_file.name}")

            # retrieve data from file
            stringio = StringIO(csv_file.getvalue().decode("utf-8"))
            csv_file_contents = stringio.read()

            # file received status
            st.write("File received!  Uploading to space...")

            # upload file
            gateway = ObjectStorageGateway()
            path = f"{space_id}/raw/{csv_file.name}"
            gateway.upload(path, csv_file_contents)

            st.success("File Saved in Space!")

def import_data_set(space_id):
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
        import_from_snow(space_id)
    elif data_set_source_radio == file_option:
        import_file(space_id)
