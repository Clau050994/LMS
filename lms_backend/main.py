# app.py
import streamlit as st
import streamlit_index1
import streamlit_index2

st.set_page_config(page_title="Library App", layout="wide")

page = st.sidebar.radio("Go to", ["Dashboard", "Homepage"])

if page == "Dashboard":
    streamlit_index1.run()
elif page == "Homepage":
    streamlit_index2.run()
