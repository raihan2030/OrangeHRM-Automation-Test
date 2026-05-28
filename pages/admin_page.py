import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AdminPage(BasePage):
    # --- LOCATORS ---
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    
    # Locators Form Tambah/Cari User
    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/../following-sibling::div//input")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div//input")
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    
    # Locators Dropdown (User Role & Status)
    USER_ROLE_DROPDOWN = (By.XPATH, "//label[text()='User Role']/../following-sibling::div//i")
    STATUS_DROPDOWN = (By.XPATH, "//label[text()='Status']/../following-sibling::div//i")
    DROPDOWN_OPTION_ADMIN = (By.XPATH, "//div[@role='listbox']//span[text()='Admin']")
    DROPDOWN_OPTION_ENABLED = (By.XPATH, "//div[@role='listbox']//span[text()='Enabled']")
    AUTOCOMPLETE_FIRST_OPTION = (By.XPATH, "//div[@role='listbox']//span")
    
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    # Locators Notifikasi & Error
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast-content--success')]")
    FIELD_ERROR_MSG = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")
    CONFIRM_PASSWORD_ERROR = (By.XPATH, "//label[text()='Confirm Password']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class, 'oxd-input-field-error-message')]")
    PASSWORD_ERROR = (By.XPATH, "//label[text()='Password']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class, 'oxd-input-field-error-message')]")
    NO_RECORDS_MSG = (By.XPATH, "//span[text()='No Records Found']")

    # --- ACTIONS ---
    def click_add_button(self):
        self.wait_for_clickable(self.ADD_BUTTON).click()
        self.wait.until(EC.url_contains("saveSystemUser"))

    def select_user_role_admin(self):
        self.wait_for_clickable(self.USER_ROLE_DROPDOWN).click()
        self.wait_for_clickable(self.DROPDOWN_OPTION_ADMIN).click()

    def select_status_enabled(self):
        self.wait_for_clickable(self.STATUS_DROPDOWN).click()
        self.wait_for_clickable(self.DROPDOWN_OPTION_ENABLED).click()

    def enter_employee_name(self, name):
        emp_input = self.wait_for_element(self.EMPLOYEE_NAME_INPUT)
        emp_input.send_keys(name)
        time.sleep(2) 
        self.wait_for_clickable(self.AUTOCOMPLETE_FIRST_OPTION).click()

    def enter_username(self, username):
        self.wait_for_element(self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)

    def enter_confirm_password(self, password):
        self.wait_for_element(self.CONFIRM_PASSWORD_INPUT).send_keys(password)

    def click_save_button(self):
        self.wait_for_clickable(self.SAVE_BUTTON).click()

    def search_by_username(self, username):
        self.wait_for_element(self.USERNAME_INPUT).send_keys(username)
        self.wait_for_clickable(self.SEARCH_BUTTON).click()

    # --- ASSERTIONS / GETTERS ---
    def is_success_toast_displayed(self):
        return self.wait_for_element(self.SUCCESS_TOAST).is_displayed()

    def get_field_error_message(self):
        return self.wait_for_element(self.FIELD_ERROR_MSG).text
    
    def get_confirm_password_error_message(self):
        return self.wait_for_element(self.CONFIRM_PASSWORD_ERROR).text
        
    def is_no_records_found_displayed(self):
        return self.wait_for_element(self.NO_RECORDS_MSG).is_displayed()