from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


path = "chromedriver-linux64/chromedriver"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.poyerbani.pl/pol_m_Yerba-Mate_Yerba-Mate-wedlug-rodzaju_Smakowe-176.html')

urls = []
def cycle():
    global urls
    # find all the elements with data-product_id
    products = driver.find_elements(by=webdriver.common.by.By.XPATH, value="//*[@data-product_id]")
    # ger url for each data-product_id element and print it
    for product in products:
        try:
            product_link_element = product.find_element(by=webdriver.common.by.By.XPATH, value='.//a[contains(@class, "product__icon")]')
            url = product_link_element.get_attribute('href')
            if url:
                urls.append(url)
        except:
            continue
    try:
        link = driver.find_element(By.LINK_TEXT, "Następna strona")
        driver.execute_script("arguments[0].click();", link)
    except NoSuchElementException:
        driver.quit()

for x in range(11):
    cycle()


print(len(urls))