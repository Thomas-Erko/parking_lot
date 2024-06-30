import streamlit as st

st.set_page_config(layout="wide", page_title="Home Page")

st.markdown("<h1 style='text-align: center; color: white;'>Home Page</h1>", unsafe_allow_html=True)
st.divider()

st.write("## Keep track of your propoerty")

st.write("""Teref is a product created to track your buisness' metrics.\n
        We track: 
            - Foot traffic 
            - Vehicle traffic 
            - Lot utilization rate 
            - Lot encroachment
         """)


col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    if st.button(label="Start Tracking!"):
        st.switch_page('pages/tracking_page.py')

