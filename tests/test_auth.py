import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestAuth(unittest.TestCase):

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

    # Skenario 4: [Positif] Logout Berhasil (Pindahan)
    def test_04_logout_berhasil(self):
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.logout()
        self.assertTrue(self.login_page.is_login_button_displayed())

        # Skenario 5: [Negatif] Password Kosong
    def test_05_login_empty_password(self):
        self.login_page.enter_username("Admin")
        # Sengaja tidak mengisi password
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())

    # Skenario 6: [Negatif] Username dan Password Kosong
    def test_06_login_empty_username_and_password(self):
        # Langsung klik login tanpa mengisi apapun
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_required_message_displayed())

    # Skenario 7: [Negatif] Password Case Sensitive (Huruf Besar/Kecil salah)
    def test_07_login_invalid_password_case_sensitive(self):
        # Password yang benar adalah "admin123" (huruf kecil semua)
        # Kita uji dengan memasukkan "ADMIN123" (huruf besar)
        self.login_page.login_as("Admin", "ADMIN123")
        self.assertEqual(self.login_page.get_error_message(), "Invalid credentials")