# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import time
import io

def crawl_web_pages(url, pattern, max_depth=2):
    visited_urls = set()
    urls = []

    def crawl(url, depth):
        if depth > max_depth:
            return

        if url in visited_urls:
            return
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # エラーが発生した場合、例外を発生させる
            time.sleep(3)  # サーバーへの負荷を軽減するため、少し待機

            # レスポンスがHTMLドキュメントであることを確認
            content_type = response.headers.get('content-type')
            if content_type is None or 'text/html' not in content_type.lower():
                return

        except requests.exceptions.RequestException as e:
            st.error(f"{url} の取得中にエラーが発生しました: {e}")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # 現在のURLがパターンに一致するか確認
        if pattern in urlparse(url).path:
            urls.append(url)

        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(url, link["href"])

            # リンクがウェブページ（画像、PDFなどではない）につながることを確認
            parsed_link = urlparse(absolute_url)
            if not parsed_link.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.rar')):
                crawl(absolute_url, depth + 1)

    crawl(url, 1)
    return urls


def download_urls(selected_urls):
    data = "\n".join(selected_urls).encode('utf-8')
    filename = "selected_urls.txt"
    st.download_button(
        label="選択したURLをダウンロード",
        data=data,
        file_name=filename,
        mime="text/plain",
    )


# Streamlitアプリのタイトルを設定
st.title("URLリスト作成 📝")
st.markdown('---')
st.markdown("""
URLのページに記載されているリンクを辿ってURLのリストを作成します。
指定したキーワードが含まれるURLのみをリスト化します。サブディレクトリなどを指定してください。
深度は、リンク先のリンクの深さを示します。リンク先のリンク先のリンクまで収集する場合は3。
""")
st.markdown('---')

st.session_state.urls = None

with st.form('crawl'):
    start_url = st.text_input('URLを入力してください', value='https://www.thinkwithgoogle.com/intl/ja-jp/marketing-strategies/search/')
    url_pattern = st.text_input('キーワードを入力してください', value='/marketing-strategies/')
    max_depth = st.number_input('最大深度を入力してください', min_value=1, max_value=3, value=2)
    submit_crawl = st.form_submit_button('Crawl')
    if submit_crawl:
        urls = crawl_web_pages(start_url, url_pattern, max_depth)
        st.session_state.urls = urls

with st.form('download'):
    if st.session_state.urls:
        for i, url in enumerate(st.session_state.urls):
            selected = st.checkbox(url, key=f"checkbox_{i}")  # チェックボックスにユニークなキーを設定
            st.session_state.selected_urls[i] = selected  # チェックボックスの状態を更新
        submit_download = st.form_submit_button('Download')
    if submit_download:
        selected_urls = [url for i, url in enumerate(st.session_state.urls) if st.session_state.selected_urls[i]]
        st.write("選択されたURL:", selected_urls)
