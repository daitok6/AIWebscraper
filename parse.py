from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time

# AI解析用テンプレート
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_chunks, parse_description, model_name="tinyllama"):
    """AIでデータを解析・抽出 - モデル選択対応"""
    try:
        # 選択されたモデルで初期化
        model = OllamaLLM(model=model_name)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        # 各チャンクを処理
        results = []
        for i, chunk in enumerate(dom_chunks):
            try:
                # AI解析実行
                response = chain.invoke({
                    "dom_content": chunk,
                    "parse_description": parse_description
                })
                
                # LangChainレスポンスからテキストを抽出
                if hasattr(response, 'content'):
                    result = response.content
                elif hasattr(response, 'text'):
                    result = response.text
                else:
                    result = str(response)
                
                if result and result.strip():
                    results.append(result.strip())
                    
            except Exception as chunk_error:
                print(f"チャンク {i+1} の処理中にエラー: {chunk_error}")
                continue
        
        # 結果を結合
        if results:
            return "\n".join(results)
        else:
            return ""
            
    except Exception as e:
        print(f"AI解析エラー: {e}")
        return ""