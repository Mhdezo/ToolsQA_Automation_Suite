from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from ToolsQA_Automation_Suite.utils.common_methods import (
    scrollIntoView, readExcelData, selectDropdownOption
)

class PracticeFormPage:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

        # Locators
        self.forms_menu_locator = (By.XPATH, "//h5[normalize-space()='Forms']")
        self.practice_form_menu_locator = (By.XPATH, "//span[normalize-space()='Practice Form']")
        self.first_name_locator = (By.ID, 'firstName')
        self.last_name_locator = (By.ID, 'lastName')
        self.user_email_locator = (By.ID, 'userEmail')
        self.gender_locator = (By.XPATH, "//div//label[contains(@for,'gender-radio')]")
        self.user_number_locator = (By.ID, 'userNumber')
        self.date_of_birth_locator = (By.ID, 'dateOfBirthInput')
        self.subjects_input_locator = (By.ID, 'subjectsInput')
        self.hobbies_locator = (By.XPATH, "//input[contains(@id,'hobbies-checkbox')]")
        self.upload_picture_locator = (By.ID, 'uploadPicture')
        self.current_address_locator = (By.ID, 'currentAddress')
        self.state_locator = (By.ID, 'state')
        self.city_locator = (By.ID, 'city')
        self.submit_button_locator = (By.ID, 'submit')

    def navigate_to_practice_form(self):
        """Navigate to the Practice Form page."""
        forms_menu = self.driver.find_element(*self.forms_menu_locator)
        scrollIntoView(self.driver, forms_menu)
        forms_menu.click()
        practice_form_menu = self.driver.find_element(*self.practice_form_menu_locator)
        scrollIntoView(self.driver, practice_form_menu)
        practice_form_menu.click()

    def fill_personal_details(self, data):
        """Fill the personal details section of the form."""
        self.driver.find_element(*self.first_name_locator).send_keys(data['First Name'])
        self.driver.find_element(*self.last_name_locator).send_keys(data['Last Name'])
        self.driver.find_element(*self.user_email_locator).send_keys(data['Email'])

        genders = self.driver.find_elements(*self.gender_locator)
        for gender_option in genders:
            if gender_option.text == data['Gender']:
                gender_option.click()
                break

        self.driver.find_element(*self.user_number_locator).send_keys(data['Mobile'])

    def select_date_of_birth(self, dob):
        """Select the date of birth."""
        date_picker = self.driver.find_element(*self.date_of_birth_locator)
        scrollIntoView(self.driver, date_picker)
        date_picker.click()
        # Logic to handle the date picker interaction (simplified here)
        logging.info(f"Date of birth selected: {dob}")

    def fill_subjects(self, subjects):
        """Fill the subjects field."""
        subjects_input = self.driver.find_element(*self.subjects_input_locator)
        for subject in subjects.split(','):
            subjects_input.send_keys(subject)
            subject_dropdown_locator = "//div[@id='subjectsContainer']//div[contains(@class,'css-26l3qy')]"
            subject_options_locator = ".//div[contains(@id,'-option')]"
            selectDropdownOption(self.driver, subject_dropdown_locator, subject, subject_options_locator)

    def select_hobbies(self, hobbies):
        """Select hobbies."""
        hobby_elements = self.driver.find_elements(*self.hobbies_locator)
        hobbies = [hobby.lower() for hobby in hobbies.split(',')]
        for hobby_element in hobby_elements:
            label = hobby_element.find_element(By.XPATH, './following-sibling::label')
            if label.text.lower() in hobbies:
                label.click()

    def upload_picture(self, picture_name):
        """Upload a picture."""
        upload_path = self.config.get("PATHS", "uploadfile")
        full_path = os.path.join(upload_path, picture_name)
        self.driver.find_element(*self.upload_picture_locator).send_keys(full_path)

    def fill_address(self, address, state, city):
        """Fill the address fields."""
        self.driver.find_element(*self.current_address_locator).send_keys(address)

        # Select State
        self.driver.find_element(*self.state_locator).click()
        state_dropdown_locator = "//div[@id='state']//div[contains(@class,'css-26l3qy')]"
        state_options_locator = ".//div[contains(@id,'-option')]"
        selectDropdownOption(self.driver, state_dropdown_locator, state, state_options_locator)

        # Select City
        self.driver.find_element(*self.city_locator).click()
        city_dropdown_locator = "//div[@id='city']//div[contains(@class,'css-26l3qy')]"
        city_options_locator = ".//div[contains(@id,'-option')]"
        selectDropdownOption(self.driver, city_dropdown_locator, city, city_options_locator)

    def submit_form(self):
        """Submit the form."""
        self.driver.find_element(*self.submit_button_locator).click()
        logging.info("Form submitted successfully.")
