import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

st.title("AI Webスクレイパー")
url = st.text_input("URLを入力: ")

if st.button("Scrape!"):
    st.write("スクレイピング中")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("DOMを表示"):
        st.text_area("DOM内容", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description= st.text_area("抽出したいデータを入力してください")

    if st.button("抽出"):
        if parse_description:
            st.write("抽出中")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)