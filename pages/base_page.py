from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Fungsi pembantu untuk menunggu elemen muncul
    def wait_for_element(self, by_locator):
        return self.wait.until(EC.presence_of_element_located(by_locator))
        
    # Fungsi pembantu untuk menunggu elemen bisa diklik
    def wait_for_clickable(self, by_locator):
        return self.wait.until(EC.element_to_be_clickable(by_locator))