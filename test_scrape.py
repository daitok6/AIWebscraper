import unittest
from unittest.mock import Mock, patch, MagicMock
from scrape import scrape_website, clean_html_content, split_dom_content

class TestScrapeFunctions(unittest.TestCase):
    
    def test_clean_html_content(self):
        """HTMLコンテンツのクリーンアップテスト"""
        # テスト用HTML
        test_html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <script>alert('test');</script>
                <style>body { color: red; }</style>
                <h1>Hello World</h1>
                <p>This is a test paragraph.</p>
                <div>More content here</div>
            </body>
        </html>
        """
        
        result = clean_html_content(test_html)
        
        # スクリプトとスタイルが削除されていることを確認
        self.assertNotIn("alert('test')", result)
        self.assertNotIn("body { color: red; }", result)
        
        # テキストコンテンツが含まれていることを確認
        self.assertIn("Hello World", result)
        self.assertIn("This is a test paragraph", result)
        self.assertIn("More content here", result)
    
    def test_split_dom_content(self):
        """DOMコンテンツの分割テスト"""
        # テスト用コンテンツ
        test_content = "A" * 10000  # 10000文字のコンテンツ
        
        result = split_dom_content(test_content, max_length=3000)
        
        # 分割されていることを確認
        self.assertGreater(len(result), 1)
        
        # 各チャンクが指定された最大長以下であることを確認
        for chunk in result:
            self.assertLessEqual(len(chunk), 3000)
        
        # 元のコンテンツが保持されていることを確認
        combined = "".join(result)
        self.assertEqual(combined, test_content)
    
    @patch('scrape.webdriver.Chrome')
    def test_scrape_website_success(self, mock_chrome):
        """スクレイピング成功のテスト"""
        # モックの設定
        mock_driver = Mock()
        mock_driver.page_source = "<html><body>Test content</body></html>"
        mock_chrome.return_value = mock_driver
        
        with patch('scrape.Service'):
            result = scrape_website("https://example.com")
            
            # 結果が返されることを確認
            self.assertIsNotNone(result)
            self.assertIn("Test content", result)
    
    @patch('scrape.webdriver.Chrome')
    def test_scrape_website_timeout(self, mock_chrome):
        """タイムアウトエラーのテスト"""
        from selenium.common.exceptions import TimeoutException
        
        # モックの設定
        mock_driver = Mock()
        mock_driver.get.side_effect = TimeoutException("Timeout")
        mock_chrome.return_value = mock_driver
        
        with patch('scrape.Service'):
            with self.assertRaises(Exception) as context:
                scrape_website("https://example.com")
            
            self.assertIn("タイムアウト", str(context.exception))

if __name__ == '__main__':
    unittest.main() 