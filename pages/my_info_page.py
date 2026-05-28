import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

class MyInfoPage(BasePage):
    # --- LOCATORS ---
    # Menu & Tabs
    MY_INFO_MENU = (By.XPATH, "//span[text()='My Info']")
    PERSONAL_DETAILS_TAB = (By.XPATH, "//a[text()='Personal Details']")
    CONTACT_DETAILS_TAB = (By.XPATH, "//a[text()='Contact Details']")
    
    # Formulir Contact Details
    MOBILE_INPUT = (By.XPATH, "//label[text()='Mobile']/../following-sibling::div//input")
    WORK_EMAIL_INPUT = (By.XPATH, "//label[text()='Work Email']/../following-sibling::div//input")
    
    # Formulir Personal Details
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    
    # Locators Tombol Save & Attachments
    SAVE_BUTTON_MAIN = (By.XPATH, "(//button[@type='submit'])[1]")
    ADD_ATTACHMENT_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    
    # Notifikasi & Error
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast-content--success')]")
    FIRST_NAME_ERROR = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")
    FILE_ERROR = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")

    # --- ACTIONS ---
    def click_my_info_menu(self):
        self.wait_for_clickable(self.MY_INFO_MENU).click()
        time.sleep(2)

    def click_contact_details_tab(self):
        self.wait_for_clickable(self.CONTACT_DETAILS_TAB).click()
        time.sleep(1)

    def click_personal_details_tab(self):
        self.wait_for_clickable(self.PERSONAL_DETAILS_TAB).click()
        time.sleep(1)

    def update_mobile_phone(self, phone):
        ele = self.wait_for_element(self.MOBILE_INPUT)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(phone)

    def update_work_email(self, email):
        ele = self.wait_for_element(self.WORK_EMAIL_INPUT)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(email)

    def clear_first_name(self):
        ele = self.wait_for_element(self.FIRST_NAME_INPUT)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        ele.send_keys(Keys.TAB)

    def click_save_main_form(self):
        self.wait_for_clickable(self.SAVE_BUTTON_MAIN).click()

    def click_add_attachment(self):
        buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Add']")
        if buttons:
            buttons[-1].click()

    def upload_attachment(self, file_path):
        file_input = self.wait_for_element(self.FILE_INPUT)
        file_input.send_keys(file_path)

    def click_save_attachment(self):
        save_btns = self.driver.find_elements(By.XPATH, "//button[@type='submit']")
        if save_btns:
            save_btns[-1].click()

    # --- ASSERTIONS / GETTERS ---
    def is_success_toast_displayed(self):
        return self.wait_for_element(self.SUCCESS_TOAST).is_displayed()

    def get_first_name_error_message(self):
        return self.wait_for_element(self.FIRST_NAME_ERROR).text
    
    def get_file_error_message(self):
        return self.wait_for_element(self.FILE_ERROR).text