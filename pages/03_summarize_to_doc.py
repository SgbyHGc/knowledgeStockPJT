import streamlit as st
import requests
from bs4 import BeautifulSoup

def url_list_from_txt(file_path):
  try:
    with open(file_path, 'r') as f:
      urls = [line.strip() for line in f]
    return urls
  except FileNotFoundError:
    print(f"エラー: ファイルが見つかりません ({file_path})")
    return []


# Streamlitアプリのタイトルを設定
st.title("NotebookLM用データソースの出力 🔎")

st.markdown('---')
st.markdown('要約を生成したいページのURLが入ったtxtファイルをアップロードしてください。個々のURLは改行で区切られている必要があります')
st.markdown('---')

# URLとキーワードの入力
uploaded_file = st.file_uploader("txtファイルを選択してください", type='txt')

url = st.text_input("URLを入力してください")
keyword = st.text_input("キーワードを入力してください")

# 検索ボタン
if st.button("search"):
  if uploaded_file is not None:
    data = url_list_from_txt(uploaded_file)
    st.write(data)
  else:
    st.warning("txtファイルをアップロードしてください")