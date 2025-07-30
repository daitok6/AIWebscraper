# AI Webスクレイパー

AIを活用したインテリジェントなウェブスクレイピングアプリケーションです。Streamlitで構築され、Ollamaを使用してウェブサイトから特定のデータを自動抽出します。

## 🌟 主な機能

- **🌐 ウェブスクレイピング**: SeleniumとBeautifulSoupを使用した高精度なコンテンツ抽出
- **🤖 AI駆動解析**: Ollama（ローカルAI）を使用したインテリジェントなデータ抽出
- **🎯 モデル選択**: 3つのAIモデルから選択可能（TinyLlama、Phi-2、DeepSeek R1）
- **💬 カスタムプロンプト**: 自然言語で抽出したいデータを指定
- **🧪 包括的テスト**: ユニットテスト、統合テスト、パフォーマンステスト

## 📋 前提条件

アプリケーションを実行する前に、以下がインストールされていることを確認してください：

- **Python 3.8+**
- **Git**
- **Chrome ブラウザ**（Selenium用）
- **Ollama**（ローカルAI処理用）

### Ollamaのインストール

1. [https://ollama.ai](https://ollama.ai) にアクセス
2. お使いのOS用のOllamaをダウンロード・インストール
3. 必要なAIモデルをダウンロード：

```bash
# 3つのモデルをダウンロード
ollama pull tinyllama
ollama pull phi2
ollama pull deepseek-r1
```

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/daitok6/AIWebscraper.git
cd AIWebscraper
```

### 2. 仮想環境の作成とアクティベート

```bash
python -m venv ai
source ai/bin/activate  # macOS/Linux
# または
ai\Scripts\activate     # Windows
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. ChromeDriverのダウンロード

ChromeDriverをダウンロードしてプロジェクトルートに配置してください：

```bash
# macOSの場合（Homebrew使用）
brew install chromedriver

# または手動でダウンロード
# https://chromedriver.chromium.org/ からダウンロード
```

### 5. Ollamaの起動

```bash
ollama serve
```

## 🎯 使用方法

### アプリケーションの起動

```bash
# 簡単な起動方法
./start.sh

# または手動で起動
source ai/bin/activate
streamlit run main.py
```

### 基本的な使用手順

1. **AIモデル選択**: サイドバーから使用したいAIモデルを選択
   - **TinyLlama (高速)**: シンプルな抽出タスクに最適
   - **Phi-2 (バランス)**: 一般的な用途に適したバランス型
   - **DeepSeek R1 (高精度)**: 複雑なデータ抽出に最適

2. **URL入力**: スクレイピングしたいウェブサイトのURLを入力

3. **スクレイピング実行**: 「🔍 スクレイプ!」ボタンをクリック

4. **プロンプト入力**: 抽出したいデータを自然言語で説明
   - 例：「商品名と価格を抽出してください」
   - 例：「メールアドレスと電話番号を抽出してください」

5. **AI解析実行**: 「🤖 AIで抽出」ボタンをクリック

6. **結果確認**: 抽出されたデータを確認

## 🧪 テストフレームワーク

このプロジェクトには包括的なテストフレームワークが含まれています。

### テストの種類

#### **ユニットテスト** (`test_scrape.py`, `test_parse.py`)
- 個別の機能コンポーネントをテスト
- スクレイピング機能、AI解析機能の動作確認
- エラーハンドリングの検証

#### **統合テスト** (`test_integration.py`)
- 完全なワークフローのテスト
- スクレイピング → 解析 → 抽出の全プロセス
- セッション状態管理の確認

#### **パフォーマンステスト**
- 大量コンテンツの処理能力
- 複数AIモデルの性能比較
- レスポンス時間の測定

### テストの実行方法

```bash
# 全テストを実行
./run_tests.sh all

# 特定のテストタイプのみ実行
./run_tests.sh unit        # ユニットテストのみ
./run_tests.sh integration # 統合テストのみ
./run_tests.sh performance # パフォーマンステストのみ

# カバレッジレポート生成
./run_tests.sh coverage
```

### テストの詳細

#### **スクレイピングテスト**
```bash
# HTMLコンテンツのクリーンアップ
# コンテンツ分割機能
# エラーハンドリング（タイムアウト、ブラウザエラー）
python -m unittest test_scrape.py -v
```

#### **AI解析テスト**
```bash
# 3つのAIモデルの動作確認
# 複数チャンクの処理
# エラー時の適切な処理
python -m unittest test_parse.py -v
```

#### **統合テスト**
```bash
# 完全なワークフローの検証
# セッション状態の管理
# エラーシナリオの処理
python -m unittest test_integration.py -v
```

### テストの利点

1. **品質保証**: バグを本番環境前に発見
2. **回帰防止**: 新機能が既存機能を壊さないことを保証
3. **性能監視**: 処理時間と効率性の追跡
4. **モデル検証**: 全3つのAIモデルが正しく動作することを確認
5. **CI/CD対応**: 自動化テストパイプラインに簡単に統合可能

## 📁 プロジェクト構造

```
AiWebscraper/
├── main.py              # Streamlitメインアプリケーション
├── scrape.py            # ウェブスクレイピング機能
├── parse.py             # AI解析機能
├── requirements.txt     # Python依存関係
├── requirements-test.txt # テスト用依存関係
├── start.sh             # アプリケーション起動スクリプト
├── run_tests.sh         # テスト実行スクリプト
├── test_scrape.py       # スクレイピング機能のテスト
├── test_parse.py        # AI解析機能のテスト
├── test_integration.py  # 統合テスト
├── README.md            # このファイル
├── .gitignore           # Git除外設定
├── chromedriver         # Chromeドライバー
└── ai/                  # 仮想環境
```

## 🔧 トラブルシューティング

### よくある問題

#### **ChromeDriverエラー**
```bash
# ChromeDriverに実行権限を付与
chmod +x chromedriver
```

#### **Ollama接続エラー**
```bash
# Ollamaが起動していることを確認
ollama serve

# モデルがダウンロードされていることを確認
ollama list
```

#### **依存関係エラー**
```bash
# 仮想環境を再作成
rm -rf ai
python -m venv ai
source ai/bin/activate
pip install -r requirements.txt
```
