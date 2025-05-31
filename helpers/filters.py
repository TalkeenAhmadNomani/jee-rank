import pandas as pd
import streamlit as st
from components.table_display import display_table_with_sections

def get_combined_dataframe(year, institute_types, category, gender, data_dict):
    combined_df = pd.DataFrame()
    for inst_type in institute_types:
        df = data_dict.get(inst_type, {}).get(year)
        if df is None or df.empty:
            continue
        df = df.copy()
        df['Institute_Type'] = inst_type
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

def create_category_filter(df, category):
    if category == "PwD":
        return df["Seat Type"].str.contains(r'\(PwD\)', case=False, na=False)
    return df["Seat Type"].str.upper() == category.upper()

def process_user_selection(data_dict, exam_type, institute_type, year, category, gender, rank):
    if exam_type == "JEE Advanced":
        types = ["IIT"]
    elif institute_type == "ALL":
        types = ["NIT", "IIIT", "GFTI"]
    else:
        types = [institute_type.rstrip('s').upper()]

    df = get_combined_dataframe(year, types, category, gender, data_dict)
    if df.empty:
        st.error("No data found for the selected criteria.")
        return

    df = df[
        create_category_filter(df, category) &
        (df["Gender"].str.lower() == gender.lower())
    ]

    display_table_with_sections(df, rank, "Eligible Programs")
