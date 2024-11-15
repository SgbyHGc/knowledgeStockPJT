import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")
url_list_maker = st.Page(page="contents/crawl_web_pages.py", title="URL List Maker")
class_name_finder = st.Page(page="contents/search_keyword.py", title="Class Name Finder")
summarizer = st.Page(page="contents/summarize_to_doc.py", title="Summarizer")
pg = st.navigation([url_list_maker, class_name_finder, summarizer])
pg.run()
