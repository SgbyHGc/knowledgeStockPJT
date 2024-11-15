import streamlit as st
import requests
from bs4 import BeautifulSoup

def url_list_from_txt(uploaded_file):
  try:
    urls = uploaded_file.getvalue().decode('utf-8').splitlines()
    return urls
  except UnicodeDecodeError:
    st.error("エラー: ファイルの文字コードがUTF-8ではありません。")
    return []
  
def get_text_by_class(url, class_name):
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    target_divs = soup.find_all('div', class_=class_name)
    if target_divs:
      extracted_text = ''.join([div.text.strip() for div in target_divs])
      extracted_text = re.sub(r"\n+", "\n", extracted_text)
      return extracted_text
    else:
      return None
  except requests.exceptions.RequestException as e:
    print(f"Failed to fetch the webpage: {e}")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

# Streamlitアプリのタイトルを設定
st.title("NotebookLM用データソースの出力")

st.markdown('---')
st.markdown('要約を生成したいページのURLが入ったtxtファイルをアップロードしてください。個々のURLは改行で区切られている必要があります')
st.markdown('---')

# URLとキーワードの入力
uploaded_file = st.file_uploader("txtファイルを選択してください", type='txt')
class_name = st.text_input("URLのページに共通する、抽出したい部分のclass nameを指定してください")
api_key = st.text_input("GeminiのAPI Keyを入力してください")


# 検索ボタン
if st.button("search"):
  if uploaded_file is not None:
    data = url_list_from_txt(uploaded_file)
    st.write(data)
  else:
    st.warning("txtファイルをアップロードしてください")