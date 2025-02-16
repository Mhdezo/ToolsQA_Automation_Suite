import pytest
from logging_config import logging
from pages.practice_form import PracticeFormPage, By
from utils.common_methods import read_excel_data, read_config

# Load config using the existing method from common_methods.py
config = read_config()

# Define a function to get test data dynamically
def get_test_data():
    """Reads test data from Excel and returns a list of row dictionaries."""
    return read_excel_data("Sheet1", config)


@pytest.mark.parametrize("data", get_test_data())
def test_practice_form(browser, data):
    """Test to fill and submit the Practice Form with multiple data sets."""

    try:
        # Open the website
        browser.get(config.get("URLS", "website"))

        # Initialize the Practice Form page
        practice_form_page = PracticeFormPage(browser)

        # Navigate to the Practice Form
        practice_form_page.navigate_to_practice_form()

        # Fill the form using data from Excel
        practice_form_page.fill_first_name(data["firstName"])
        practice_form_page.fill_last_name(data["lastName"])
        practice_form_page.fill_email(data["userEmail"])
        practice_form_page.select_gender(data["Gender"])
        practice_form_page.fill_mobile_number(data["userNumber"])
        practice_form_page.fill_date_of_birth(data["dateOfBirthInput"])
        practice_form_page.fill_subjects(data["subjectsInput"])
        practice_form_page.select_hobbies(data["hobbies"])
        practice_form_page.upload_picture(str(config.get("PATHS", "uploadfile")) + str(data["uploadPicture"]))
        practice_form_page.fill_current_address(data["currentAddress"])
        practice_form_page.select_state(data["state"])
        practice_form_page.select_city(data["city"])
        practice_form_page.submit_form()

        # Check expected result
        if data.get("Expected_Result") == "Pass":
            assert practice_form_page.is_element_visible(
                (By.ID, "example-modal-sizes-title-lg")), "Form submission failed."
        else:
            assert not practice_form_page.is_element_visible(
                (By.ID, "example-modal-sizes-title-lg")), "Form should have failed but passed."

    except Exception as e:
        logging.error(f"Test failed with error: {e}")
        raise
