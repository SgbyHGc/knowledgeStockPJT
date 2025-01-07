# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
# import hashlib
import time
# import io

def get_title_from_url(url):
  """
  Fetches the title of a web page given its URL.

  Args:
    url: The URL of the web page.

  Returns:
    The title of the web page (str).
  """
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("title").text
  except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch the page: {url} - {e}")
  except Exception as e:
    st.error(f"Failed to extract the title: {url} - {e}")
  return None

def download_selected_urls(selected_urls):
  if not selected_urls:
    st.error("No URLs selected for download.")
    return

  st.download_button(
    label="選択したURLをダウンロード",
    data="\n".join(selected_urls).encode('utf-8'),
    file_name="selected_urls.txt",
    mime="text/plain",
    on_click=lambda: st.write("ダウンロードを開始します...")
  )

def crawl_web_pages(start_url, pattern, max_depth=2):
  visited_urls = st.session_state.visited_urls
  matched_urls = set()
  
  def _crawl(url, depth, progress_bar, progress_text):
    if depth > max_depth or url in visited_urls:
      return

    visited_urls.add(url)
    st.session_state.visited_urls = visited_urls

    try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()
      time.sleep(3)  # サーバー負荷軽減のためリクエスト間隔を調整

      # HTML以外はスキップ
      if response.headers.get('content-type', '').lower().find('text/html') == -1:
        return
        
      soup = BeautifulSoup(response.content, "html.parser")

      # パターンマッチ確認
      if pattern in url:
        matched_urls.add(url)

      # 進行状況更新
      progress_bar.progress(min(1.0, len(visited_urls) / (max_depth * 50)))
      progress_text.text(f"処理済みURL数: {len(visited_urls)} (該当URL数: {len(matched_urls)})")

      # 再帰的にリンクをたどる
      for link in soup.find_all("a", href=True):
        absolute_url = urljoin(url, link["href"])
        # 不要なファイル形式と訪問済みURLを除外
        if not any(absolute_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.rar']):
          _crawl(absolute_url, depth + 1, progress_bar, progress_text)
    except requests.exceptions.RequestException as e:
      st.error(f"エラー: {url} - {e}")

  # 進行状況表示の初期化
  progress_bar = st.progress(0)
  progress_text = st.empty()
  progress_text.text("処理開始...")

  # クロール実行
  _crawl(start_url, 1, progress_bar, progress_text)

  # 完了メッセージ
  progress_bar.progress(1.0)
  progress_text.text(f"完了: 総URL数 {len(visited_urls)} (該当URL数: {len(matched_urls)})")

  return list(matched_urls)

# --- Streamlit UI ---
st.set_page_config(page_title="URL収集アプリ")
st.title("URL収集アプリケーション 📝")
st.write("""
URLのページに記載されているリンクを辿ってURLのリストを作成します。\n
指定したキーワードが含まれるURLのみをリスト化します。サブディレクトリなどを指定してください。
深度は、リンク先のリンクの深さを示します。リンク先のリンク先のリンクまで収集する場合は3に設定してください。
""")
st.write('---')

# ユーザー入力
start_url = st.text_input("開始URL:", value="https://www.thinkwithgoogle.com/intl/ja-jp/marketing-strategies/")
url_pattern = st.text_input("URLパターン:", value="/marketing-strategies/")
max_depth = st.number_input("最大深度:", min_value=1, max_value=5, value=2)

# セッション状態の初期化
if 'visited_urls' not in st.session_state:
    st.session_state.visited_urls = set()
if 'urls' not in st.session_state:
    st.session_state.urls = []

# クロール開始
if st.button("クロール開始"):
    st.session_state.visited_urls.clear()
    st.session_state.urls = []
    if start_url:
        st.session_state.urls = crawl_web_pages(start_url, url_pattern, max_depth)
    else:
        st.warning("開始URLを入力してください。")

# 結果表示と選択
if st.session_state.urls:
    st.write("---")
    selected_urls = []
    for i, url in enumerate(st.session_state.urls):
        title = get_title_from_url(url)
        # st.write(f"タイトル: {title}")
        st.markdown(f"**{title}**")
        # チェックボックスの初期状態を管理
        checkbox_key = f'checkbox_{i}'
        if checkbox_key not in st.session_state:
            st.session_state[checkbox_key] = True
        if st.checkbox(url, key=checkbox_key):
            selected_urls.append(url)
        st.markdown("<br>", unsafe_allow_html=True)
        # st.write("---")

    # ダウンロードボタン
    download_selected_urls(selected_urls)
