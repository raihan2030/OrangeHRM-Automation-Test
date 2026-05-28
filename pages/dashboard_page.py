from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    # --- LOCATORS ---
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    TOPBAR_HEADER = (By.XPATH, "//h6[contains(@class, 'oxd-topbar-header-breadcrumb-module')]")
    USER_DROPDOWN = (By.XPATH, "//i[contains(@class, 'oxd-userdropdown-icon')]")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    # --- ACTIONS & GETTERS ---
    def get_dashboard_header(self):
        return self.wait_for_element(self.DASHBOARD_HEADER).text

    def click_admin_menu(self):
        self.wait_for_clickable(self.ADMIN_MENU).click()

    def get_topbar_header(self):
        return self.wait_for_element(self.TOPBAR_HEADER).text

    def logout(self):
        self.wait_for_clickable(self.USER_DROPDOWN).click()
        self.wait_for_clickable(self.LOGOUT_LINK).click()