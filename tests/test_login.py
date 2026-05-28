import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Skenario 1: [Positif] Login Valid
    def test_01_login_valid(self):
        self.login_page.login_as("Admin", "admin123")
        self.assertEqual(self.dashboard_page.get_dashboard_header(), "Dashboard")

    # Skenario 2: [Negatif] Password Salah
    def test_02_login_invalid_password(self):
        self.login_page.login_as("Admin", "salahpassword")
        self.assertEqual(self.login_page.get_error_message(), "Invalid credentials")

    # Skenario 3: [Negatif] Username Kosong
    def test_03_login_empty_username(self):
        self.login_page.enter_password("admin123")
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())