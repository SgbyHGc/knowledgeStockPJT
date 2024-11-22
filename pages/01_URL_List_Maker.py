# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import io

def crawl_web_pages(url, pattern, max_depth=2):
    """Crawls web pages and returns matching URLs."""
    visited_urls = set()
    urls = []

    def crawl(url, depth):
        """Recursive crawling function."""
        if depth > max_depth:
            return

        if url in visited_urls:
            return
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(1)  # Reduce delay to 1 second

            if 'text/html' not in response.headers.get('content-type', ''):
                return

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching {url}: {e}")  # Use st.error for cleaner output
            return

        soup = BeautifulSoup(response.content, "html.parser")

        if pattern in urlparse(url).path:
            urls.append(url)

        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(url, link["href"])
            parsed_link = urlparse(absolute_url)
            if not parsed_link.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.rar')):
                crawl(absolute_url, depth + 1)

    crawl(url, 1)
    return urls

def download_urls(urls):
    """Downloads selected URLs as a text file."""
    if not urls:
        st.warning("No URLs selected.")
        return

    f = io.StringIO("\n".join(urls))  # Use StringIO to create in-memory file
    st.download_button(
        label="Download Selected URLs",
        data=f,
        file_name="selected_urls.txt",
        mime="text/plain",
    )


st.title("URL List Generator")
st.markdown("""
This tool crawls a website and generates a list of URLs matching a specific pattern.
""")


start_url = st.text_input("Enter starting URL", value="https://www.thinkwithgoogle.com/intl/ja-jp/marketing-strategies/")
url_pattern = st.text_input("Enter keyword/pattern", value="/marketing-strategies/")
max_depth = st.number_input("Enter max depth", min_value=1, max_value=3, value=2)

if "url_states" not in st.session_state:
    st.session_state.url_states = {}

if st.button("Search"):
    urls = crawl_web_pages(start_url, url_pattern, max_depth)

    if urls:
        selected_urls = []
        for url in urls:
            key = f"button_{url}"
            is_selected = st.session_state.url_states.get(key, False)
            if st.checkbox(url, key=key, value=is_selected):  # Use checkbox for selection
                st.session_state.url_states[key] = True
                selected_urls.append(url)
            else:
                st.session_state.url_states[key] = False  # Uncheck


        download_urls([url for url, selected in st.session_state.url_states.items() if selected and url.startswith("button_")]) # Download based on checkbox state