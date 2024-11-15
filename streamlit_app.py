import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")
url_list_maker = st.Page(page="contents/01_crawl_web_pages.py", title="URL List Maker")
class_name_finder = st.Page(page="contents/02_search_keyword_in_div.py", title="Class Name Finder")
summarizer = st.Page(page="contents/03_summarize_to_doc.py", title="Summarizer")
pg = st.navigation([url_list_maker, class_name_finder, summarizer])
pg.run()
