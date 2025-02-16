import pytest
from logging_config import logging
from pages.alerts_page import AlertPage, By
from utils.common_methods import read_excel_data, read_config

# Load config using the existing method from common_methods.py
config = read_config()

# Define a function to get test data dynamically
def get_test_data():
    """Reads test data from Excel and returns a list of row dictionaries."""
    return read_excel_data("Sheet2", config)

@pytest.mark.parametrize("data", get_test_data())
def test_alerts(browser, data):
    """Test Alerts."""
    try:
        # Open the website
        browser.get(config.get("URLS", "website"))

        # Initialize the Alert page
        alert_page = AlertPage(browser)

        # Navigate to the Alert Page
        alert_page.navigate_to_alert()

        # Alerts
        alert_page.click_button_to_see_alert()
        alert_page.alert_after_five_seconds()
        alert_page.click_confirm_button(data["action"])
        alert_page.click_prompt_button(data["action"],data["prompt"])

        # Add assertions to verify form submission
        # Check expected result
        if data.get("Expected_Result") == "Pass":
            assert True
        else:
            assert False

    except Exception as e:
        logging.error(f"Test failed with error: {e}")
        raise