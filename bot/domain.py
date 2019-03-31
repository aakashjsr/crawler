import time, datetime
from datetime import timezone
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://moonsy.com/domain_authority/"
driver = webdriver.Chrome('/Users/aakashkumardas/Downloads/chromedriver')
# driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'], service_log_path='/tmp/ghostdriver.log')
driver.get(url)
# driver.quit()
    
