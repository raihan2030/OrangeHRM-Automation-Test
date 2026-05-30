import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

class PIMPage(BasePage):
    # --- LOCATORS ---
    # Tombol Navigasi & Aksi Umum
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    # Locators Form Tambah Pegawai (Add Employee)
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMPLOYEE_ID_ADD_INPUT = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    
    # Locators Pencarian (Employee List)
    EMPLOYEE_ID_SEARCH_INPUT = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")
    EMPLOYEE_NAME_SEARCH_INPUT = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    AUTOCOMPLETE_FIRST_OPTION = (By.XPATH, "//div[@role='listbox']//span")
    
    # Locators Tabel & Hapus
    FIRST_TRASH_ICON = (By.XPATH, "(//i[contains(@class, 'bi-trash')])[1]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
    
    # Locators Notifikasi & Error Spesifik
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast-content--success')]")
    FIRST_NAME_ERROR = (By.XPATH, "//input[@name='firstName']/parent::div/following-sibling::span[contains(@class, 'oxd-input-field-error-message')]")
    LAST_NAME_ERROR = (By.XPATH, "//input[@name='lastName']/parent::div/following-sibling::span[contains(@class, 'oxd-input-field-error-message')]")
    EMPLOYEE_ID_ERROR = (By.XPATH, "//label[text()='Employee Id']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class, 'oxd-input-field-error-message')]")
    FILE_ERROR = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")

    # --- ACTIONS ---
    def click_add_button(self):
        self.wait_for_clickable(self.ADD_BUTTON).click()
        self.wait.until(EC.url_contains("addEmployee"))

    def enter_first_name(self, first_name):
        self.wait_for_element(self.FIRST_NAME_INPUT).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.wait_for_element(self.LAST_NAME_INPUT).send_keys(last_name)

    def enter_employee_id_add(self, emp_id):
        ele = self.wait_for_element(self.EMPLOYEE_ID_ADD_INPUT)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(emp_id)

    def upload_photo(self, file_path):
        file_input = self.wait_for_element(self.FILE_INPUT)
        file_input.send_keys(file_path)

    def click_save_button(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "oxd-form-loader")))
        except TimeoutException:
            pass
            
        btn = self.wait_for_clickable(self.SAVE_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)

    def search_by_employee_id(self, emp_id):
        self.wait_for_element(self.EMPLOYEE_ID_SEARCH_INPUT).send_keys(emp_id)
        self.wait_for_clickable(self.SEARCH_BUTTON).click()

    def search_by_employee_name(self, name):
        emp_input = self.wait_for_element(self.EMPLOYEE_NAME_SEARCH_INPUT)
        emp_input.send_keys(name)
        time.sleep(2)
        self.wait_for_clickable(self.AUTOCOMPLETE_FIRST_OPTION).click()
        self.wait_for_clickable(self.SEARCH_BUTTON).click()

    def delete_first_record(self):
        self.wait_for_clickable(self.FIRST_TRASH_ICON).click()
        self.wait_for_clickable(self.CONFIRM_DELETE_BUTTON).click()

    # --- ASSERTIONS / GETTERS ---
    def is_success_toast_displayed(self):
        return self.wait_for_element(self.SUCCESS_TOAST).is_displayed()

    def get_first_name_error_message(self):
        return self.wait_for_element(self.FIRST_NAME_ERROR).text

    def get_last_name_error_message(self):
        return self.wait_for_element(self.LAST_NAME_ERROR).text
        
    def get_employee_id_error_message(self):
        return self.wait_for_element(self.EMPLOYEE_ID_ERROR).text
        
    def get_file_error_message(self):
        return self.wait_for_element(self.FILE_ERROR).text