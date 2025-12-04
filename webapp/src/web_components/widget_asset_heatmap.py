import logging
from calendar import monthrange
import streamlit as st
import pandas as pd
from web_components.widget_heatmap_grid import show_heatmap_grid_widget

logger = logging.getLogger(__name__)

MAX_ROWS = 20
PIVOT_DATE_COLUMN = "Date_Reported"

def show_asset_heatmap_widget(df):
    """ Display a heatmap that shows ticket counts by assets by day.
    
        df - analysis dataframe
    """
    # validate that key columns exist before trying to render
    if not "Date_Reported" in df.columns:
        st.write("Unsupported Data Import version.  Skipping heatmap render.")
        return
    
    """
    0   Incident_File      5 non-null      object
    1   Row                5 non-null      int64 
    2   Asset              5 non-null      object
    3   Summary            5 non-null      object
    4   Category           5 non-null      object
    5   Subcategory        5 non-null      object
    6   Is_Manual          5 non-null      bool  
    7   Is_Outage          5 non-null      bool  
    8   Status             5 non-null      object
    9   Date_Reported      4 non-null      object
    10  Date_Resolved      4 non-null      object
    11  Count_by_Category  5 non-null      int64 
    """

    # prepare dataframe for date analysis
    df = df.dropna(subset=[PIVOT_DATE_COLUMN])
    if len(df) == 0:
        logger.error("Data Set only had empty / null date data.")
        return

    # setup date range
    max_date = pd.to_datetime(df[PIVOT_DATE_COLUMN]).max()
    month = max_date.month
    year = max_date.year
    days_in_month = monthrange(year, month)[1]

    # prepare core dataframe (Asset/Date/Count)
    df['Date'] = pd.to_datetime(df[PIVOT_DATE_COLUMN]).dt.normalize()
    df = df[(df['Date'] >= f"{year}-{month}-1") & (df['Date'] <= f"{year}-{month}-{days_in_month}")]
    df = df[['Asset', 'Date']]
    df = df.groupby(['Asset', 'Date']).size().reset_index(name='Count')
    logging.info("Refined Data Frame: %s", df.info())

    # append total count (Asset/Count)
    df['Total'] = df.groupby('Asset')['Count'].transform('sum')

    # sort data frame
    df = df.sort_values(by=['Total', 'Asset', 'Date'], ascending=[False, True, True])

    # build header
    header = ["Config Item"]
    for i in range(days_in_month):
        header.append(str(i + 1))
    header.append("Count")

    # build asset rows
    rows = []
    prior_row = None
    for index, row in df.iterrows():
        # collect data points
        asset = row["Asset"]
        date = row["Date"]
        date_count = row["Count"]
        total = row["Total"]

        # create new row?
        if prior_row is not None and prior_row[0] != asset:
            prior_row = None

        # build new row
        if prior_row is None:
            # have we hit the max row count?
            if len(rows) >= MAX_ROWS:
                break

            # create new row
            asset_row = [asset]
            for i in range(days_in_month):
                cell_value = None
                if date.day == i:
                    cell_value = date_count
                asset_row.append(cell_value)
            asset_row.append(total)

            rows.append(asset_row)
            prior_row = asset_row
        
        # update existing
        else:
            prior_row[date.day + 1] = date_count

    # display heatmap
    show_heatmap_grid_widget(f"Top {MAX_ROWS} Incident Heat Map", year, month, header, rows)
