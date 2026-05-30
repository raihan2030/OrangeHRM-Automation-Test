import unittest
import time
from datetime import datetime, timedelta
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.leave_page import LeavePage
from pages.pim_page import PIMPage
from pages.my_info_page import MyInfoPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestLeave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://opensource-demo.orangehrmlive.com/")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        leave_page = LeavePage(driver)
        my_info_page = MyInfoPage(driver)

        cls.first_name = "LeaveTest"
        cls.last_name = "AdminUser"
        cls.employee_name = f"{cls.first_name} {cls.last_name}"
        
        login_page.login_as("Admin", "admin123")
        
        # 1. Ubah nama profil Admin saat ini agar konsisten
        my_info_page.click_my_info_menu()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )
        my_info_page.enter_first_name(cls.first_name)
        my_info_page.clear_middle_name()
        my_info_page.enter_last_name(cls.last_name)
        my_info_page.click_save_main_form()
        time.sleep(3)
        
        # 2. Tambahkan Entitlement langsung ke nama Admin yang baru diubah
        dashboard_page.click_leave_menu()

        # --- PRECONDITION NEW 1: Cancel semua riwayat cuti aktif ---
        leave_page.click_my_leave_tab()
        leave_page.cancel_all_my_leaves()
        
        # --- PRECONDITION NEW 2: Hapus semua sisa saldo entitlement lama ---
        leave_page.click_employee_entitlements_menu()
        leave_page.enter_employee_name(cls.employee_name)
        leave_page.click_search_button()
        time.sleep(2)
        leave_page.delete_all_employee_entitlements()

        leave_page.click_add_entitlements_menu()
        leave_page.enter_employee_name(cls.employee_name)
        leave_page.select_leave_type()
        leave_page.enter_entitlement_amount("10")
        leave_page.click_save_button()
        leave_page.confirm_entitlement_if_needed()
        time.sleep(2) 
        
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

    def test_04_assign_leave_to_date_before_from_date(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name)
        self.leave_page.select_leave_type()
        
        tommorow = (datetime.now() + timedelta(days=1)).strftime("%Y-%d-%m")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(tommorow)
        time.sleep(1)
        self.leave_page.enter_to_date(yesterday)
        self.leave_page.force_unfocus()
        time.sleep(1)
        
        self.assertTrue(self.leave_page.is_date_error_displayed())

    def test_05_assign_leave_without_leave_type(self):
        self.leave_page.click_assign_leave_tab()
        self.leave_page.enter_employee_name(self.employee_name)
        
        today = datetime.now().strftime("%Y-%d-%m")
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(today)
        time.sleep(1)
        self.leave_page.enter_to_date(aftTommorow)
        
        self.leave_page.click_assign_button()
        self.assertTrue(self.leave_page.is_required_error_displayed())

    def test_06_apply_leave_success(self):
        # Langsung menuju menu Apply Leave
        self.dashboard_page.click_leave_menu()
        self.leave_page.click_apply_tab()
        
        self.leave_page.select_leave_type()
        
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        day_4 = (datetime.now() + timedelta(days=4)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(aftTommorow)
        time.sleep(1) 
        self.leave_page.enter_to_date(day_4)
        
        self.leave_page.enter_comment("Automated test: Apply Leave Success")
        self.leave_page.click_apply_button()
        
        self.assertTrue(self.leave_page.is_success_toast_displayed())

    def test_07_apply_leave_overlapping(self):
        self.leave_page.click_apply_tab()

        self.leave_page.select_leave_type()
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        day_4 = (datetime.now() + timedelta(days=4)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(aftTommorow)
        time.sleep(1) 
        self.leave_page.enter_to_date(day_4)
        
        self.leave_page.enter_comment("Automated test: Overlapping Leave")
        self.leave_page.click_apply_button()
        
        self.assertTrue(self.leave_page.is_warn_toast_displayed())

    def test_08_apply_leave_insufficient_balance(self):
        self.leave_page.click_apply_tab()
        self.leave_page.select_leave_type()
        
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        day_17 = (datetime.now() + timedelta(days=17)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(aftTommorow)
        time.sleep(1) 
        self.leave_page.enter_to_date(day_17)
        
        self.leave_page.force_unfocus()
        time.sleep(2)
        
        self.assertTrue(self.leave_page.is_insufficient_balance_msg_displayed())

    def test_09_apply_leave_to_date_before_from_date(self):
        self.leave_page.click_apply_tab()
        self.leave_page.select_leave_type()
        
        tommorow = (datetime.now() + timedelta(days=1)).strftime("%Y-%d-%m")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%d-%m")
        
        self.leave_page.enter_from_date(tommorow)
        time.sleep(1)
        self.leave_page.enter_to_date(yesterday)
        self.leave_page.force_unfocus()
        time.sleep(1)

        self.assertTrue(self.leave_page.is_date_error_displayed())

    def test_10_apply_leave_without_leave_type(self):
        self.leave_page.click_apply_tab()
        
        today = datetime.now().strftime("%Y-%d-%m")
        aftTommorow = (datetime.now() + timedelta(days=2)).strftime("%Y-%d-%m")
        self.leave_page.enter_from_date(today)
        time.sleep(1)
        self.leave_page.enter_to_date(aftTommorow)
        
        self.leave_page.click_apply_button()
        self.assertTrue(self.leave_page.is_required_error_displayed())

    def test_11_filter_leave_by_pending_approval(self):
        self.leave_page.click_leave_list_tab()
        self.leave_page.select_status_pending_approval()
        self.leave_page.click_search_button()
        time.sleep(2) 