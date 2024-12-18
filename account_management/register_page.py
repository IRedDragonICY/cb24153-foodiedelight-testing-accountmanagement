# register_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    # Locators
    USERNAME = (By.ID, "user_login-1204")
    FIRST_NAME = (By.ID, "first_name-1204")
    LAST_NAME = (By.ID, "last_name-1204")
    EMAIL = (By.ID, "user_email-1204")
    PASSWORD = (By.ID, "user_password-1204")
    CONFIRM_PASSWORD = (By.ID, "confirm_user_password-1204")
    SUBMIT_BUTTON = (By.ID, "um-submit-btn")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(),'Thank you for registering.')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'um-field-error')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def load(self):
        self.driver.get("https://projectnest.io/register/")

    def fill_username(self, username):
        username_field = self.wait.until(EC.presence_of_element_located(self.USERNAME))
        username_field.clear()
        username_field.send_keys(username)

    def fill_first_name(self, first_name):
        first_name_field = self.driver.find_element(*self.FIRST_NAME)
        first_name_field.clear()
        first_name_field.send_keys(first_name)

    def fill_last_name(self, last_name):
        last_name_field = self.driver.find_element(*self.LAST_NAME)
        last_name_field.clear()
        last_name_field.send_keys(last_name)

    def fill_email(self, email):
        email_field = self.driver.find_element(*self.EMAIL)
        email_field.clear()
        email_field.send_keys(email)

    def fill_password(self, password):
        password_field = self.driver.find_element(*self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

    def fill_confirm_password(self, confirm_password):
        confirm_password_field = self.driver.find_element(*self.CONFIRM_PASSWORD)
        confirm_password_field.clear()
        confirm_password_field.send_keys(confirm_password)

    def submit(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def register(self, username, email, password, confirm_password):
        self.fill_username(username)
        self.fill_first_name("Test")
        self.fill_last_name("User")
        self.fill_email(email)
        self.fill_password(password)
        self.fill_confirm_password(confirm_password)
        self.submit()

    def get_success_message(self):
        return self.wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE)).text

    def get_error_messages(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.ERROR_MESSAGE))
