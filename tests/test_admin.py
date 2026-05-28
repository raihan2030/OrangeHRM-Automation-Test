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
        
        unique_username = f"RaihanUser_{int(time.time())}"
        self.admin_page.enter_username(unique_username)
        
        self.admin_page.enter_password("RaihanPassword123!")
        self.admin_page.enter_confirm_password("RaihanPassword123!")
        self.admin_page.click_save_button()
        
        self.assertTrue(self.admin_page.is_success_toast_displayed())

    # --- NEGATIVE TEST CASE ---

    def test_03_add_user_password_mismatch(self):
        self.admin_page.click_add_button()
        self.admin_page.enter_username("TestMismatch123")
        self.admin_page.enter_password("SandiKuat123!")
        self.admin_page.enter_confirm_password("SandiBeda123!")
        
        self.assertEqual(self.admin_page.get_confirm_password_error_message(), "Passwords do not match")

    def test_04_add_user_short_password(self):
        self.admin_page.click_add_button()
        self.admin_page.enter_password("1234")
        
        self.assertEqual(self.admin_page.get_field_error_message(), "Should have at least 7 characters")

    def test_05_search_invalid_username(self):
        self.admin_page.search_by_username("UserAsalAsalan999")
        
        self.assertTrue(self.admin_page.is_no_records_found_displayed())