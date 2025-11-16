import streamlit as st
from web_components.widget_asset_heatmap import show_asset_heatmap_widget

def view_evaluation_heat_map_by_server(space_id, command):
    df = command.analysis_df
    if df is None or len(df) == 0:
        st.write("Please run the analysis tool first.")
    else:
        show_asset_heatmap_widget(df)
