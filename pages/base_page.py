# base class for all pages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging_config import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator):
        """Clicks an element."""
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            logging.error(f"Failed to click element: {e}")
            raise

    def type(self, locator, text):
        """Types text into an input field."""
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except Exception as e:
            logging.error(f"Failed to type text: {e}")
            raise

    def is_element_visible(self, locator):
        """Checks if an element is visible."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_for_element(self, locator, timeout=10):
        """Waits for an element to be visible."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            logging.error(f"Element not found: {e}")
            raise