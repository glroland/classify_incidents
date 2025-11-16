import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from web_components.widget_category_scatterplot import show_category_scatterplot_widget

def view_evaluation_summary(space_id, command):
    # load the space metadata file
    metadata = command.metadata

    # display instructions if analysis has not yet occurred
    if metadata.summary is None or len(metadata.summary) == 0:
        st.write("After creating a space, import incident data and then run analysis using the other tabs.")
    else:
        # display scatter plot for analysis data
        df = command.analysis_df
        if df is not None:
            show_category_scatterplot_widget(df)

        # display executive summary
        st.write(metadata.summary)
