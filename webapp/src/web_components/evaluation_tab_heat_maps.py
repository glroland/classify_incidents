import logging
from calendar import monthrange
import streamlit as st
import pandas as pd
from web_components.widget_heatmap_grid import show_heatmap_grid_widget

logger = logging.getLogger(__name__)

MAX_ROWS = 20
PIVOT_DATE_COLUMN = "Date_Reported"

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

def render_heat_map(title, pivot_entity_type, pivot_column, df):
    # validate that key columns exist before trying to render
    if not PIVOT_DATE_COLUMN in df.columns:
        st.write("Unsupported Data Import version.  Skipping heatmap render.")
        return

    # prepare dataframe for date analysis
    prior_count = len(df)
    df = df.dropna(subset=[PIVOT_DATE_COLUMN])
    if len(df) != prior_count:
        msg = f"WARNING: Dropped {prior_count - len(df)} rows from data set that had no value for '{PIVOT_DATE_COLUMN}' column."
        logger.warning(msg)
        st.markdown(f":red[**{msg}**]")
    if len(df) == 0:
        logger.warning("Data Set has no data to process in heat map view")
        st.markdown("I'm sorry but this data set has no data to analyze.\n\nThis may be due to the analysis process not running first or an issue with the AI model analyzing the raw data.")
        return

    # setup date range
    max_date = pd.to_datetime(df[PIVOT_DATE_COLUMN]).max()
    month = max_date.month
    year = max_date.year
    days_in_month = monthrange(year, month)[1]

    # prepare core dataframe (PivotColumn/Date/Count)
    df['Date'] = pd.to_datetime(df[PIVOT_DATE_COLUMN]).dt.normalize()
    df = df[(df['Date'] >= f"{year}-{month}-1") & (df['Date'] <= f"{year}-{month}-{days_in_month}")]
    df = df[[pivot_column, 'Date']]
    df = df.groupby([pivot_column, 'Date']).size().reset_index(name='Count')
    logging.info("Refined Data Frame: %s", df.info())

    # append total count (Asset/Count)
    df['Total'] = df.groupby(pivot_column)['Count'].transform('sum')

    # sort data frame
    df = df.sort_values(by=['Total', pivot_column, 'Date'], ascending=[False, True, True])

    # build header
    header = [pivot_entity_type]
    for i in range(days_in_month):
        header.append(str(i + 1))
    header.append("Count")

    # build asset rows
    rows = []
    prior_row = None
    for index, row in df.iterrows():
        # collect data points
        pivot = row[pivot_column]
        date = row["Date"]
        date_count = row["Count"]
        total = row["Total"]

        # create new row?
        if prior_row is not None and prior_row[0] != pivot:
            prior_row = None

        # build new row
        if prior_row is None:
            # have we hit the max row count?
            if len(rows) >= MAX_ROWS:
                break

            # create new row
            pivot_row = [pivot]
            for i in range(days_in_month):
                cell_value = None
                if date.day == i:
                    cell_value = date_count
                pivot_row.append(cell_value)
            pivot_row.append(total)

            rows.append(pivot_row)
            prior_row = pivot_row
        
        # update existing
        else:
            prior_row[date.day + 1] = date_count

    # display heatmap
    show_heatmap_grid_widget(f"{title}", year, month, header, rows)


def view_evaluation_heat_map(space_id, command):
    # retrieve data set
    df = command.analysis_df
    if df is None or len(df) == 0:
        st.write("Please run the analysis tool first.")
        return
    
    # setup radio button labels
    RADIO_LABEL_TOP_CIS = "Top Config Items"
    RADIO_LABEL_BY_CATEGORY = "Issue Category"
    RADIO_LABEL_BY_SUBCATEGORY = "Issue Subcategory"
    heat_map_type = st.radio(
            "View Incident Heat Map by:",
            (RADIO_LABEL_TOP_CIS, RADIO_LABEL_BY_CATEGORY, RADIO_LABEL_BY_SUBCATEGORY),
            horizontal=True
    )

    if heat_map_type == RADIO_LABEL_BY_CATEGORY:
        render_heat_map("Classified Incident Heat Map", "Issue Type", "Category", df)
    elif heat_map_type == RADIO_LABEL_BY_SUBCATEGORY:
        render_heat_map("Classified Incident Heat Map", "Issue Type", "Subcategory", df)
    else:
        render_heat_map(f"Top {MAX_ROWS} Incident Heat Map", "Config Item", "Asset", df)
