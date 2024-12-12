from pet_registration_scraper import PetRegistrationScraper

# 創建爬蟲實例
scraper = PetRegistrationScraper()

# 獲取2024年1月的狗隻登記數據
df = scraper.get_registration_data(
    start_date="2024-01-01",
    end_date="2024-01-31",
    animal_type=0  # 0代表狗，1代表貓
)

# 保存為CSV檔案
scraper.save_to_csv(df, "dog_registration_data.csv")