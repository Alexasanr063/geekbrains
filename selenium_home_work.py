from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import  pandas as pd
# Настройка User Agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# Настройки для Firefox
firefox_options = Options()
firefox_options.set_preference("general.useragent.override", user_agent)

# Запуск драйвера Firefox
driver = webdriver.Firefox(options=firefox_options)




pages = 10
for page in range(1, pages):
    url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"
    driver.get(url)
    items = len(driver.find_elements(By.CLASS_NAME,"quote"))
    total = []
    for item in range(items):
        quotes = driver.find_elements(By.CLASS_NAME,"quote")
        for quote in quotes:
            #quote_text = quote.find_element_by_class_name('text').text[1:]
            quote_text = quote.find_element(By.CLASS_NAME,"text").text[1:]
            author = quote.find_element(By.CLASS_NAME,"author").text
            new = ((quote_text, author))
            total.append(new)
    df = pd.DataFrame(total, columns=['quote', 'author'])
    df.to_csv('quoted.csv')
driver.close()