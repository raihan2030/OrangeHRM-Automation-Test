import unittest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage

class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.admin_page = AdminPage(self.driver)
        
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.click_admin_menu()

    def tearDown(self):
        self.driver.quit()

    # --- POSITIVE TEST CASE ---

    def test_01_search_user_valid(self):
        self.admin_page.search_by_username("Admin")
        time.sleep(2) 
        pass

    def test_02_add_user_success(self):
        self.admin_page.click_add_button()
        self.admin_page.select_user_role_admin()
        self.admin_page.select_status_enabled()
        self.admin_page.enter_employee_name("a")
        
        unique_username = f"ZeztzUser_{int(time.time())}"
        self.admin_page.enter_username(unique_username)
        
        self.admin_page.enter_password("ZeztzPassword123!")
        self.admin_page.enter_confirm_password("ZeztzPassword123!")
        self.admin_page.click_save_button()
        
        self.assertTrue(self.admin_page.is_success_toast_displayed())
    
    def test_03_search_user_by_user_role(self):
        self.admin_page.wait_for_clickable(self.admin_page.USER_ROLE_DROPDOWN).click()
        self.admin_page.wait_for_clickable(self.admin_page.DROPDOWN_OPTION_ADMIN).click()
        self.admin_page.click_search_button()
        time.sleep(2)
        pass

    def test_04_search_user_by_employee_name(self):
        self.admin_page.enter_employee_name("a") 
        self.admin_page.click_search_button()
        time.sleep(2)
        pass

    def test_05_edit_user_status_disabled(self):
        self.admin_page.edit_first_record()
        self.admin_page.select_status_disabled()
        self.admin_page.click_save_button()
        
        self.assertTrue(self.admin_page.is_success_toast_displayed())

    def test_06_delete_user(self):
        self.admin_page.delete_second_record()
        
        time.sleep(2)
        self.assertTrue(self.admin_page.is_success_toast_displayed())

    # --- NEGATIVE TEST CASE ---

    def test_07_add_user_password_mismatch(self):
        self.admin_page.click_add_button()
        self.admin_page.enter_username("TestMismatch123")
        self.admin_page.enter_password("SandiKuat123!")
        self.admin_page.enter_confirm_password("SandiBeda123!")
        
        self.assertEqual(self.admin_page.get_confirm_password_error_message(), "Passwords do not match")

    def test_08_add_user_short_password(self):
        self.admin_page.click_add_button()
        self.admin_page.enter_password("1234")
        
        self.assertEqual(self.admin_page.get_field_error_message(), "Should have at least 7 characters")

    def test_09_search_invalid_username(self):
        self.admin_page.search_by_username("UserAsalAsalan999")
        
        self.assertTrue(self.admin_page.is_no_records_found_displayed())
    
    def test_10_add_user_empty_user_role(self):
        self.admin_page.click_add_button()
        self.admin_page.select_status_enabled()
        self.admin_page.enter_employee_name("a")
        
        unique_username = f"UserNoRole_{int(time.time())}"
        self.admin_page.enter_username(unique_username)
        self.admin_page.enter_password("ZeztzPassword123!")
        self.admin_page.enter_confirm_password("ZeztzPassword123!")
        self.admin_page.click_save_button()
        
        time.sleep(2)
        self.assertEqual(self.admin_page.get_field_error_message(), "Required")

    def test_11_add_user_empty_employee_name(self):
        self.admin_page.click_add_button()
        self.admin_page.select_user_role_admin()
        self.admin_page.select_status_enabled()
        
        unique_username = f"UserNoName_{int(time.time())}"
        self.admin_page.enter_username(unique_username)
        self.admin_page.enter_password("ZeztzPassword123!")
        self.admin_page.enter_confirm_password("ZeztzPassword123!")
        self.admin_page.click_save_button()
        
        time.sleep(2)
        self.assertEqual(self.admin_page.get_field_error_message(), "Required")

    def test_12_add_user_duplicate_username(self):
        self.admin_page.click_add_button()
        self.admin_page.select_user_role_admin()
        self.admin_page.select_status_enabled()
        self.admin_page.enter_employee_name("a")
        
        self.admin_page.enter_username("Admin")
        
        self.admin_page.enter_password("ZeztzPassword123!")
        self.admin_page.enter_confirm_password("ZeztzPassword123!")
        self.admin_page.click_save_button()
        
        time.sleep(2)
        self.assertEqual(self.admin_page.get_field_error_message(), "Already exists")