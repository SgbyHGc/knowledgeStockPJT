# -*- coding: utf-8 -*-

import streamlit as st
import requests
import time
import re
from bs4 import BeautifulSoup
import google.generativeai as genai


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

def gemini(extacted_text, api_key):
  template = """
  ## Persona
  あなたはトレーニング資料作成のスペシャリストです。
  以下のテキストデータから内容を読み取り、箇条書きで要点を詳細に説明してください。

  ## Context
  営業部員が顧客向けの提案資料作成や顧客からの質問を受けた際に参考となる資料が多くありますが、
  一つ一つを把握することは困難なため全部読まなくても要点をつかめるようにまとめる必要があります。

  ## テキストータ
  <text_data>

  ## Task
  - 文章の主要なポイントを要点として見逃さないよう注意して3~5個で抽出してください。
  - 要点を出力する際は簡潔に日本語で500文字以内に収めてください。
  - 検索用のタグとして、利用者が使えそうな検索用のタグも当てはまりそうなものを作ってください。
  - 書式を統一してください。
  - ほどほどの長さで改行をしてください。
  - 出力を一まとまりと認識できるように箇条書きでインデントしてください。
  - 項目間に無用な改行を入れないでください。

  ## Format
  ## 要点
  1. 要点1
  ## 検索用タグ:
  タグ1,タグ2

  ## 例
  ## 要点
  1. 広告効果の多角的な「測定」の必要性: 近年のプライバシー保護強化により、従来のデータ計測が困難に。バンダイナムコエンターテインメント(BNEI)では、MMMやCausalImpactなどの手法を用い、多角的に広告効果を測定することで、変化への対応と意思決定を可能にしている。
  1. MMMによる包括的な効果測定: 独自のMMMを開発し、オンライン・オフラインを含む多様なプロモーション施策のインストール数への貢献度を分析。施策間相互作用も考慮した予算配分や、予測値と実測値の誤差が少ない高精度なモデル構築を実現。
  1. CausalImpactによる認知施策の効果検証: 従来、懐疑的な見方があった認知施策の効果を、CausalImpactを用いた分析により定量化。YouTube広告配信によるインストール数の純増や、ランディングページへの遷移率向上を実証し、認知施策の貢献度を明確化。
  1. iOSアプリ広告における「推定ROAS」の活用: ATT導入によるiOSアプリ広告の効果測定の課題に対し、「推定ROAS」を開発・運用。従来のROASに近い数値を算出することで、iOSアプリキャンペーンの出稿タイトル数増加とROAS目標達成を実現。
  1. 多角的な検証による組織風土の醸成: MMM、CausalImpact、「推定ROAS」といった多角的な検証体制の構築により、社内のデータに基づいた意思決定を促進。データドリブンなマーケティングへの意識改革を推進し、組織全体の「測定」に対する意識向上を実現。
  ## 検索用タグ: 広告効果測定, MMM, CausalImpact, 推定ROAS, アプリビジネス, プライバシー保護, ATT, データドリブン, バンダイナムコエンターテインメント
  """

  genai.configure(api_key=api_key)
  prompt = template.replace("<text_data>", "\n".join(extracted_text))
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content(
      prompt,
      generation_config={
          "temperature": 0.7,
          "max_output_tokens": 100000,
      },
      request_options={
          "timeout": 60
      }
  )
  time.sleep(2)
  return response.text

def add_info(summary, title, url):
  summary = f"# タイトル: {title}\n## URL: {url}\n{summary.strip()}\n---"
  print(summary)
  return summary

# Streamlitアプリのタイトルを設定
st.title("サマリーの出力 📚")

st.markdown('---')
st.markdown(
"""
URLのリスト(txtファイル)に順番にアクセスし、指定したClass Nameの箇所を抜粋してGeminiで要約した結果をテキストファイルにまとめます。
個々のURLは改行で区切られている必要があります。
""")
st.markdown('---')

# URLとキーワードの入力
uploaded_file = st.file_uploader("txtファイルを選択してください", type='txt')
class_name = st.text_input("URLのページに共通する、抽出したい部分のclass nameを指定してください", value=' page-content--detail')
api_key = st.text_input("GeminiのAPI Keyを入力してください")
summarized_text = []

# 検索ボタン
if st.button("Summarize"):
  if uploaded_file is not None and class_name and api_key:
    urls = url_list_from_txt(uploaded_file)
    for url in urls:
      extracted_text = get_text_by_class(url, class_name)
      st.write(extracted_text)
      if extracted_text is not None:
        title = get_title_from_url(url)
        summary = gemini(extracted_text, api_key)
        summary = add_info(summary, title, url)
        summarized_text.append(summary)
        st.markdown(summary)
      continue
    txt_data = "\n".join(summarized_text)
    st.download_button(
      label="Download txt file",
      data=txt_data,
      file_name="summarized.txt",
      mime="text/plain",
      )
  else:
    st.warning("フォームを全て入力してください")