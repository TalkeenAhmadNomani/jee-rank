import streamlit as st
from helpers.data_loader import load_data, clean_all_data
from components.ui_elements import render_help_box, render_header
from components.table_display import display_table_with_sections
from helpers.filters import get_combined_dataframe, create_category_filter
from helpers.status_utils import create_status_column

# Load & clean data
data_dict = load_data()
if data_dict is None:
    st.stop()
data_dict = clean_all_data(data_dict)

# UI Header
render_header()

# Inputs
exam_type = st.selectbox("Select exam", ["JEE Advanced", "JEE Mains"])
rank = st.number_input(f"Enter your {exam_type} rank (category rank, if applicable)", min_value=1, value=1000)
year = st.selectbox("Select year", [2022, 2023, 2024])

if exam_type == "JEE Advanced":
    institute_type = "IITs"
    st.info("🎯 JEE Advanced: Showing IIT programs only")
else:
    institute_type = st.selectbox("Select institute type", ["ALL", "NITs", "IIITs", "GFTIs"])

category = st.selectbox("Select category", ["OPEN", "EWS", "OBC-NCL", "SC", "ST", "PwD"])
gender = st.selectbox("Select gender", ["Gender-Neutral", "Female-only"])

render_help_box()

if st.button("Find Eligible Programs"):
    # Logic for data filtering and display
    from helpers.filters import process_user_selection
    process_user_selection(data_dict, exam_type, institute_type, year, category, gender, rank)
