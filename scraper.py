from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# 🔹 Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # run in background
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔹 Base URL
base_url = "https://www.iplt20.com/stats/2025"

# 🔹 Open the page
driver.get(base_url)
time.sleep(5)  # wait for JS to load

# 🔹 Make output folder
output_folder = "IPL_2025_Stats"
os.makedirs(output_folder, exist_ok=True)

# ----------------------------
# Helper function to scrape a table
def scrape_table(table_selector, csv_name, columns):
    rows = driver.find_elements(By.CSS_SELECTOR, table_selector + " tbody tr")
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(os.path.join(output_folder, csv_name), index=False)
    print(f"✅ Saved {csv_name}")

# ----------------------------
# 1️⃣ Team Rankings
scrape_table(
    "table.standings-table",
    "Team_Rankings_2025.csv",
    ["Position", "Team", "Matches", "Wins", "Losses", "Points", "Net RR"]
)

# 2️⃣ Top Batsmen (Most Runs)
scrape_table(
    "table.top-players__batting",
    "Top_Batsmen_2025.csv",
    ["Position", "Player", "Team", "Matches", "Runs", "Highest", "Average", "Strike Rate", "50s", "100s"]
)

# 3️⃣ Top Bowlers (Most Wickets)
scrape_table(
    "table.top-players__bowling",
    "Top_Bowlers_2025.csv",
    ["Position", "Player", "Team", "Matches", "Wickets", "Best", "Average", "Economy", "Strike Rate"]
)

# ----------------------------
driver.quit()
print("✅ All IPL 2025 stats scraped and saved!")
