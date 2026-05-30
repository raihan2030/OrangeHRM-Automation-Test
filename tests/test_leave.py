import unittest
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage
from pages.my_info_page import MyInfoPage
from pages.pim_page import PIMPage

class TestLeave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver = webdriver.Edge()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        leave_page = LeavePage(driver)
        my_info_page = MyInfoPage(driver)
        pim_page = PIMPage(driver)

        cls.admin_first_name = "LeaveTest"
        cls.admin_last_name = "AdminUser"
        cls.admin_employee_name = f"{cls.admin_first_name} {cls.admin_last_name}"
        
        cls.dummy_first_name = "Dummy"
        cls.dummy_last_name = "Assignee"
        cls.dummy_employee_name = f"{cls.dummy_first_name} {cls.dummy_last_name}"
        cls.dummy_emp_id = f"TMP{int(time.time())}"[-8:]

        login_page.login_as("Admin", "admin123")
        
        my_info_page.click_my_info_menu()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )
        my_info_page.enter_first_name(cls.admin_first_name)
        my_info_page.clear_middle_name()
        my_info_page.enter_last_name(cls.admin_last_name)
        my_info_page.click_save_main_form()
        time.sleep(3)
        
        dashboard_page.click_pim_menu()
        pim_page.click_add_button()
        pim_page.enter_first_name(cls.dummy_first_name)
        pim_page.enter_last_name(cls.dummy_last_name)
        pim_page.enter_employee_id_add(cls.dummy_emp_id)
        pim_page.click_save_button()
        time.sleep(3)
        
        dashboard_page.click_leave_menu()
        leave_page.click_my_leave_tab()
        leave_page.cancel_all_my_leaves()

        leave_page.click_employee_entitlements_menu()
        leave_page.enter_employee_name(cls.admin_employee_name)
        leave_page.click_search_button()
        time.sleep(2)
        leave_page.delete_all_employee_entitlements()

        leave_page.click_add_entitlements_menu()
        leave_page.enter_employee_name(cls.admin_employee_name)
        leave_page.select_leave_type()
        leave_page.enter_entitlement_amount("10")
        leave_page.click_save_button()
        leave_page.confirm_entitlement_if_needed()
        time.sleep(2) 

        leave_page.click_employee_entitlements_menu()
        leave_page.click_add_entitlements_menu()
        leave_page.enter_employee_name(cls.dummy_employee_name)
        leave_page.select_leave_type()
        leave_page.enter_entitlement_amount("10")
        leave_page.click_save_button()
        leave_page.confirm_entitlement_if_needed()
        time.sleep(2)
        
        driver.quit()

    @classmethod
    def tearDownClass(cls):
        """Membersihkan lingkungan pengujian dengan menghapus employee sementara (Aman jika tidak ditemukan)"""
        driver = webdriver.Edge()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        
        try:
            login_page.login_as("Admin", "admin123")
            dashboard_page.click_pim_menu()
            
            pim_page.search_by_employee_id(cls.dummy_emp_id)
            time.sleep(2)
            
            no_records = driver.find_elements(By.XPATH, "//span[text()='No Records Found']")
            
            if len(no_records) == 0:
                pim_page.delete_first_record()
                time.sleep(2)
            else:
                print(f"Employee dengan ID {cls.dummy_emp_id} tidak ditemukan. Melewati proses hapus.")
                
        except Exception as e:
            print(f"Terdapat kendala saat Teardown: {e}")
        finally:
            driver.quit()

    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.leave_page = LeavePage(self.driver)
        
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.click_leave_menu()

    def tearDown(self):
        self.driver.quit()

    # --- HELPER METHODS ---
    
    def get_date(self, days_offset=0):
        return (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%d-%m")

    def fill_assign_leave(self, from_offset, to_offset, comment=""):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.dummy_employee_name) 
        self.leave_page.select_leave_type()
        self.leave_page.enter_from_date(self.get_date(from_offset))
        time.sleep(1) 
        self.leave_page.enter_to_date(self.get_date(to_offset))
        if comment:
            self.leave_page.enter_comment(comment)
        self.leave_page.force_unfocus()
        time.sleep(2)

    def fill_apply_leave(self, from_offset, to_offset, comment=""):
        self.leave_page.click_apply_tab()
        self.leave_page.select_leave_type()
        self.leave_page.enter_from_date(self.get_date(from_offset))
        time.sleep(1) 
        self.leave_page.enter_to_date(self.get_date(to_offset))
        if comment:
            self.leave_page.enter_comment(comment)
        self.leave_page.force_unfocus()
        time.sleep(2)

    # --- POSITIVE TEST CASES ---

    def test_01_assign_leave_success(self):
        self.fill_assign_leave(0, 2, "Automated test: Normal Leave")
        self.leave_page.click_assign_button()
        time.sleep(2)
        self.assertTrue(self.leave_page.is_success_toast_displayed())

    def test_06_apply_leave_success(self):
        self.fill_apply_leave(2, 4, "Automated test: Apply Leave Success")
        self.leave_page.click_apply_button()
        time.sleep(2)
        self.assertTrue(self.leave_page.is_success_toast_displayed())

    def test_11_filter_leave_by_pending_approval(self):
        self.leave_page.click_leave_list_tab()
        self.leave_page.select_status_pending_approval()
        self.leave_page.click_search_button()
        time.sleep(2) 

    # --- NEGATIVE TEST CASES ---

    def test_02_assign_leave_overlapping(self):
        self.fill_assign_leave(0, 2, "Automated test: Overlapping Leave")
        self.leave_page.click_assign_button()
        time.sleep(2)
        self.assertTrue(self.leave_page.is_warn_toast_displayed())

    def test_03_assign_leave_insufficient_balance(self):
        self.fill_assign_leave(2, 52)
        self.assertTrue(self.leave_page.is_insufficient_balance_msg_displayed())

    def test_04_assign_leave_to_date_before_from_date(self):
        self.fill_assign_leave(1, -1)
        self.assertTrue(self.leave_page.is_date_error_displayed())

    def test_05_assign_leave_without_leave_type(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.dummy_employee_name)
        self.leave_page.enter_from_date(self.get_date(0))
        time.sleep(1)
        self.leave_page.enter_to_date(self.get_date(2))
        self.leave_page.force_unfocus()
        time.sleep(1)
        
        self.leave_page.click_assign_button()
        self.assertTrue(self.leave_page.is_required_error_displayed())

    def test_07_apply_leave_overlapping(self):
        self.fill_apply_leave(2, 4, "Automated test: Overlapping Leave")
        self.leave_page.click_apply_button()
        time.sleep(2)
        self.assertTrue(self.leave_page.is_warn_toast_displayed())

    def test_08_apply_leave_insufficient_balance(self):
        self.fill_apply_leave(2, 17)
        self.assertTrue(self.leave_page.is_insufficient_balance_msg_displayed())

    def test_09_apply_leave_to_date_before_from_date(self):
        self.fill_apply_leave(1, -1)
        self.assertTrue(self.leave_page.is_date_error_displayed())

    def test_10_apply_leave_without_leave_type(self):
        self.leave_page.click_apply_tab()
        self.leave_page.enter_from_date(self.get_date(0))
        time.sleep(1)
        self.leave_page.enter_to_date(self.get_date(2))
        self.leave_page.force_unfocus()
        time.sleep(1)
        
        self.leave_page.click_apply_button()
        self.assertTrue(self.leave_page.is_required_error_displayed())