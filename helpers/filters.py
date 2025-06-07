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

def safe_numeric_filter(df, column, operator, value):
    try:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        if operator == ">=":
            return df[column] >= value
        elif operator == "<":
            return df[column] < value
        elif operator == "<=":
            return df[column] <= value
        elif operator == ">":
            return df[column] > value
        else:
            return pd.Series([True] * len(df))
    except Exception:
        return pd.Series([False] * len(df))

def process_user_selection(data_dict, exam_type, institute_type, year, category, gender, rank):
    try:
        if exam_type == "JEE Advanced":
            institute_types = ["IIT"]
            display_name = "IITs"
        elif institute_type == "ALL":
            institute_types = ["NIT", "IIIT", "GFTI"] 
            display_name = "All Engineering Colleges (NITs, IIITs, GFTIs)"
        else:
            institute_types = [institute_type.rstrip('s').upper()]  
            display_name = institute_type

        if exam_type == "JEE Advanced" or (exam_type == "JEE Mains" and institute_type == "ALL"):
            df = get_combined_dataframe(year, institute_types, category, gender, data_dict)
        else:
            inst_key = institute_types[0]
            if inst_key in data_dict and year in data_dict[inst_key]:
                df = data_dict[inst_key][year].copy()
            else:
                st.error(f"Data not available for {institute_type} {year}")
                st.stop()

        if df.empty:
            st.error("No data available for the selected criteria.")
            st.stop()

        required_columns = ["Seat Type", "Gender", "OR", "CR", "Institute", "Program"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in data: {missing_columns}")
            st.write("Available columns:", df.columns.tolist())
            st.stop()

        base_filter = (
            create_category_filter(df, category) &
            df["Gender"].str.contains(gender, case=False, na=False)
        )

        # --- Recommended Programs Table ---
        st.subheader("🎯 All Recommended Programs")
        st.caption("Aspirational: CR from rank-300 to rank-1 | Fitting: OR ≤ rank ≤ CR | Opening Down: OR from rank+1 to rank+500")
        if category == "PwD":
            st.caption("*PwD Category*: Includes OPEN(PwD), SC(PwD), OBC-NCL(PwD), etc.")
        st.caption("For reservations, OR and CR shown correspond to category rank.")
        
        table1_filter = base_filter & (
            (safe_numeric_filter(df, "CR", ">=", rank - 300) & safe_numeric_filter(df, "CR", "<", rank)) |
            (safe_numeric_filter(df, "OR", "<=", rank) & safe_numeric_filter(df, "CR", ">=", rank)) |
            (safe_numeric_filter(df, "OR", ">", rank) & safe_numeric_filter(df, "OR", "<=", rank + 500))
        )
        display_table_with_sections(df[table1_filter], rank, f"All Recommended {display_name} Programs")

        # --- student can see Circuital Programs Table  ---
        st.markdown("---")
        st.subheader("⚡ Circuital Programs")
        circuital_keywords = ['Computer Science', 'Electrical', 'Electronics', 'Artificial', 'Mathematics', 'Instrumentation', 'Computational', 'Circuit', 'Data Science', 'CSE']
        circuital_pattern = '|'.join(circuital_keywords)

        table2_filter = base_filter & (
            df["Program"].str.contains(circuital_pattern, case=False, na=False)
        ) & (
            (safe_numeric_filter(df, "CR", ">=", rank - 300) & safe_numeric_filter(df, "CR", "<", rank)) |
            (safe_numeric_filter(df, "OR", "<=", rank) & safe_numeric_filter(df, "CR", ">=", rank)) |
            safe_numeric_filter(df, "OR", ">", rank)
        )
        display_table_with_sections(df[table2_filter], rank, f"Circuital {display_name} Programs")

        # --- Old 7 IITs Table ---
        if exam_type == "JEE Advanced":
            st.markdown("---")
            st.subheader("🏛️ Old 7 IITs")
            old_iits = ['Bombay', 'Delhi', 'Kharagpur', 'Madras', 'Kanpur', 'Roorkee', 'Guwahati']
            old_iits_pattern = '|'.join(old_iits)

            table3_filter = base_filter & (
                df["Institute"].str.contains(old_iits_pattern, case=False, na=False)
            ) & (
                (safe_numeric_filter(df, "OR", ">=", rank - 300) & safe_numeric_filter(df, "OR", "<", rank)) |
                (safe_numeric_filter(df, "OR", "<=", rank) & safe_numeric_filter(df, "CR", ">=", rank)) |
                safe_numeric_filter(df, "OR", ">", rank)
            )
            display_table_with_sections(df[table3_filter], rank, "Old 7 IITs Programs")

    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.write("Please check your CSV file format and column names.")
        st.write("Error details:", str(e))
