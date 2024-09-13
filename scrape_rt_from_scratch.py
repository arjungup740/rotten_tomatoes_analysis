import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# options = webdriver.ChromeOptions()
# options.add_argument('--headless') # speed things up?
# driver = webdriver.Chrome(options=options)


# Function to extract scores from a single page
def extract_scores(url):
    try:
        # Open the Rotten Tomatoes page
        driver.get(url)
        
        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

        # JavaScript to directly access the text content
        critics_score_script = """
            return document.querySelector('rt-button[slot="criticsScore"] rt-text').textContent;
        """
        audience_score_script = """
            return document.querySelector('rt-button[slot="audienceScore"] rt-text').textContent;
        """

        # Extract the critics score
        critics_score = driver.execute_script(critics_score_script)

        # Extract the audience score
        audience_score = driver.execute_script(audience_score_script)

        print(f'URL: {url}')
        print('Critics Score:', critics_score)
        print('Audience Score:', audience_score)

        return {'url': url, 'critics_score': critics_score, 'audience_score': audience_score}

    except Exception as e:
        print(f"Error occurred for {url}: {e}")
        return {'url': url, 'critics_score': None, 'audience_score': None}

# List of URLs to scrape
urls = [
    'https://www.rottentomatoes.com/m/the_super_mario_bros_movie',
    'https://www.rottentomatoes.com/m/barbie',
    'https://www.rottentomatoes.com/m/oppenheimer',
    # Add up to 100 URLs here
]

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()

# List to store results
results = []

# Loop through URLs and scrape data
for url in urls:
    result = extract_scores(url)
    results.append(result)

    # Implement a delay between requests
    time.sleep(2)  # Adjust delay as necessary

# Close the browser
driver.quit()

# Display or save results
print("Scraping completed. Results:")
for result in results:
    print(result)

# Optionally, save results to a file
import json
with open('rottentomatoes_results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)


##################

