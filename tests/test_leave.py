import unittest
import time
from datetime import datetime, timedelta
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage
from pages.pim_page import PIMPage  # Pastikan mengimpor PIMPage

class TestLeave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.unique_id = str(int(time.time()))[-6:]
        cls.first_name = "LeaveTest"
        cls.last_name = f"User{cls.unique_id}"
        cls.employee_name = f"{cls.first_name} {cls.last_name}"
        cls.emp_id = f"L{cls.unique_id}"

        # --- SETUP PRASYARAT (BUAT KARYAWAN & TAMBAH SALDO) ---
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        leave_page = LeavePage(driver)
        pim_page = PIMPage(driver)
        
        login_page.login_as("Admin", "admin123")
        
        dashboard_page.click_pim_menu()
        pim_page.click_add_button()
        pim_page.enter_first_name(cls.first_name)
        pim_page.enter_last_name(cls.last_name)
        pim_page.enter_employee_id_add(cls.emp_id)
        pim_page.click_save_button()
        time.sleep(4)
        
        dashboard_page.click_leave_menu()
        leave_page.click_add_entitlements_menu()
        
        leave_page.enter_employee_name(cls.employee_name)
        leave_page.select_leave_type()
        leave_page.enter_entitlement_amount("10")
        leave_page.click_save_button()
        leave_page.confirm_entitlement_if_needed()
        time.sleep(2) 
        
        driver.quit()

    @classmethod
    def tearDownClass(cls):
        # --- CLEANUP PRASYARAT (HAPUS KARYAWAN AGAR DATABASE BERSIH) ---
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        
        login_page.login_as("Admin", "admin123")
        
        dashboard_page.click_pim_menu()
        pim_page.search_by_employee_id(cls.emp_id)
        time.sleep(2)
        
        try:
            pim_page.delete_first_record()
            time.sleep(2)
        except:
            pass
            
        driver.quit()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://opensource-demo.orangehrmlive.com/")
        
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.leave_page = LeavePage(self.driver)
        
        self.login_page.login_as("Admin", "admin123")
        self.dashboard_page.click_leave_menu()

    def tearDown(self):
        self.driver.quit()

    # --- POSITIVE TEST CASE ---

    def test_01_assign_leave_success_normal(self):
        self.leave_page.click_assign_leave_tab()
        
        self.leave_page.enter_employee_name(self.employee_name) 
        self.leave_page.select_leave_type()
        
        today = datetime.now().strftime("%Y-%d-%m")
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(today)
        time.sleep(1) 
        self.leave_page.enter_to_date(aftTommorow)
        
        self.leave_page.enter_comment("Automated test: Normal Leave")
        self.leave_page.click_assign_button()
        
        self.assertTrue(self.leave_page.is_success_toast_displayed())

    def test_04_filter_leave_by_pending_approval(self):
        self.leave_page.click_leave_list_tab()
        self.leave_page.select_status_pending_approval()
        self.leave_page.click_search_button()
        time.sleep(2) 

    # --- NEGATIVE TEST CASE ---

    def test_02_assign_leave_overlapping(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name) 
        self.leave_page.select_leave_type()
        
        today = datetime.now().strftime("%Y-%d-%m")
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(today)
        time.sleep(1) 
        self.leave_page.enter_to_date(aftTommorow)
        self.leave_page.enter_comment("Automated test: Overlapping Leave")
        
        self.leave_page.click_assign_button()
        
        self.assertTrue(self.leave_page.is_warn_toast_displayed())

    def test_03_assign_leave_insufficient_balance(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name) 
        self.leave_page.select_leave_type()
        
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        day_17 = (datetime.now() + timedelta(days=17)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(aftTommorow)
        time.sleep(1) 
        self.leave_page.enter_to_date(day_17)
        
        self.leave_page.force_unfocus()
        time.sleep(2)
        
        self.assertTrue(self.leave_page.is_insufficient_balance_msg_displayed())

    def test_05_assign_leave_to_date_before_from_date(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name)
        self.leave_page.select_leave_type()
        
        tommorow = (datetime.now() + timedelta(days=1)).strftime("%Y-%d-%m")
        kemarin = (datetime.now() - timedelta(days=1)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(tommorow)
        time.sleep(1)
        self.leave_page.enter_to_date(kemarin)
        self.leave_page.force_unfocus()
        time.sleep(1)
        
        self.assertTrue(self.leave_page.is_date_error_displayed())

    def test_06_assign_leave_without_leave_type(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name)
        
        today = datetime.now().strftime("%Y-%d-%m")
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        self.leave_page.enter_from_date(today)
        time.sleep(1)
        self.leave_page.enter_to_date(aftTommorow)
        
        self.leave_page.click_assign_button()
        self.assertTrue(self.leave_page.is_required_error_displayed())