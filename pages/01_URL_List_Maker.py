# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import time
import io

def crawl_web_pages(url, pattern, max_depth=2):
    """
    指定されたURLからウェブページをクロールし、特定のパターンに一致する一意のリンクを抽出します。

    この関数は、指定されたURLから開始し、指定された深さまでリンクされたページを探索し、
    提供されたパターンに一致し、ウェブページ（HTMLドキュメント）につながるURLのみを収集します。
    無限ループを防ぐために、同じURLへの再アクセスは避けます。

    Args:
        url: クロールを開始するURL。
        pattern: URLで一致させるパターンを表す文字列（例： "/blog/"）。
        max_depth: クロールする最大深度。

    Returns:
        パターンに一致し、ウェブページにつながる一意のURLのリスト。
    """
    visited_urls = set()
    urls = []

    def crawl(url, depth):
        """
        再帰的なクロールを実行します。

        Args:
            url: クロールするURL。
            depth: 現在のクロールの深度。
        """
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


def download_urls(urls):
    data = "\n".join(urls).encode('utf-8')
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

# Streamlitの入力フォーム
start_url = st.text_input('URLを入力してください', value='https://www.thinkwithgoogle.com/intl/ja-jp/marketing-strategies/')
url_pattern = st.text_input('キーワードを入力してください', value='/marketing-strategies/')
max_depth = st.number_input('最大深度を入力してください', min_value=1, max_value=3, value=2)

if st.button("Search"):
    urls = crawl_web_pages(start_url, url_pattern, max_depth)
if urls is not None:
    if "selected_urls" not in st.session_state:
        st.session_state.selected_urls = []

    selected_urls = st.multiselect("URLを選択", urls, key="selected_urls")
    if selected_urls:
        download_urls(selected_urls)
    else:
        st.warning("URLが選択されていません。")
