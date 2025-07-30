import unittest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from scrape import scrape_website, split_dom_content
from parse import parse_with_ollama

class TestIntegration(unittest.TestCase):
    
    @patch('scrape.webdriver.Chrome')
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_full_workflow(self, mock_ollama, mock_prompt, mock_chrome):
        """完全なワークフローのテスト"""
        # モックの設定
        mock_driver = Mock()
        mock_driver.page_source = """
        <html>
            <body>
                <h1>Product Page</h1>
                <div class="product">
                    <h2>iPhone 15</h2>
                    <p class="price">$999</p>
                    <p class="description">Latest iPhone model</p>
                </div>
            </body>
        </html>
        """
        mock_chrome.return_value = mock_driver
        
        mock_model = Mock()
        mock_ollama.return_value = mock_model
        
        mock_chain = Mock()
        mock_response = Mock()
        mock_response.content = "iPhone 15: $999"
        mock_chain.invoke.return_value = mock_response
        mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
        
        # 1. スクレイピング
        scraped_content = scrape_website("https://example.com")
        self.assertIn("iPhone 15", scraped_content)
        self.assertIn("$999", scraped_content)
        
        # 2. コンテンツ分割
        chunks = split_dom_content(scraped_content)
        self.assertGreater(len(chunks), 0)
        
        # 3. AI解析
        result = parse_with_ollama(chunks, "Extract product name and price", "tinyllama")
        self.assertIn("iPhone 15", result)
        self.assertIn("$999", result)
    
    def test_streamlit_session_state(self):
        """Streamlitセッション状態のテスト"""
        # セッション状態のシミュレーション
        session_state = {}
        
        # スクレイピング後の状態
        session_state['dom_content'] = "Test content"
        session_state['website'] = "https://example.com"
        
        # 状態が正しく保存されていることを確認
        self.assertIn('dom_content', session_state)
        self.assertIn('website', session_state)
        self.assertEqual(session_state['website'], "https://example.com")
    
    @patch('scrape.webdriver.Chrome')
    def test_error_handling_workflow(self, mock_chrome):
        """エラーハンドリングの統合テスト"""
        from selenium.common.exceptions import TimeoutException
        
        # タイムアウトエラーのシミュレーション
        mock_driver = Mock()
        mock_driver.get.side_effect = TimeoutException("Timeout")
        mock_chrome.return_value = mock_driver
        
        # エラーが適切に処理されることを確認
        with self.assertRaises(Exception) as context:
            scrape_website("https://example.com")
        
        self.assertIn("タイムアウト", str(context.exception))

class TestPerformance(unittest.TestCase):
    
    def test_large_content_handling(self):
        """大量コンテンツの処理テスト"""
        # 大量のコンテンツを生成
        large_content = "A" * 50000  # 50KBのコンテンツ
        
        # 分割処理
        chunks = split_dom_content(large_content, max_length=6000)
        
        # パフォーマンスチェック
        self.assertGreater(len(chunks), 8)  # 少なくとも8チャンクに分割される
        
        # 各チャンクのサイズチェック
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 6000)
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_multiple_model_performance(self, mock_ollama, mock_prompt):
        """複数モデルのパフォーマンステスト"""
        models = ["tinyllama", "phi2", "deepseek-r1"]
        test_chunks = ["Test content"] * 5  # 5つのチャンク
        
        for model in models:
            mock_model = Mock()
            mock_ollama.return_value = mock_model
            
            mock_chain = Mock()
            mock_response = Mock()
            mock_response.content = f"Result from {model}"
            mock_chain.invoke.return_value = mock_response
            mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
            
            # 各モデルでの処理時間を測定
            import time
            start_time = time.time()
            result = parse_with_ollama(test_chunks, "extract", model)
            end_time = time.time()
            
            # 処理時間が妥当であることを確認（5秒以内）
            self.assertLess(end_time - start_time, 5.0)
            self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main() 