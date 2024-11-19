import streamlit as st
st.title("このページについて 📖")
st.markdown("""
---
NotebookLM用データソースを作ります。         
---
### URL List Maker
URLのページに記載されているリンクを辿ってURLのリストを作成します。
### Class Name Finder
URLを指定したページをキーワード検索し、該当箇所のdivタグのClass Nameを表示します。
### Summarizer
URLのリスト(txtファイル)に順番にアクセスし、指定したClass Nameの箇所を抜粋してGeminiで要約した結果をテキストファイルにまとめます。
""")