from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Documentation
#   https://selenium-python.readthedocs.io/

path = "C:/Users/gamac/Desktop/Projects/EmailAutomation/chromedriver_win32/chromedriver.exe"

driver = webdriver.Chrome(path)

driver.get("https://techwithtim.net/")
#print(driver.title)

search = driver.find_element_by_name("s")
# Limpar input
search.clear()
# Enviar Texto
search.send_keys("test")
search.send_keys(Keys.RETURN)

time.sleep(5)

# Access all the source code
#print(driver.page_source)

# Esperar até o elemento aparecer
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )

    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        print('a')
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)

except:
    driver.close()

# Voltar para a pagina anterior
#driver.back()

print('fim')

# Close the tab
#driver.close()
# driver.quit() Close the entire browser






