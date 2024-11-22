import streamlit as st
import os
import base64

def download_txt(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}.txt">Download {filename}.txt</a>'
    st.markdown(href, unsafe_allow_html=True)


st.title("URL Checker and Downloader")

urls = {
    "Google": "https://www.google.com",
    "Yahoo": "https://www.yahoo.com",
    "Bing": "https://www.bing.com",
    "DuckDuckGo": "https://duckduckgo.com",
    "GitHub": "https://github.com"  # 追加のURL
}

selected_urls = {}
for name, url in urls.items():
    if st.checkbox(name):
        selected_urls[name] = url


if st.button("Download selected URLs"):
    if selected_urls:
        text = ""
        for name, url in selected_urls.items():
            text += f"{name}: {url}\n"

        download_txt(text, "selected_urls")
    else:
        st.warning("Please select at least one URL.")
