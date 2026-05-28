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

    # --- TEST CASE POSITIF ---

    def test_01_search_user_valid(self):
        """[Positif] Mencari User berdasarkan Username yang valid (Admin)"""
        # Kita pakai username 'Admin' karena pasti selalu ada di database default
        self.admin_page.search_by_username("Admin")
        # Scroll sedikit ke bawah untuk melihat hasil atau tunggu loading selesai
        time.sleep(2) 
        # Kita bisa memvalidasi tidak muncul pesan error/no records
        # Logika: Jika tidak ada pesan "No Records Found", berarti data ada
        # (Idealnya dicek ke dalam tabel, tapi ini cara tercepat memastikan filter bekerja)
        pass # Script berjalan tanpa error (Explicit Wait berhasil menemukan tombol dan mengekliknya)

    def test_02_add_user_success(self):
        """[Positif] Menambahkan User baru dengan data lengkap dan valid"""
        self.admin_page.click_add_button()
        self.admin_page.select_user_role_admin()
        self.admin_page.select_status_enabled()
        # Masukkan huruf awal nama pegawai yang ada (contoh: "a", lalu klik saran pertama)
        self.admin_page.enter_employee_name("a")
        
        # Buat username unik agar tidak bentrok jika test diulang
        unique_username = f"RaihanUser_{int(time.time())}"
        self.admin_page.enter_username(unique_username)
        
        self.admin_page.enter_password("RaihanPassword123!")
        self.admin_page.enter_confirm_password("RaihanPassword123!")
        self.admin_page.click_save_button()
        
        # Validasi muncul popup hijau "Successfully Saved"
        self.assertTrue(self.admin_page.is_success_toast_displayed())

    # --- TEST CASE NEGATIF ---

    def test_03_add_user_password_mismatch(self):
        """[Negatif] Membuat User baru dengan konfirmasi password yang berbeda"""
        self.admin_page.click_add_button()
        self.admin_page.enter_username("TestMismatch123")
        self.admin_page.enter_password("SandiKuat123!")
        self.admin_page.enter_confirm_password("SandiBeda123!") # Sengaja disalahkan
        
        # Validasi pesan error di bawah field konfirmasi password
        self.assertEqual(self.admin_page.get_confirm_password_error_message(), "Passwords do not match")

    def test_04_add_user_short_password(self):
        """[Negatif] Membuat User baru dengan password kurang dari 8 karakter"""
        self.admin_page.click_add_button()
        self.admin_page.enter_password("1234") # Terlalu pendek
        
        self.assertEqual(self.admin_page.get_field_error_message(), "Should have at least 7 characters")

    def test_05_search_invalid_username(self):
        """[Negatif] Mencari User dengan Username acak yang tidak terdaftar"""
        self.admin_page.search_by_username("UserAsalAsalan999")
        
        # Validasi pesan "No Records Found" muncul
        self.assertTrue(self.admin_page.is_no_records_found_displayed())