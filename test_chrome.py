from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Testando Chrome...")

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

print("Chrome aberto! Acessando LinkedIn...")
driver.get('https://www.linkedin.com')
time.sleep(5)

print("Teste concluído! Fechando...")
driver.quit()
