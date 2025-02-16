# page class for the Practice Form
from selenium.webdriver.common.by import By
from ToolsQA_Automation_Suite.logging_config import logging
from ToolsQA_Automation_Suite.utils.common_methods import scroll_into_view, select_dropdown_option
from ToolsQA_Automation_Suite.pages.base_page import BasePage

class AlertPage(BasePage):
    # Locators
    ALERT_CARD = (By.XPATH, "//h5[normalize-space()='Alerts, Frame & Windows']")
    ALERTS = (By.XPATH, "//div[@class='element-list collapse show']//li[@id='item-1']")
    BEGINNING_OF_ALERTS = (By.XPATH, "//h1[normalize-space()='Alerts']")
    ALERT_BUTTON = (By.ID, "alertButton")
    TIMER_ALERT_BUTTON = (By.ID, "timerAlertButton")
    CONFIRM_BUTTON = (By.ID, "confirmButton")
    PROMPT_BUTTON = (By.ID, "promtButton")

    def __init__(self, driver):
        super().__init__(driver)

    def click_button_to_see_alert(self):
        """Click Button to see alert."""
        self.click(self.ALERT_BUTTON)
        logging.info(f'Click Button to see alert button has been clicked')
        if self.is_alert_present():
            self.accept_alert()
        else:
            logging.warning(f'Alert of "Click Button to see alert" has not been visible')

    def alert_after_five_seconds(self):
        """On button click, alert will appear after 5 seconds."""
        self.click(self.TIMER_ALERT_BUTTON)
        logging.info(f'On button click, alert will appear after 5 seconds has been clicked')
        if self.is_alert_present():
            self.accept_alert()
        else:
            logging.warning(f'Alert of "On button click, alert will appear after 5 seconds" has not been visible')

    def click_confirm_button(self, action):
        """On button click, confirm box will appear."""
        self.click(self.CONFIRM_BUTTON)
        logging.info(f'On button click, confirm box will appear has been clicked')
        if self.is_alert_present():
            if action.lower() == 'accept':
                self.accept_alert()
            else:
                self.cancel_alert()
        else:
            logging.warning(f'Alert of "On button click, confirm box will appear" has not been visible')

    def click_prompt_button(self, action, prompt):
        """On button click, prompt box will appear."""
        self.click(self.PROMPT_BUTTON)
        logging.info(f'On button click, prompt box will appear has been clicked')
        if self.is_alert_present():
            self.type_alert(prompt)
            if action.lower() == 'accept':
                self.accept_alert()
            else:
                self.cancel_alert()
        else:
            logging.warning(f'Alert of "On button click, confirm box will appear" has not been visible')

    def navigate_to_alert(self):
        """Navigates to the Practice Form page."""
        try:
            scroll_into_view(self.driver, *self.ALERT_CARD)
            self.click(self.ALERT_CARD)
            self.driver.find_element(*self.ALERTS).click()
        except Exception as e:
            logging.error(f'Navigate to Alerts Failed: "{e}"')
            raise