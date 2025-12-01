import logging
import streamlit as st
import plotly.express as px

logger = logging.getLogger(__name__)

def show_category_scatterplot_widget(df):
    """ Display a scatterplot that shows ticket count density by category type.
    
        df - analysis dataframe
    """
    # validate arguments
    if df is None:
        msg = "Input DataFrame is a required parameter."
        logger.error(msg)
        raise ValueError(msg)

    # disallow empty data frames
    if len(df) == 0:
        logger.warning("Input DataFrame cannot be empty for widget to render.")
    else:
        # create summary dataframe
        df.info()
        df['Count_by_Category'] = df.groupby('Category')['Category'].transform('count')

        # handle situations where nan is pervasive in the data to be plotted
        logger.info("BEFORE CLEANSE...  Shape=%s. Head=%s", df.shape, df.head())
        df = df.dropna(thresh=(len(df.columns) - 7))
        logger.info("AFTER CLEANSE...  Shape=%s. Head=%s", df.shape, df.head())
        if len(df) == 0:
            logger.warning("DataFrame is empty after cleansing NaNs.  Skipping graph rendering...")
        else:
            # display new dataframe
            fig = px.scatter(df, x="Asset", y="Category",
                            size="Count_by_Category")
            st.plotly_chart(fig, key="Category", on_select="rerun")
