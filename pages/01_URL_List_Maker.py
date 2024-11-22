# -*- coding: utf-8 -*-
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_web_pages(url, pattern, max_depth=2):
  """
  Crawls a given URL recursively to extract unique links to web pages
  matching a specific pattern.

  This function starts at a given URL and explores linked pages up to a
  specified depth, collecting only the URLs that match the provided pattern
  and lead to web pages (HTML documents). It avoids revisiting the same URLs
  to prevent infinite loops.

  Args:
    url: The URL to start crawling.
    pattern: A string representing the pattern to match in the URLs (e.g., "/blog/").
    max_depth: The maximum depth to crawl.

  Returns:
    A list of unique URLs matching the pattern and leading to web pages.
  """
  visited_urls = set()
  urls = []

  def crawl(url, depth):
    """
    Performs the recursive crawling.

    Args:
      url: The URL to crawl.
      depth: The current depth of the crawl.
    """
    if depth > max_depth:
      return

    if url in visited_urls:
      return
    visited_urls.add(url)

    try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()
      time.sleep(3)

      # Check if the response is an HTML document
      if 'text/html' not in response.headers['content-type']:
        return

    except requests.exceptions.RequestException as e:
      print(f"Error fetching {url}: {e}")
      return

    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the current URL matches the pattern
    if pattern in urlparse(url).path:
      urls.append(url)
      print(f"Found URL: {url}")

    for link in soup.find_all("a", href=True):
      absolute_url = urljoin(url, link["href"])

      # Check if the link leads to a web page (not an image, PDF, etc.)
      parsed_link = urlparse(absolute_url)
      if not parsed_link.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.rar')):
        crawl(absolute_url, depth + 1)

  crawl(url, 1)
  return urls

def get_title_from_url(url):
  """
  Fetches the title of a web page given its URL.

  Args:
    url: The URL of the web page.

  Returns:
    The title of the web page (str).
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error status codes
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    return title
  except requests.exceptions.RequestException as e:
    print(f"Failed to fetch the page: {e}")
    return None
  except Exception as e:
    print(f"Failed to extract the title: {e}")
    return None

def download_urls(urls):
    if not urls:
        st.warning("Please select at least one URL.")
        return

    text_content = "\n".join(urls)
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

if "checked_urls" not in st.session_state:
    st.session_state.checked_urls = set()

if st.button("Search"):
    urls = crawl_web_pages(start_url, url_pattern, max_depth)

    if urls:
        with st.form("url_form"):
            selected_urls = []
            for url in urls:
              
                checked = st.checkbox(url, key=url, value=(url in st.session_state.checked_urls))
                st.write(checked)
                st.write(url)
                if checked:  # チェックされている場合のみURLを追加
                    selected_urls.append(url)

            submitted = st.form_submit_button("選択したURLをダウンロード")
            if submitted:
                st.write(f"DEBUG: st.session_state.checked_urls before update: {st.session_state.checked_urls}") # 更新前の状態
                st.session_state.checked_urls = set(selected_urls)
                st.write(f"DEBUG: st.session_state.checked_urls after update: {st.session_state.checked_urls}") # 更新後の状態
                download_selected_urls(selected_urls)