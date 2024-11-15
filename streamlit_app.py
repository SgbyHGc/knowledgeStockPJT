import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")
url_list_maker = st.Page(page="crawl_web_pages.py", title="URL List Maker", icon=":material/search:")
class_name_finder = st.Page(page="search_keyword.py", title="Class Name Finder", icon=":material/search:")
summarizer = st.Page(page="summarize_to_doc.py", title="Summarizer", icon=":material/apps:")
pg = st.navigation([url_list_maker, class_name_finder, summarizer])
pg.run()
