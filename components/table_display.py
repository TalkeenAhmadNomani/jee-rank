import streamlit as st
from helpers.status_utils import create_status_column

## Filtering 

def display_table_with_sections(df, rank, table_name, opening_down_limit=None):
    if df.empty:
        st.info(f"No programs available for {table_name}.")
        return

    df['Status'] = create_status_column(df, rank, opening_down_limit)
    df = df.dropna(subset=['Status'])
## for no program matched
    if df.empty:
        st.info(f"No programs match your criteria in {table_name}.")
        return

    df['Status_Order'] = df['Status'].map({'Fitting': 1, 'Aspirational': 2, 'Opening Down': 3})
    df = df.sort_values(['Status_Order', 'OR'])

    cols = ["Institute", "Program", "OR", "CR", "Status"]
    if "Quota" in df.columns:
        cols.insert(2, "Quota")
    if "Institute_Type" in df.columns:
        cols.insert(0, "Institute_Type")

    st.markdown(f"**{len(df)} programs found for {table_name}:**")
    st.dataframe(df[cols], hide_index=True)
