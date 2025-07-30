#!/bin/bash

echo "🧪 AI Web Scraper テストスイート"
echo "================================"

# 仮想環境のアクティベート
if [ -d "ai" ]; then
    source ai/bin/activate
    echo "✅ 仮想環境をアクティベートしました"
else
    echo "❌ 仮想環境が見つかりません"
    exit 1
fi

# テストオプション
case "$1" in
    "unit")
        echo "🔬 ユニットテストを実行中..."
        echo ""
        echo "📊 スクレイピング機能のテスト:"
        python -m unittest test_scrape.py -v
        echo ""
        echo "🤖 AI解析機能のテスト:"
        python -m unittest test_parse.py -v
        ;;
    "integration")
        echo "🔗 統合テストを実行中..."
        python -m unittest test_integration.py -v
        ;;
    "performance")
        echo "⚡ パフォーマンステストを実行中..."
        python -m unittest test_integration.TestPerformance -v
        ;;
    "all")
        echo "🚀 全テストを実行中..."
        echo ""
        echo "📊 スクレイピング機能のテスト:"
        python -m unittest test_scrape.py -v
        echo ""
        echo "🤖 AI解析機能のテスト:"
        python -m unittest test_parse.py -v
        echo ""
        echo "🔗 統合テスト:"
        python -m unittest test_integration.py -v
        ;;
    "coverage")
        echo "📈 カバレッジテストを実行中..."
        if ! command -v coverage &> /dev/null; then
            echo "📦 coverageをインストール中..."
            pip install coverage
        fi
        coverage run -m unittest discover
        coverage report
        coverage html
        echo "📊 カバレッジレポートを生成しました: htmlcov/index.html"
        ;;
    *)
        echo "使用方法: $0 [unit|integration|performance|all|coverage]"
        echo ""
        echo "オプション:"
        echo "  unit        - ユニットテストのみ実行"
        echo "  integration - 統合テストのみ実行"
        echo "  performance - パフォーマンステストのみ実行"
        echo "  all         - 全テストを実行"
        echo "  coverage    - カバレッジテストを実行"
        echo ""
        echo "例:"
        echo "  $0 unit      # ユニットテストのみ"
        echo "  $0 all       # 全テスト"
        echo "  $0 coverage  # カバレッジテスト"
        ;;
esac

echo ""
echo "✅ テスト完了!" 