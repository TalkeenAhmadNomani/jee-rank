import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    try:
        return {
            'IIT': {y: pd.read_csv(f"data/ranks{y}.csv") for y in [2022, 2023, 2024]},
            'NIT': {y: pd.read_csv(f"data/nits{y}.csv") for y in [2022, 2023, 2024]},
            'IIIT': {y: pd.read_csv(f"data/IIITs{y}.csv") for y in [2022, 2023, 2024]},
            'GFTI': {y: pd.read_csv(f"data/GFTIs{y}.csv") for y in [2022, 2023, 2024]}
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def clean_rank_data(df):
    if df is None or df.empty:
        return df
    df_clean = df.copy()
    for col in ['OR', 'CR']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df_clean[col] = pd.to_numeric(df_clean[col].replace('', np.nan), errors='coerce')
    return df_clean.dropna(subset=['OR', 'CR'])

def clean_all_data(data_dict):
    for inst_type in data_dict:
        for year in data_dict[inst_type]:
            data_dict[inst_type][year] = clean_rank_data(data_dict[inst_type][year])
    return data_dict
