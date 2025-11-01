import streamlit as st
import plotly.graph_objects as go

def show_asset_heatmap_widget(df):
    """ Display a heatmap that shows ticket counts by assets by day.
    
        df - analysis dataframe
    """
    # prepare data
    null_date_val = df["Date_Reported"].dropna().min()
    df["Date_Reported"] = df["Date_Reported"].fillna(null_date_val)

    # build X and Y axises
    asset_list = df["Asset"]
    tdate_list = df["Date_Reported"]

    # populate data per cell
    counts_dim = []
    for asset in asset_list:
        cell_list = []
        for tdate in tdate_list:
            count = ((df['Asset'] == asset) & (df['Date_Reported'] == tdate)).sum()
            cell_list.append(count)
        counts_dim.append(cell_list)

    # display heatmap
    custom_colorscale = [
        [0.0, 'white'],     # 0% of the data range maps to blue
        [0.5, 'yellow'],    # 50% of the data range maps to yellow
        [1.0, 'red']        # 100% of the data range maps to red
    ]
    fig = go.Figure(data=go.Heatmap(
            z=counts_dim,
            x=tdate_list,
            y=asset_list,
            colorscale=custom_colorscale,
            hoverongaps=True))
    st.plotly_chart(fig, key="Asset", on_select="rerun")
