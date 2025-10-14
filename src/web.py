""" Streamlit Web Application guiding the Incident analysis and automation workflow. """
import logging
import streamlit as st
from web_components.sidebar import sidebar
from web_components.actions import actions
from web_components.home import home
from web_components.create_new import create_new
from web_components.view_evaluation import view_evaluation
from web_components.import_data_set import import_data_set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Streamline Operations with AI Automation",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Sidebar
with st.sidebar:
    sidebar()

# Handle Page Actions
if not "action" in st.query_params or st.query_params["action"] == actions.HOME:
    home()
elif st.query_params["action"] == actions.CREATE_EVALUATION:
    create_new()
elif st.query_params["action"] == actions.IMPORT_DATA_SET:
    import_data_set()
elif st.query_params["action"] == actions.VIEW_EVALUATION:
    view_evaluation()
else:
    # Error - unknown action
    msg = f"Unknown action passed into application!  Action={st.query_params["action"]}"
    logger.error(msg)
    raise ValueError(msg)

# Hide Streamlit's main Menu
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True) 
