import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage

class TestPIM(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Membuat dummy files untuk keperluan test upload secara otomatis
        cls.valid_image_path = os.path.abspath("dummy_valid.jpg")
        cls.invalid_pdf_path = os.path.abspath("dummy_invalid.pdf")
        cls.large_image_path = os.path.abspath("dummy_large.jpg")
        
        with open(cls.valid_image_path, "wb") as f: f.write(os.urandom(1024))
        with open(cls.invalid_pdf_path, "wb") as f: f.write(os.urandom(1024))
        with open(cls.large_image_path, "wb") as f: f.write(os.urandom(2 * 1024 * 1024))

        # --- SETUP PRASYARAT: Pastikan Employee ID 0024 ada ---
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        
        login_page.login_as("Admin", "admin123")
        dashboard_page.click_pim_menu()
        
        pim_page.search_by_employee_id("0024")
        time.sleep(2)
        
        no_records = driver.find_elements(By.XPATH, "//span[text()='No Records Found']")
        if len(no_records) > 0:
            pim_page.click_add_button()
            pim_page.enter_first_name("Kamen")
            pim_page.enter_last_name("Rider")
            pim_page.enter_employee_id_add("0024")
            pim_page.click_save_button()
            time.sleep(3)
            
        driver.quit()

    @classmethod
    def tearDownClass(cls):
        for file in [cls.valid_image_path, cls.invalid_pdf_path, cls.large_image_path]:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.pim_page = PIMPage(self.driver)
        
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.click_pim_menu()

    def tearDown(self):
        self.driver.quit()

    # --- POSITIVE TEST CASE ---

    def test_01_add_employee_valid(self):
        self.pim_page.click_add_button()
        self.pim_page.enter_first_name("Zeztz")
        self.pim_page.enter_last_name("Automated")
        
        unique_id = f"ID{int(time.time())}"[-8:] 
        self.pim_page.enter_employee_id_add(unique_id)
        
        self.pim_page.click_save_button()
        self.assertTrue(self.pim_page.is_success_toast_displayed())

    def test_02_add_employee_with_valid_photo(self):
        self.pim_page.click_add_button()
        self.pim_page.enter_first_name("Foto")
        self.pim_page.enter_last_name("Tester")
        
        self.pim_page.upload_photo(self.valid_image_path)
        
        self.pim_page.click_save_button()
        self.assertTrue(self.pim_page.is_success_toast_displayed())

    def test_03_search_employee_by_id(self):
        self.pim_page.search_by_employee_id("0024") 
        time.sleep(2)
        pass 

    def test_04_search_employee_by_name(self):
        self.pim_page.search_by_employee_name("a")
        time.sleep(2)
        pass

    def test_05_delete_employee(self):
        self.pim_page.delete_first_record()
        self.assertTrue(self.pim_page.is_success_toast_displayed())

        # --- NEGATIVE TEST CASE ---

    def test_06_add_employee_empty_first_name(self):
        self.pim_page.click_add_button()
        self.pim_page.enter_last_name("Automated")
        self.pim_page.click_save_button()
        self.assertEqual(self.pim_page.get_first_name_error_message(), "Required")

    def test_07_add_employee_empty_last_name(self):
        self.pim_page.click_add_button()
        self.pim_page.enter_first_name("Zeztz")
        self.pim_page.click_save_button()
        self.assertEqual(self.pim_page.get_last_name_error_message(), "Required")

    def test_08_add_employee_duplicate_id(self):
        self.pim_page.click_add_button()
        self.pim_page.enter_first_name("Duplicate")
        self.pim_page.enter_last_name("Tester")
        
        # Mengisi dengan ID yang sudah ada di sistem, misal 0024
        self.pim_page.enter_employee_id_add("0024")
        self.pim_page.click_save_button()
        
        self.assertEqual(self.pim_page.get_employee_id_error_message(), "Employee Id already exists")

    def test_09_upload_invalid_file_extension(self):
        self.pim_page.click_add_button()
        self.pim_page.upload_photo(self.invalid_pdf_path)
        
        self.assertEqual(self.pim_page.get_file_error_message(), "File type not allowed")

    def test_10_upload_file_size_exceeded(self):
        self.pim_page.click_add_button()
        self.pim_page.upload_photo(self.large_image_path)
        
        self.assertEqual(self.pim_page.get_file_error_message(), "Attachment Size Exceeded")