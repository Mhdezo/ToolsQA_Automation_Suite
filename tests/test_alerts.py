from ToolsQA_Automation_Suite.logging_config import logging
from ToolsQA_Automation_Suite.pages.alerts_page import AlertPage, By
from ToolsQA_Automation_Suite.utils.common_methods import read_excel_data
def test_alerts(browser, config):
    """Test Alerts."""
    try:
        # Open the website
        browser.get(config.get("URLS", "website"))

        # Initialize the Alert page
        alert_page = AlertPage(browser)

        # Navigate to the Alert Page
        alert_page.navigate_to_alert()

        # Read data from Excel
        data = read_excel_data("Sheet2", config)

        # Alerts
        alert_page.click_button_to_see_alert()
        alert_page.alert_after_five_seconds()
        alert_page.click_confirm_button(data["action"])
        alert_page.click_prompt_button(data["action"],data["prompt"])

        # Add assertions to verify form submission
        assert True

    except Exception as e:
        logging.error(f"Test failed with error: {e}")
        raise