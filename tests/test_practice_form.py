from logging_config import logging
import pytest
from pages.practice_form import PracticeFormPage, By
from utils.common_methods import read_excel_data

def test_practice_form(browser, config):
    """Test to fill and submit the Practice Form."""
    try:
        # Open the website
        browser.get(config.get("URLS", "website"))

        # Initialize the Practice Form page
        practice_form_page = PracticeFormPage(browser)

        # Navigate to the Practice Form
        practice_form_page.navigate_to_practice_form()

        # Read data from Excel
        data = read_excel_data("Sheet1", config)

        # Fill the form
        practice_form_page.fill_first_name(data["firstName"])
        practice_form_page.fill_last_name(data["lastName"])
        practice_form_page.fill_email(data["userEmail"])
        practice_form_page.select_gender(data["Gender"])
        practice_form_page.fill_mobile_number(data["userNumber"])
        practice_form_page.fill_date_of_birth(data["dateOfBirthInput"])
        practice_form_page.fill_subjects(data["subjectsInput"])
        practice_form_page.select_hobbies(data["hobbies"])
        practice_form_page.upload_picture(str(config.get("PATHS", "uploadfile")) + str(data["uploadPicture"][0]))
        practice_form_page.fill_current_address(data["currentAddress"])
        practice_form_page.select_state(data["state"])
        practice_form_page.select_city(data["city"])
        practice_form_page.submit_form()

        # Add assertions to verify form submission
        assert practice_form_page.is_element_visible((By.ID, "example-modal-sizes-title-lg")), "Form submission failed."

    except Exception as e:
        logging.error(f"Test failed with error: {e}")
        raise