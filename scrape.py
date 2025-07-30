import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time

def scrape_website(website):
    """ウェブサイトをスクレイピング"""
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
