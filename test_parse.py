import unittest
from unittest.mock import Mock, patch, MagicMock
from parse import parse_with_ollama

class TestParseFunctions(unittest.TestCase):
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_parse_with_ollama_success(self, mock_ollama, mock_prompt):
        """AI解析成功のテスト"""
        # モックの設定
        mock_model = Mock()
        mock_ollama.return_value = mock_model
        
        mock_chain = Mock()
        mock_response = Mock()
        mock_response.content = "Extracted data: Test result"
        mock_chain.invoke.return_value = mock_response
        mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
        
        # テストデータ
        test_chunks = ["This is test content with some data to extract"]
        test_description = "Extract the word 'data'"
        
        result = parse_with_ollama(test_chunks, test_description, "tinyllama")
        
        # 結果が返されることを確認
        self.assertIsNotNone(result)
        self.assertIn("Test result", result)
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_parse_with_ollama_empty_result(self, mock_ollama, mock_prompt):
        """空の結果のテスト"""
        # モックの設定
        mock_model = Mock()
        mock_ollama.return_value = mock_model
        
        mock_chain = Mock()
        mock_response = Mock()
        mock_response.content = ""
        mock_chain.invoke.return_value = mock_response
        mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
        
        # テストデータ
        test_chunks = ["This is test content"]
        test_description = "Extract non-existent data"
        
        result = parse_with_ollama(test_chunks, test_description, "tinyllama")
        
        # 空の結果が返されることを確認
        self.assertEqual(result, "")
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_parse_with_ollama_multiple_chunks(self, mock_ollama, mock_prompt):
        """複数チャンクの処理テスト"""
        # モックの設定
        mock_model = Mock()
        mock_ollama.return_value = mock_model
        
        mock_chain = Mock()
        mock_response1 = Mock()
        mock_response1.content = "Result 1"
        mock_response2 = Mock()
        mock_response2.content = ""
        mock_response3 = Mock()
        mock_response3.content = "Result 3"
        mock_chain.invoke.side_effect = [mock_response1, mock_response2, mock_response3]
        mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
        
        # テストデータ
        test_chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
        test_description = "Extract results"
        
        result = parse_with_ollama(test_chunks, test_description, "tinyllama")
        
        # 複数の結果が結合されていることを確認
        self.assertIn("Result 1", result)
        self.assertIn("Result 3", result)
        self.assertNotIn("Result 2", result)  # 空の結果は含まれない
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_parse_with_ollama_error_handling(self, mock_ollama, mock_prompt):
        """エラーハンドリングのテスト"""
        # モックの設定
        mock_model = Mock()
        mock_ollama.return_value = mock_model
        
        mock_chain = Mock()
        mock_chain.invoke.side_effect = Exception("AI model error")
        mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
        
        # テストデータ
        test_chunks = ["Test content"]
        test_description = "Extract data"
        
        result = parse_with_ollama(test_chunks, test_description, "tinyllama")
        
        # エラー時に空の結果が返されることを確認
        self.assertEqual(result, "")
    
    @patch('parse.ChatPromptTemplate')
    @patch('parse.OllamaLLM')
    def test_parse_with_ollama_different_models(self, mock_ollama, mock_prompt):
        """異なるモデルのテスト"""
        models = ["tinyllama", "phi2", "deepseek-r1"]
        
        for model in models:
            mock_model = Mock()
            mock_ollama.return_value = mock_model
            
            mock_chain = Mock()
            mock_response = Mock()
            mock_response.content = f"Result from {model}"
            mock_chain.invoke.return_value = mock_response
            mock_prompt.from_template.return_value.__or__ = lambda self, model: mock_chain
            
            result = parse_with_ollama(["test"], "extract", model)
            
            # 各モデルが正しく呼び出されることを確認
            mock_ollama.assert_called_with(model=model)
            self.assertIn(model, result)

if __name__ == '__main__':
    unittest.main() 