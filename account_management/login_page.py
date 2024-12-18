# login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    # Locators
    USERNAME_EMAIL_FIELD = (By.ID, "username-1205")
    PASSWORD_FIELD = (By.ID, "user_password-1205")
    SUBMIT_BUTTON = (By.ID, "um-submit-btn")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'um-field-error')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def load(self):
        self.driver.get("https://projectnest.io/login-2/")

    def fill_username_or_email(self, username_or_email):
        username_email_field = self.wait.until(EC.presence_of_element_located(self.USERNAME_EMAIL_FIELD))
        username_email_field.clear()
        username_email_field.send_keys(username_or_email)

    def fill_password(self, password):
        password_field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)

    def submit(self):
        self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON)).click()

    def login(self, username_or_email, password):
        self.fill_username_or_email(username_or_email)
        self.fill_password(password)
        self.submit()

    def get_error_messages(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.ERROR_MESSAGE))

    def wait_for_redirect(self, timeout=10):
        """
        Waits for the URL to change to the expected user profile page after login.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url.startswith("https://projectnest.io/user/")
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """
        Returns the current URL.
        """
        return self.driver.current_url