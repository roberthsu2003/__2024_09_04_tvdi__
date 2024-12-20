import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json

class PetRegistrationScraper:
    def __init__(self):
        self.base_url = "https://www.pet.gov.tw/Web/O302.aspx"
        
        # 設置 Chrome 選項
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 無頭模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 初始化 WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)  # 增加等待時間
        self.driver.set_window_size(1920, 1080)  # 確保窗口大小足夠

    def format_date(self, date):
        """Convert date to the required format (YYYY/MM/DD)"""
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        return date.strftime("%Y/%m/%d")

    def scroll_to_element(self, element):
        """Scroll element into view"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)

    def get_registration_data(self, start_date, end_date, animal_type=0):
        """
        Get pet registration data for a specific period
        """
        try:
            print("Starting data collection process...")
            
            # 訪問頁面
            self.driver.get(self.base_url)
            print("Page loaded successfully")
            time.sleep(3)  # 等待頁面完全加載

            # 等待並找到日期輸入元素
            print("Setting date range...")
            try:
                # 使用JavaScript直接設置日期值
                formatted_start = self.format_date(start_date)
                formatted_end = self.format_date(end_date)
                
                self.driver.execute_script(
                    f'document.getElementById("txtSDATE").value = "{formatted_start}";'
                )
                self.driver.execute_script(
                    f'document.getElementById("txtEDATE").value = "{formatted_end}";'
                )
                print("Date range set successfully")
            except Exception as e:
                print(f"Error setting dates: {str(e)}")
                raise

            # 選擇動物類型
            print("Selecting animal type...")
            try:
                radio_id = "animal_dog" if animal_type == 0 else "animal_cat"
                animal_radio = self.wait.until(
                    EC.presence_of_element_located((By.ID, radio_id))
                )
                self.scroll_to_element(animal_radio)
                # 使用 JavaScript 點擊
                self.driver.execute_script("arguments[0].click();", animal_radio)
                print("Animal type selected")
            except Exception as e:
                print(f"Error selecting animal type: {str(e)}")
                raise

            # 點擊查詢按鈕
            print("Clicking search button...")
            try:
                search_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-main[data-event='前台_O302_查詢']"))
                )
                self.scroll_to_element(search_button)
                # 使用 JavaScript 點擊
                self.driver.execute_script("arguments[0].click();", search_button)
                print("Search button clicked")
            except Exception as e:
                print(f"Error clicking search button: {str(e)}")
                raise

            # 等待表格加載
            print("Waiting for table to load...")
            time.sleep(5)

            # 獲取表格數據
            print("Extracting table data...")
            try:
                table = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
                )
                
                # 獲取表頭
                headers = []
                header_cells = table.find_elements(By.CSS_SELECTOR, "th")
                for cell in header_cells:
                    header_text = cell.text.split('\n')[0]
                    headers.append(header_text)

                # 獲取數據行
                data = []
                rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = {}
                    for i, cell in enumerate(cells):
                        row_data[headers[i]] = cell.text
                    data.append(row_data)
                
                print(f"Found {len(data)} rows of data")
                
                # 轉換為DataFrame
                df = pd.DataFrame(data)
                return df

            except Exception as e:
                print(f"Error extracting table data: {str(e)}")
                raise

        except Exception as e:
            raise Exception(f"Error during scraping: {str(e)}")
        
        finally:
            print("Closing browser...")
            self.driver.quit()

    def save_to_csv(self, df, filename):
        """Save DataFrame to CSV file"""
        df.to_csv(filename, index=False, encoding='utf-8-sig')

# Example usage
if __name__ == "__main__":
    scraper = PetRegistrationScraper()
    
    try:
        print("Starting scraping process...")
        df = scraper.get_registration_data(
            start_date="2023-01-01",
            end_date="2023-01-31",
            animal_type=1  # 0 for dogs
        )
        
        # Save to CSV
        scraper.save_to_csv(df, "pet_registration_data.csv")
        print("\nData successfully scraped and saved to pet_registration_data.csv")
        print("\nFirst few rows of data:")
        print(df.head())
        
    except Exception as e:
        print(f"Error: {str(e)}")