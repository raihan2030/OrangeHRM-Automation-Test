import unittest
import time
import os
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.my_info_page import MyInfoPage

class TestMyInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dummy_doc_path = os.path.abspath("dummy_profile_attachment.txt")
        with open(cls.dummy_doc_path, "w") as f:
            f.write("Ini adalah dokumen dummy untuk pengujian upload di menu My Info.")
        
        cls.large_doc_path = os.path.abspath("dummy_large_attachment.txt")
        with open(cls.large_doc_path, "wb") as f:
            f.write(os.urandom(2 * 1024 * 1024))

    @classmethod
    def tearDownClass(cls):
        for file in [cls.dummy_doc_path, cls.large_doc_path]:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.my_info_page = MyInfoPage(self.driver)
        
        self.login_page.login_as("Admin", "admin123")
        self.my_info_page.click_my_info_menu()

    def tearDown(self):
        self.driver.quit()

    # --- POSITIVE TEST CASE ---

    def test_01_update_contact_details_valid(self):
        self.my_info_page.click_contact_details_tab()
        
        self.my_info_page.update_mobile_phone("081234567890")
        self.my_info_page.update_work_email("update.test@example.com")
        
        self.my_info_page.click_save_main_form()
        
        self.assertTrue(self.my_info_page.is_success_toast_displayed())

    def test_02_add_attachment_valid(self):
        self.my_info_page.click_personal_details_tab()
        self.my_info_page.click_add_attachment()
        
        self.my_info_page.upload_attachment(self.dummy_doc_path)
        self.my_info_page.click_save_attachment()
        
        self.assertTrue(self.my_info_page.is_success_toast_displayed())

    # --- NEGATIVE TEST CASE ---

    def test_03_update_personal_details_empty_first_name(self):
        self.my_info_page.click_personal_details_tab()
        self.my_info_page.clear_first_name()
        
        self.my_info_page.click_save_main_form()
        
        self.assertEqual(self.my_info_page.get_first_name_error_message(), "Required")

    def test_04_add_attachment_size_exceeded(self):
        self.my_info_page.click_personal_details_tab()
        self.my_info_page.click_add_attachment()
        
        self.my_info_page.upload_attachment(self.large_doc_path)
        
        self.assertEqual(self.my_info_page.get_file_error_message(), "Attachment Size Exceeded")