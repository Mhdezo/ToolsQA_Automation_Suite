# base class for all pages
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self,driver):
        self.driver = driver

    def click(self, locator):
        """
            Click an element
        """
        element = (WebDriverWait(self.driver,10)
                   .until(EC.element_to_be_clickable(locator)))
        element.click()

    def type(self, locator, text):
        """
            Types test into an input field
        """
        element = (WebDriverWait(self.driver,10)
                   .until(EC.visibility_of_element_located(locator)))
        element.clear()
        element.send_keys(text)

    def is_element_visible(self, locator):
        """
            Check if an element is visible
        """
        try:
            (WebDriverWait(self.driver,10)
             .until(EC.visibility_of_element_located(locator)))
            return True
        except:
            return False