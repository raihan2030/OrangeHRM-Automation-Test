from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # --- LOCATORS ---
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MSG = (By.XPATH, "//p[contains(@class, 'oxd-alert-content-text')]")
    REQUIRED_MSG = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")

    # --- ACTIONS ---
    def enter_username(self, username):
        self.wait_for_element(self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.wait_for_clickable(self.LOGIN_BUTTON).click()

    # Aksi gabungan agar tidak perlu mengetik 3 baris di file test
    def login_as(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # --- ASSERTIONS / GETTERS ---
    def get_error_message(self):
        return self.wait_for_element(self.ERROR_MSG).text

    def get_required_message(self):
        return self.wait_for_element(self.REQUIRED_MSG).text
        
    def is_login_button_displayed(self):
        return self.wait_for_element(self.LOGIN_BUTTON).is_displayed()
    
    def is_required_message_displayed(self):
        return self.wait_for_element(self.REQUIRED_MSG).is_displayed()