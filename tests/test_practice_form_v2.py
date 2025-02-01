# tests/test_practice_form.py
import pytest
from ToolsQA_Automation_Suite.pages.practice_form_v2 import PracticeFormPage
from ToolsQA_Automation_Suite.utils.common_methods import initialize_driver, read_config, configure_logging, readExcelData

def test_practice_form():
    try:
        # Read config and initialize driver
        config = read_config()
        configure_logging(config)
        driver = initialize_driver("chrome", config)

        # Open the website
        driver.get(config.get("URLS", "website"))

        # Initialize the Practice Form page
        practice_form_page = PracticeFormPage(driver)

        # Navigate to the Practice Form
        practice_form_page.navigate_to_practice_form()
        practice_form_page.scroll_to_form_beginning()

        # Read data from Excel
        data = readExcelData("Sheet1", config)

        # Fill the form
        practice_form_page.fill_first_name(data["firstName"])
        practice_form_page.fill_last_name(data["lastName"])
        practice_form_page.fill_email(data["userEmail"])
        practice_form_page.select_gender(data["Gender"][0])
        practice_form_page.fill_mobile_number(data["userNumber"])
        practice_form_page.fill_date_of_birth(data["dateOfBirthInput"])
        # we are here 
        practice_form_page.fill_subjects(data["subjectsInput"].split(","))
        practice_form_page.select_hobbies(data["hobbies"].split(","))
        practice_form_page.upload_picture(config.get("PATHS", "uploadfile") + data["uploadPicture"])
        practice_form_page.fill_current_address(data["currentAddress"])
        practice_form_page.select_state(data["state"])
        practice_form_page.select_city(data["city"])
        practice_form_page.submit_form()

        # Add assertions to verify form submission
        assert practice_form_page.is_element_visible((By.ID, "example-modal-sizes-title-lg")), "Form submission failed."

    finally:
        # Quit the browser
        driver.quit()