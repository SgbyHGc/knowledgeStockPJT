import streamlit as st
import os
import base64

if st.button("Search"):
    urls = crawl_web_pages(start_url, url_pattern, max_depth)

    if urls:
        selected_urls = []  # フォームの外でリストを初期化
        for url in urls:
            checked = st.checkbox(url, key=url) # st.form を使わない
            if checked:
                selected_urls.append(url)

        if st.button("ダウンロード"): # 別のボタンでダウンロード処理を実行
            download_selected_urls(selected_urls)