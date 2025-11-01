import streamlit as st
import plotly.express as px

def show_category_scatterplot_widget(df):
    """ Display a scatterplot that shows ticket count density by category type.
    
        df - analysis dataframe
    """
    # validate arguments
    if df is None or len(df) == 0:
        raise ValueError("Input DataFrame is a required parameter and cannot be empty.")

    # create summary dataframe
    df.info()
    df['Count_by_Category'] = df.groupby('Category')['Category'].transform('count')
    df['Count_by_Subcategory'] = df.groupby('Subcategory')['Subcategory'].transform('count')
    df.info()
    print(df.head())

    # display new dataframe
    fig = px.scatter(df, x="Asset", y="Subcategory",
                    size="Count_by_Subcategory")
    st.plotly_chart(fig, key="Subcategory", on_select="rerun")
