#!/bin/bash

echo "🚀 AI Web Scraper を起動中..."

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境の存在確認
if [ ! -d "ai" ]; then
    echo "❌ 仮想環境が見つかりません。"
    echo "以下のコマンドでセットアップしてください："
    echo "python -m venv ai"
    echo "source ai/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# ChromeDriverの存在確認
if [ ! -f "chromedriver" ]; then
    echo "❌ ChromeDriverが見つかりません。"
    echo "ChromeDriverをダウンロードしてプロジェクトルートに配置してください。"
    exit 1
fi

# ChromeDriverに実行権限を付与
chmod +x chromedriver

# 仮想環境をアクティベートしてアプリを起動
echo "✅ アプリを起動中..."
source ai/bin/activate && streamlit run main.py 