import streamlit as st
from scrape import scrape_website, split_dom_content
from parse import parse_with_ollama

st.title("🕷️ AI Webスクレイパー")
st.markdown("---")

# サイドバー - モデル選択
with st.sidebar:
    st.header("🤖 AIモデル選択")
    
    # 利用可能なモデル
    available_models = {
        "tinyllama": "TinyLlama (高速)",
        "phi2": "Phi-2 (バランス)",
        "deepseek-r1": "DeepSeek R1 (高精度)"
    }
    
    selected_model = st.selectbox(
        "AIモデルを選択:",
        list(available_models.keys()),
        format_func=lambda x: available_models[x]
    )
    
    st.info(f"選択中: {available_models[selected_model]}")

# メインコンテンツ
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌐 ウェブサイトスクレイピング")
    
    # URL入力
    website = st.text_input("スクレイピングしたいURLを入力してください:")
    
    if st.button("🔍 スクレイプ!", type="primary"):
        if website:
            with st.spinner("ウェブサイトをスクレイピング中..."):
                try:
                    # スクレイピング実行
                    dom_content = scrape_website(website)
                    if dom_content:
                        st.success("✅ スクレイピング完了!")
                        
                        # コンテンツ表示
                        with st.expander("📄 抽出されたコンテンツ", expanded=False):
                            st.text_area("DOMコンテンツ:", value=dom_content, height=200, disabled=True)
                        
                        # セッション状態に保存
                        st.session_state.dom_content = dom_content
                        st.session_state.website = website
                    else:
                        st.error("❌ スクレイピングに失敗しました。URLを確認してください。")
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
        else:
            st.warning("⚠️ URLを入力してください。")

with col2:
    st.subheader("📊 データ抽出")
    
    # カスタムプロンプト入力
    parse_description = st.text_area(
        "抽出したいデータを説明してください:",
        placeholder="例: 商品名と価格を抽出してください",
        height=150
    )
    
    if 'dom_content' in st.session_state and st.session_state.dom_content:
        st.success("✅ スクレイピング済み")
        
        if st.button("🤖 AIで抽出", type="secondary"):
            if parse_description:
                with st.spinner(f"AI ({selected_model}) でデータを抽出中..."):
                    try:
                        # DOMコンテンツを分割
                        dom_chunks = split_dom_content(st.session_state.dom_content)
                        
                        # AI解析実行
                        extracted_data = parse_with_ollama(dom_chunks, parse_description, selected_model)
                        
                        if extracted_data:
                            st.success("✅ データ抽出完了!")
                            
                            # 抽出結果表示
                            st.subheader("📋 抽出結果")
                            st.text_area("抽出されたデータ:", value=extracted_data, height=200, disabled=True)
                            
                        else:
                            st.warning("⚠️ データが見つかりませんでした。プロンプトを変更してみてください。")
                            
                    except Exception as e:
                        st.error(f"❌ AI解析中にエラーが発生しました: {str(e)}")
                        st.info("💡 ヒント: Ollamaが起動しているか確認してください。")
            else:
                st.warning("⚠️ 抽出したいデータの説明を入力してください。")
    else:
        st.info("ℹ️ まずURLをスクレイピングしてください。")

# フッター
st.markdown("---")
st.markdown("🕷️ **AI Webスクレイパー** - インテリジェントなウェブデータ抽出ツール")