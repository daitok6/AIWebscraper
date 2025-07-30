import streamlit as st
import pandas as pd
import json
from datetime import datetime
from scrape import scrape_website, split_dom_content
from parse import parse_with_ollama

# ページ設定
st.set_page_config(
    page_title="AI Webスクレイパー",
    page_icon="🕷️",
    layout="wide"
)

# セッション状態の初期化
if 'first_time' not in st.session_state:
    st.session_state.first_time = True
if 'scraping_history' not in st.session_state:
    st.session_state.scraping_history = []
if 'saved_templates' not in st.session_state:
    st.session_state.saved_templates = {
        "商品情報": "商品名と価格を抽出してください",
        "連絡先": "メールアドレスと電話番号を抽出してください",
        "記事タイトル": "記事のタイトルと要約を抽出してください",
        "テーブルデータ": "テーブルの内容を構造化して抽出してください"
    }

st.title("🕷️ AI Webスクレイパー")
st.markdown("---")

# サイドバー - モデル選択とテンプレートライブラリ
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
    
    st.markdown("---")
    st.header("📚 テンプレートライブラリ")
    
    # テンプレート選択
    template_options = list(st.session_state.saved_templates.keys()) + ["カスタム"]
    selected_template = st.selectbox("テンプレートを選択:", template_options)
    
    if selected_template == "カスタム":
        parse_description = st.text_area(
            "カスタムプロンプト:",
            placeholder="例: 商品名と価格を抽出してください",
            height=100
        )
    else:
        parse_description = st.session_state.saved_templates[selected_template]
        st.text_area("選択されたテンプレート:", value=parse_description, height=100, disabled=True)
    
    # 新しいテンプレートの保存
    st.markdown("---")
    st.header("💾 テンプレート保存")
    new_template_name = st.text_input("テンプレート名:")
    new_template_content = st.text_area("テンプレート内容:", height=80)
    
    if st.button("💾 保存", key="save_template"):
        if new_template_name and new_template_content:
            st.session_state.saved_templates[new_template_name] = new_template_content
            st.success(f"✅ '{new_template_name}' を保存しました!")
            st.rerun()
    
    # 結果履歴
    st.markdown("---")
    st.header("📚 最近のスクレイピング")
    if st.session_state.scraping_history:
        for i, history in enumerate(st.session_state.scraping_history[-5:]):  # 最新5件
            if st.sidebar.button(f"📄 {history['url'][:25]}...", key=f"history_{i}"):
                st.session_state.dom_content = history['content']
                st.session_state.website = history['url']
                st.rerun()
    else:
        st.sidebar.info("まだスクレイピング履歴がありません")

# インタラクティブチュートリアル
if st.session_state.first_time:
    st.info("🎓 **AI Webスクレイパーへようこそ！** クイックツアーを始めましょう。")
    
    tutorial_step = st.session_state.get('tutorial_step', 0)
    
    if tutorial_step == 0:
        st.success("**ステップ 1/4: AIモデル選択**")
        st.write("サイドバーから使用したいAIモデルを選択してください。")
        st.write("- **TinyLlama**: 高速処理、シンプルなタスクに最適")
        st.write("- **Phi-2**: バランス型、一般的な用途に適している")
        st.write("- **DeepSeek R1**: 高精度、複雑なデータ抽出に最適")
        
        if st.button("次へ →", key="tutorial_next_1"):
            st.session_state.tutorial_step = 1
            st.rerun()
    
    elif tutorial_step == 1:
        st.success("**ステップ 2/4: URL入力**")
        st.write("スクレイピングしたいウェブサイトのURLを入力してください。")
        st.write("例: https://example.com")
        
        if st.button("← 戻る", key="tutorial_back_1"):
            st.session_state.tutorial_step = 0
            st.rerun()
        if st.button("次へ →", key="tutorial_next_2"):
            st.session_state.tutorial_step = 2
            st.rerun()
    
    elif tutorial_step == 2:
        st.success("**ステップ 3/4: プロンプト入力**")
        st.write("抽出したいデータを自然言語で説明してください。")
        st.write("例:")
        st.write("- 「商品名と価格を抽出してください」")
        st.write("- 「メールアドレスと電話番号を抽出してください」")
        st.write("- 「記事のタイトルと要約を抽出してください」")
        
        if st.button("← 戻る", key="tutorial_back_2"):
            st.session_state.tutorial_step = 1
            st.rerun()
        if st.button("次へ →", key="tutorial_next_3"):
            st.session_state.tutorial_step = 3
            st.rerun()
    
    elif tutorial_step == 3:
        st.success("**ステップ 4/4: 結果確認**")
        st.write("スクレイピングとAI解析が完了すると、結果が表示されます。")
        st.write("結果は履歴に保存され、後で再利用できます。")
        
        if st.button("← 戻る", key="tutorial_back_3"):
            st.session_state.tutorial_step = 2
            st.rerun()
        if st.button("🎉 チュートリアル完了", key="tutorial_complete"):
            st.session_state.first_time = False
            st.rerun()

# メインコンテンツ
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌐 ウェブサイトスクレイピング")
    
    # URL入力
    website = st.text_input("スクレイピングしたいURLを入力してください:")
    
    if st.button("🔍 スクレイプ!", type="primary"):
        if website:
            # プログレスバー付きスクレイピング
            with st.spinner("ウェブサイトをスクレイピング中..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # ステップ1: スクレイピング開始
                    status_text.text("🌐 ウェブサイトにアクセス中...")
                    progress_bar.progress(25)
                    
                    dom_content = scrape_website(website)
                    progress_bar.progress(50)
                    
                    if dom_content:
                        # ステップ2: コンテンツ処理
                        status_text.text("📄 コンテンツを処理中...")
                        progress_bar.progress(75)
                        
                        # 履歴に保存
                        history_entry = {
                            'url': website,
                            'content': dom_content,
                            'timestamp': datetime.now().isoformat(),
                            'model': selected_model
                        }
                        st.session_state.scraping_history.append(history_entry)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ 完了!")
                        
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
                finally:
                    # プログレスバーをクリア
                    progress_bar.empty()
                    status_text.empty()
        else:
            st.warning("⚠️ URLを入力してください。")

with col2:
    st.subheader("📊 データ抽出")
    
    if 'dom_content' in st.session_state and st.session_state.dom_content:
        st.success("✅ スクレイピング済み")
        
        if st.button("🤖 AIで抽出", type="secondary"):
            if parse_description:
                # プログレスバー付きAI解析
                with st.spinner(f"AI ({selected_model}) でデータを抽出中..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # ステップ1: コンテンツ分割
                        status_text.text("📝 コンテンツを分割中...")
                        progress_bar.progress(25)
                        
                        dom_chunks = split_dom_content(st.session_state.dom_content)
                        progress_bar.progress(50)
                        
                        # ステップ2: AI解析
                        status_text.text(f"🤖 AI ({selected_model}) で解析中...")
                        progress_bar.progress(75)
                        
                        extracted_data = parse_with_ollama(dom_chunks, parse_description, selected_model)
                        progress_bar.progress(100)
                        
                        if extracted_data:
                            status_text.text("✅ 抽出完了!")
                            
                            st.success("✅ データ抽出完了!")
                            
                            # 抽出結果表示
                            st.subheader("📋 抽出結果")
                            st.text_area("抽出されたデータ:", value=extracted_data, height=200, disabled=True)
                            
                            # データプレビュー
                            st.subheader("👀 データプレビュー")
                            preview_text = extracted_data[:300] + "..." if len(extracted_data) > 300 else extracted_data
                            st.info(f"**プレビュー:** {preview_text}")
                            
                            # 統計情報
                            col_stats1, col_stats2, col_stats3 = st.columns(3)
                            with col_stats1:
                                st.metric("抽出文字数", len(extracted_data))
                            with col_stats2:
                                st.metric("使用モデル", selected_model)
                            with col_stats3:
                                st.metric("処理時間", "完了")
                            
                        else:
                            st.warning("⚠️ データが見つかりませんでした。プロンプトを変更してみてください。")
                            
                    except Exception as e:
                        st.error(f"❌ AI解析中にエラーが発生しました: {str(e)}")
                        st.info("💡 ヒント: Ollamaが起動しているか確認してください。")
                    finally:
                        # プログレスバーをクリア
                        progress_bar.empty()
                        status_text.empty()
            else:
                st.warning("⚠️ 抽出したいデータの説明を入力してください。")
    else:
        st.info("ℹ️ まずURLをスクレイピングしてください。")

# フッター
st.markdown("---")
st.markdown("🕷️ **AI Webスクレイパー** - インテリジェントなウェブデータ抽出ツール")

# チュートリアルリセットボタン（開発用）
if st.sidebar.button("🔄 チュートリアルリセット"):
    st.session_state.first_time = True
    st.session_state.tutorial_step = 0
    st.rerun()