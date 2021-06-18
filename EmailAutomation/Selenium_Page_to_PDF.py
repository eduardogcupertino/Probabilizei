from selenium import webdriver
import json
import os

chrome_options = webdriver.ChromeOptions()
settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')

CHROMEDRIVER_PATH = "C:/Users/gamac/Desktop/Projects/EmailAutomation/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)
driver.get("https://nfe.prefeitura.sp.gov.br/contribuinte/notaprint.aspx?ccm=51858827&nf=3028&cod=4VY4S7FX")
driver.execute_script('window.print();')
#driver.quit()