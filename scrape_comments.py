import json
from openai import OpenAI

from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SeleniumFetcher:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0"
        )
        self.options.add_argument("--headless")  # Keep headless for performance
        self.service = Service(ChromeDriverManager().install())
        self.service.start()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def fetch_comments(self, link):
        try:
            # Open the webpage
            self.driver.get(link)
            time.sleep(2)  # Allow the page to load fully
            # Find all comments using the class name
            comments_elements = self.driver.find_elements(By.CLASS_NAME, "Comments__StyledComments-dzzyvm-0.gRjWel")
            comments = [comment.text for comment in comments_elements]
            return comments
        except Exception as e:
            print(f"Error occurred for {link}: {e}")
            return []
    
    def close(self):
        self.driver.quit()




def scrape_professor_comments(prof_list):
    scraper = SeleniumFetcher()
    all_comments = {}

    try:
        for prof in prof_list:
            if prof['legacyId'] and prof['numRatings'] > 2:
                prof_id = prof['legacyId']
                link = f"https://www.ratemyprofessors.com/professor/{prof_id}"
                print(f"Scraping comments for professor ID: {prof_id}")
                comments = scraper.fetch_comments(link)
                all_comments[prof_id] = comments
    finally:
        scraper.close()  # Ensure the browser is properly closed
    
    return all_comments



# Load the professor list
with open("rmp_prof_clean.json", 'r') as f:
    prof_list = json.load(f)

# Scrape comments for professors
comments_by_prof = scrape_professor_comments(prof_list)

# Save the results to a file
with open("comments_by_prof.json", "w") as f:
    json.dump(comments_by_prof, f, indent=4)

print("Scraping complete. Comments saved to 'comments_by_prof.json'.")