import streamlit as st

if 'my_checkbox' not in st.session_state:
    st.session_state.my_checkbox = False

if st.checkbox("Check me", key="my_checkbox"):
    st.write("Checkbox is checked!")
else:
    st.write("Checkbox is not checked.")