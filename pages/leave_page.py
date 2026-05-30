import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

class LeavePage(BasePage):
    # --- LOCATORS ---
    # Tab Navigasi
    ASSIGN_LEAVE_TAB = (By.XPATH, "//a[normalize-space()='Assign Leave']")
    LEAVE_LIST_TAB = (By.XPATH, "//a[normalize-space()='Leave List']")
    APPLY_TAB = (By.XPATH, "//a[normalize-space()='Apply']")
    APPLY_BUTTON = (By.XPATH, "//button[normalize-space()='Apply']")
    
    # Locators Form Assign Leave
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    EMPLOYEE_SUGGESTION = (By.XPATH, "//div[@role='listbox']//div[contains(@class, 'oxd-autocomplete-option')]")
    LEAVE_TYPE_DROPDOWN = (By.XPATH, "//label[text()='Leave Type']/../following-sibling::div//i")
    FIRST_VALID_LEAVE_TYPE = (By.XPATH, "(//div[@role='listbox']//div[contains(@class, 'oxd-select-option')])[2]") 
    FROM_DATE_INPUT = (By.XPATH, "//label[text()='From Date']/../following-sibling::div//input")
    TO_DATE_INPUT = (By.XPATH, "//label[text()='To Date']/../following-sibling::div//input")
    COMMENT_INPUT = (By.XPATH, "//label[text()='Comments']/../following-sibling::div//textarea")
    ASSIGN_BUTTON = (By.XPATH, "//button[normalize-space()='Assign']")
    CONFIRM_OK_BUTTON = (By.XPATH, "//button[normalize-space()='Ok']")
    
    # Locators Form Leave List (Filter)
    STATUS_DROPDOWN = (By.XPATH, "//label[text()='Show Leave with Status']/../following-sibling::div//div[contains(@class, 'oxd-select-text')]")
    PENDING_APPROVAL_OPTION = (By.XPATH, "//div[@role='listbox']//span[text()='Pending Approval']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    
    # Locators Pesan / Notifikasi
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast-content--success')]")
    WARN_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast-content--warn') or contains(@class, 'oxd-toast-content--error')]")     
    INSUFFICIENT_BALANCE_MSG = (By.XPATH, "//p[contains(@class, 'orangehrm-leave-balance-text') and text()='Balance not sufficient']")
    DATE_ERROR_MSG = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message') and text()='To date should be after from date']")
    REQUIRED_ERROR_MSG = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message') and text()='Required']")

    # Locators Menu Entitlements
    ENTITLEMENTS_MENU = (By.XPATH, "//span[normalize-space()='Entitlements' or contains(text(), 'Entitlements')]")
    ADD_ENTITLEMENTS_SUBMENU = (By.XPATH, "//a[normalize-space()='Add Entitlements']")
    ENTITLEMENT_INPUT = (By.XPATH, "//label[text()='Entitlement']/../following-sibling::div//input")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    CONFIRM_ENTITLEMENT_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")
    MY_LEAVE_TAB = (By.XPATH, "//a[normalize-space()='My Leave']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    CHECKBOX_ALL = (By.XPATH, "//div[contains(@class, 'oxd-table-header')]//i[contains(@class, 'oxd-checkbox-input-icon')]")
    EMPLOYEE_ENTITLEMENTS_SUBMENU = (By.XPATH, "//a[normalize-space()='Employee Entitlements']")
    CHECKBOX_MASTER = (By.XPATH, "//div[contains(@class, 'oxd-table-header')]//span[contains(@class, 'oxd-checkbox-input')]")
    DELETE_SELECTED_BUTTON = (By.XPATH, "//button[normalize-space()='Delete Selected']")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")

    # --- ACTIONS ---
    def click_assign_leave_tab(self):
        self.wait_for_clickable(self.ASSIGN_LEAVE_TAB).click()
        time.sleep(1)

    def click_leave_list_tab(self):
        self.wait_for_clickable(self.LEAVE_LIST_TAB).click()
        time.sleep(1)

    def enter_employee_name(self, name_hint="a"):
        ele = self.wait_for_element(self.EMPLOYEE_NAME_INPUT)
        ele.send_keys(name_hint)
        time.sleep(2) 
        self.wait_for_clickable(self.EMPLOYEE_SUGGESTION).click()

    def select_leave_type(self):
        self.wait_for_clickable(self.LEAVE_TYPE_DROPDOWN).click()
        self.wait_for_clickable(self.FIRST_VALID_LEAVE_TYPE).click()
        time.sleep(1)

    def _enter_date(self, locator, date_str):
        """Fungsi pembantu internal untuk menghapus dan mengisi tanggal"""
        ele = self.wait_for_element(locator)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(date_str)
        ele.send_keys(Keys.TAB) 

    def enter_from_date(self, date_str):
        self._enter_date(self.FROM_DATE_INPUT, date_str)

    def enter_to_date(self, date_str):
        self._enter_date(self.TO_DATE_INPUT, date_str)
        
    def enter_comment(self, comment_text):
        self.wait_for_element(self.COMMENT_INPUT).send_keys(comment_text)

    def click_assign_button(self):
        self.wait_for_clickable(self.ASSIGN_BUTTON).click()

    def select_status_pending_approval(self):
        self.wait_for_clickable(self.STATUS_DROPDOWN).click()
        self.wait_for_clickable(self.PENDING_APPROVAL_OPTION).click()
        self.force_unfocus()

    def click_search_button(self):
        self.wait_for_clickable(self.SEARCH_BUTTON).click()

    def _handle_popup(self, locator, timeout=3):
        """Fungsi pembantu untuk menangani berbagai pop-up konfirmasi"""
        try:
            wait_short = WebDriverWait(self.driver, timeout)
            wait_short.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException:
            pass

    def handle_insufficient_balance_popup(self):
        self._handle_popup(self.CONFIRM_OK_BUTTON)

    def confirm_entitlement_if_needed(self):
        self._handle_popup(self.CONFIRM_ENTITLEMENT_BUTTON)
    
    def force_unfocus(self):
        try:
            self.driver.find_element(By.XPATH, "//h6[contains(@class, 'oxd-topbar-header-breadcrumb-module')]").click()
        except:
            pass

    def click_add_entitlements_menu(self):
        self.wait_for_clickable(self.ENTITLEMENTS_MENU).click()
        self.wait_for_clickable(self.ADD_ENTITLEMENTS_SUBMENU).click()
        time.sleep(1)

    def enter_entitlement_amount(self, amount):
        ele = self.wait_for_element(self.ENTITLEMENT_INPUT)
        ele.send_keys(Keys.CONTROL + "a")
        ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(amount)

    def click_save_button(self):
        self.wait_for_clickable(self.SAVE_BUTTON).click()

    def click_confirm_ok_popup_strict(self):
        """Mengklik tombol Ok pada pop-up. Tanpa try-except agar test gagal jika pop-up tidak muncul."""
        self.wait_for_clickable(self.CONFIRM_OK_BUTTON).click()

    def click_apply_tab(self):
        self.wait_for_clickable(self.APPLY_TAB).click()
        time.sleep(1)

    def click_apply_button(self):
        self.wait_for_clickable(self.APPLY_BUTTON).click()

    def click_my_leave_tab(self):
        self.wait_for_clickable(self.MY_LEAVE_TAB).click()
        time.sleep(1)

    def cancel_all_my_leaves(self):
        """Membatalkan seluruh permohonan cuti yang masih bisa di-cancel"""
        while True:
            try:
                # Menggunakan timeout pendek agar pengujian cepat berlanjut jika tombol tidak ada
                wait_short = WebDriverWait(self.driver, 3)
                cancel_btn = wait_short.until(EC.element_to_be_clickable(self.CANCEL_BUTTON))
                cancel_btn.click()
                time.sleep(2) # Memberi jeda waktu proses pembatalan/toast info
            except TimeoutException:
                break

    def click_employee_entitlements_menu(self):
        self.wait_for_clickable(self.ENTITLEMENTS_MENU).click()
        self.wait_for_clickable(self.EMPLOYEE_ENTITLEMENTS_SUBMENU).click()
        time.sleep(1)

    def delete_all_employee_entitlements(self):
        """Menghapus massal menggunakan master checkbox"""
        try:
            wait_short = WebDriverWait(self.driver, 3)
            
            # 1. Klik Master Checkbox di Header Tabel
            master_cb = wait_short.until(EC.element_to_be_clickable(self.CHECKBOX_MASTER))
            master_cb.click()
            time.sleep(1) # Tunggu tombol Delete Selected muncul
            
            # 2. Klik Delete Selected
            del_selected = wait_short.until(EC.element_to_be_clickable(self.DELETE_SELECTED_BUTTON))
            del_selected.click()
            time.sleep(1)
            
            # 3. Konfirmasi
            confirm_del = wait_short.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON))
            confirm_del.click()
            time.sleep(2)
            
        except TimeoutException:
            # Masuk ke sini jika tabel kosong (Master Checkbox tidak ada)
            pass

    # --- ASSERTIONS / GETTERS ---
    def is_success_toast_displayed(self):
        return self.wait_for_element(self.SUCCESS_TOAST).is_displayed()
    
    def is_warn_toast_displayed(self):
        return self.wait_for_element(self.WARN_TOAST).is_displayed()

    def is_insufficient_balance_msg_displayed(self):
        return self.wait_for_element(self.INSUFFICIENT_BALANCE_MSG).is_displayed()

    def is_date_error_displayed(self):
        return self.wait_for_element(self.DATE_ERROR_MSG).is_displayed()
    
    def is_required_error_displayed(self):
        return self.wait_for_element(self.REQUIRED_ERROR_MSG).is_displayed()