import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
import requests
import os

def scrape_website(website):
    """ウェブサイトをスクレイピング - クラウド対応版"""
    
    # クラウド環境かどうかをチェック
    is_cloud = os.environ.get('STREAMLIT_SERVER_PORT') is not None
    
    if is_cloud:
        # クラウド環境ではrequests + BeautifulSoupを使用
        return scrape_with_requests(website)
    else:
        # ローカル環境ではSeleniumを使用
        return scrape_with_selenium(website)

def scrape_with_requests(website):
    """requests + BeautifulSoupを使用したスクレイピング（クラウド対応）"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(website, headers=headers, timeout=30)
        response.raise_for_status()
        
        # HTMLをテキストに変換
        cleaned_content = clean_html_content(response.text)
        return cleaned_content
        
    except requests.RequestException as e:
        raise Exception(f"リクエストエラー: {str(e)}")
    except Exception as e:
        raise Exception(f"スクレイピングエラー: {str(e)}")

def scrape_with_selenium(website):
    """Seleniumを使用したスクレイピング（ローカル環境）"""
    driver = None
    try:
        # Chromeドライバーの設定
        chrome_driver_path = "./chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # ドライバー起動
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.set_page_load_timeout(30)
        
        # ページ読み込み
        driver.get(website)
        
        # ページが完全に読み込まれるまで待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # JavaScriptの実行を待つ
        time.sleep(2)
        
        html = driver.page_source
        
        # HTMLをテキストに変換
        cleaned_content = clean_html_content(html)
        
        return cleaned_content
        
    except TimeoutException:
        raise Exception("ページの読み込みがタイムアウトしました。")
    except WebDriverException as e:
        raise Exception(f"ブラウザエラー: {str(e)}")
    except Exception as e:
        raise Exception(f"スクレイピングエラー: {str(e)}")
    finally:
        if driver:
            driver.quit()

def clean_html_content(html_content):
    """HTMLコンテンツをクリーンアップしてテキストを抽出"""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # スクリプトとスタイルを削除
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        
        # テキストを抽出してクリーンアップ
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        
        return cleaned_content
    except Exception as e:
        return html_content  # エラーの場合は元のHTMLを返す

def split_dom_content(dom_content, max_length=6000):
    """DOMコンテンツをチャンクに分割"""
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
