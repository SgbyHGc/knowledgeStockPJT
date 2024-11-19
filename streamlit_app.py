import streamlit as st
st.title("使い方")
st.write("""
URL List Maker: URLのページに記載されているリンクを再帰的に辿ってURLのリストを作成します。
Class Name Finder: URLを指定したページをキーワード検索し、該当箇所のClass Nameを表示します。
Summarizer: URLのリスト(txtファイル)に順番にアクセスし、指定したClass Nameの箇所を抜粋してGeminiで要約した結果をテキストファイルにまとめます。

""")