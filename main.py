import unittest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
from account_management.register_page import RegisterPage
from selenium.common.exceptions import TimeoutException


class RegisterPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initialize the WebDriver once for all tests.
        """
        options = Options()
        # Uncomment the next line to run tests in headless mode
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        cls.driver = webdriver.Edge(options=options)
        cls.driver.implicitly_wait(5)
        cls.register_page = RegisterPage(cls.driver)
        cls.register_page.load()
        cls.registered_username = None

    @classmethod
    def tearDownClass(cls):
        """
        Quit the WebDriver after all tests are done.
        """
        cls.driver.quit()

    def setUp(self):
        """
        Navigate to the registration page before each test.
        """
        self.register_page.load()

    @staticmethod
    def generate_unique_credentials():
        """
        Generate unique username and email using the current timestamp.
        """
        timestamp = int(time.time())
        username = f"testuser{timestamp}"
        email = f"testuser{timestamp}@example.com"
        return username, email

    def test_successful_registration(self):
        """Test case for successful registration."""
        username, email = self.generate_unique_credentials()
        self.register_page.register(username, email, "Password123!", "Password123!")
        try:
            success_text = self.register_page.get_success_message()
            self.assertIn("Thank you for registering", success_text)
            self.__class__.registered_username = username  # Save for reuse
        except TimeoutException:
            self.driver.save_screenshot("error_successful_registration.png")
            self.fail("Success message not displayed.")

    def test_registration_with_existing_username(self):
        """Test case for registration with an existing username."""
        # Ensure a username is available for testing
        if not self.__class__.registered_username:
            self.test_successful_registration()

        existing_username = self.__class__.registered_username
        username, email = self.generate_unique_credentials()
        self.register_page.register(existing_username, email, "Password123!", "Password123!")
        try:
            error_elements = self.register_page.get_error_messages()
            error_texts = [error.text.lower() for error in error_elements]
            self.assertTrue(any("already registered" in text for text in error_texts),
                            "Expected 'already registered' error message not found.")
        except TimeoutException:
            self.driver.save_screenshot("error_existing_username.png")
            self.fail("Error message for existing username not displayed.")

    def test_password_validations(self):
        """Test cases for various password validation scenarios."""
        test_cases = [
            {"password": "PASSWORD123!", "confirm_password": "PASSWORD123!", "error": "one lowercase letter"},
            {"password": "password123!", "confirm_password": "password123!", "error": "one capital letter"},
            {"password": "PasswordTest!", "confirm_password": "PasswordTest!", "error": "one number"},
            {"password": "Pass1!", "confirm_password": "Pass1!", "error": "at least 8 characters"},
        ]

        for case in test_cases:
            with self.subTest(case=case):
                username, email = self.generate_unique_credentials()
                self.register_page.register(
                    username=username,
                    email=email,
                    password=case["password"],
                    confirm_password=case["confirm_password"]
                )
                try:
                    error_elements = self.register_page.get_error_messages()
                    error_texts = [error.text.lower() for error in error_elements]
                    self.assertTrue(any(case["error"] in text for text in error_texts),
                                    f"Expected error '{case['error']}' not found.")
                except TimeoutException:
                    self.driver.save_screenshot(f"error_{case['error'].replace(' ', '_')}.png")
                    self.fail(f"Expected error message for '{case['error']}' not displayed.")

    def test_registration_with_empty_password(self):
        """Test case for registration with an empty password."""
        username, email = self.generate_unique_credentials()
        self.register_page.register(username, email, "", "")
        try:
            error_elements = self.register_page.get_error_messages()
            error_texts = [error.text.lower() for error in error_elements]
            self.assertTrue(any("password is required" in text for text in error_texts),
                            "Expected 'Password is required' error message not found.")
        except TimeoutException:
            self.driver.save_screenshot("error_empty_password.png")
            self.fail("Expected error message for empty password not displayed.")


if __name__ == "__main__":
    unittest.main()
