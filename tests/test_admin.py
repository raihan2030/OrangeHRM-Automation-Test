import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Skenario 4: [Positif] Buka Menu Admin
    def test_04_navigasi_ke_menu_admin(self):
        # Karena ini tes dashboard, kita wajib login dulu di setiap awal skenario
        self.login_page.login_as("Admin", "admin123")
        
        self.dashboard_page.click_admin_menu()
        self.assertEqual(self.dashboard_page.get_topbar_header(), "Admin")

    # Skenario 5: [Positif] Logout
    def test_05_logout_berhasil(self):
        self.login_page.login_as("Admin", "admin123")
        
        self.dashboard_page.logout()
        self.assertTrue(self.login_page.is_login_button_displayed())