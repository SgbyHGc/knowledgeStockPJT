# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
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
    """
    URLのリストをテキストファイルとしてダウンロードします。
    """
    if not urls:
        st.warning("URLが選択されていません。")
        return

    f = io.BytesIO()  # BytesIOオブジェクトを作成
    f.write("\n".join(urls).encode('utf-8'))  # URLをUTF-8エンコーディングで書き込む
    f.seek(0)  # ファイルポインタを先頭に戻す
    filename = "selected_urls.txt"
    st.download_button(
        label="選択したURLをダウンロード",
        data=f,
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

    if urls:
        selected_urls = []
        for url in urls:
            key = f"button_{url}"
            is_selected = st.session_state.url_states.get(key, False)
            if st.button(url, key=key):
                is_selected = not is_selected
            st.session_state.url_states[key] = is_selected

            if is_selected:
                selected_urls.append(url)

        # ここに変更を加えます
        if st.button("選択したURLをダウンロード", use_container_width=True):  # use_container_widthを追加
            if selected_urls:
                download_urls(selected_urls)
            else:
                st.warning("URLが選択されていません。") # ダウンロードボタンを押したときに警告を表示
    elif not urls and start_url and url_pattern: # クロール結果が空で、入力があれば
        st.warning("条件に一致するURLが見つかりませんでした。") # 検索ボタンを押したときに警告を表示
    elif not start_url or not url_pattern: # URLまたはキーワードが入力されていない場合
        st.warning("URLとキーワードを入力してください")