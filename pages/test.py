import streamlit as st
import os
import base64

import streamlit as st

if "checkboxes" not in st.session_state:
    st.session_state.checkboxes = {}

options = ["Option 1", "Option 2", "Option 3"]

for i, option in enumerate(options):
    st.checkbox(option, key=f"checkbox_{i}", value=st.session_state.checkboxes.get(f"checkbox_{i}", False))

if st.button("Submit"):
    selected_options = [option for i, option in enumerate(options) if st.session_state[f"checkbox_{i}"]]
    st.write(f"Selected options: {selected_options}")