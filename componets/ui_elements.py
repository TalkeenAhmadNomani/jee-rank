import streamlit as st

def render_header():
    st.markdown("<h1 style='text-align: center;'>🎓 JOSAA College & Branch Finder</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Find eligible colleges and programs based on your JEE rank.</p>", unsafe_allow_html=True)
    st.markdown("""<hr style="margin-top: 2em;">""", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Created by Musaib Bin Bashir.</p>", unsafe_allow_html=True)

def render_help_box():
    with st.expander("ℹ️ Help"):
        st.markdown("""
        - **OR** = Opening Rank  
        - **CR** = Closing Rank  
        - **Status**:
            - *Aspirational*: CR is between (Rank - 300) and (Rank - 1)  
            - *Fitting*: OR ≤ Rank ≤ CR  
            - *Opening Down*: OR is just above your rank  
        - Use filters wisely to get the best results.
        """)
