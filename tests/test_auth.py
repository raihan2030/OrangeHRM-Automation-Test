import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # --- POSITIVE TEST CASE ---

    def test_01_login_valid(self):
        self.login_page.login_as("Admin", "admin123")
        self.assertEqual(self.dashboard_page.get_dashboard_header(), "Dashboard")

    def test_02_logout_berhasil(self):
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.logout()
        self.assertTrue(self.login_page.is_login_button_displayed())

    # --- NEGATIVE TEST CASE ---
    
    def test_03_login_invalid_password(self):
        self.login_page.login_as("Admin", "salahpassword")
        self.assertEqual(self.login_page.get_error_message(), "Invalid credentials")

    def test_04_login_empty_username(self):
        self.login_page.enter_password("admin123")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())

    def test_05_login_empty_password(self):
        self.login_page.enter_username("Admin")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())

    def test_06_login_empty_username_and_password(self):
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())

    def test_07_login_invalid_password_case_sensitive(self):
        self.login_page.login_as("Admin", "ADMIN123")
        self.assertEqual(self.login_page.get_error_message(), "Invalid credentials")