# base class for all pages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ToolsQA_Automation_Suite.logging_config import logging
from selenium.webdriver.common.alert import Alert

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
        except Exception as e:
            logging.error(f"Failed of element visibility: {e}")
            return False

    def is_alert_present(self):
        """Check if alert is visible"""
        try:
            WebDriverWait(self.driver,10).until(EC.alert_is_present())
            return True
        except Exception as e:
            logging.error(f"Failed of alert visibility: {e}")
            return False

    def accept_alert(self):
        try:
            Alert(self.driver).accept()
            logging.info(f'Alert has been accepted')
        except Exception as e:
            logging.error(f"Failed to accept alert: {e}")

    def cancel_alert(self):
        try:
            Alert(self.driver).dismiss()
            logging.info(f'Alert has been dismissed')
        except Exception as e:
            logging.error(f"Failed to dismiss alert: {e}")

    def type_alert(self, prompt):
        try:
            Alert(self.driver).send_keys(prompt)
            logging.info(f'Prompt has been written with: {prompt}')
        except Exception as e:
            logging.error(f"Failed type in the prompt field: {e}")