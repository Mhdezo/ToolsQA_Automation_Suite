# page class for the Practice Form
from selenium.webdriver.common.by import By
from logging_config import logging
from utils.common_methods import scroll_into_view, select_dropdown_option
from pages.base_page import BasePage

class PracticeFormPage(BasePage):
    # Locators
    FORMS_CARD = (By.XPATH, "//h5[normalize-space()='Forms']")
    PRACTICE_FORM = (By.XPATH, "//div[@class='element-list collapse show']//li[@id='item-0']")
    BEGINNING_OF_FORM = (By.XPATH, "//h5[normalize-space()='Student Registration Form']")
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    USER_EMAIL = (By.ID, "userEmail")
    USER_NUMBER = (By.ID, "userNumber")
    DATE_OF_BIRTH = (By.ID, "dateOfBirthInput")
    CURRENT_MONTH_YEAR = (By.XPATH, "//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']")
    RIGHT_ARROW = (By.XPATH, "//button[normalize-space()='Next Month']")
    LEFT_ARROW = (By.XPATH, "//button[normalize-space()='Previous Month']")
    DAYS = (By.XPATH, "//div[@class='react-datepicker__week']//div")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    DROPDOWN = (By.XPATH, "//div[contains(@class,'css-26l3qy')]")
    DROPDOWN_OPTIONS = (By.XPATH, "//div[contains(@id,'-option')]")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    SUBMIT_BUTTON = (By.ID, "submit")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_first_name(self, first_name):
        """Fills the First Name field."""
        self.type(self.FIRST_NAME, first_name)
        logging.info(f'First Name : "{first_name}"')

    def fill_last_name(self, last_name):
        """Fills the Last Name field."""
        self.type(self.LAST_NAME, last_name)
        logging.info(f'Last Name : "{last_name}"')

    def fill_email(self, email):
        """Fills the Email field."""
        self.type(self.USER_EMAIL, email)
        logging.info(f'User Email : "{email}"')

    def select_gender(self, gender):
        """Selects a gender."""
        gender_locator = (By.XPATH, f'//label[text()="{gender[0]}"]')
        self.click(gender_locator)
        logging.info(f'Gender : "{gender}"')

    def fill_mobile_number(self, number):
        """Fills the Mobile Number field."""
        self.type(self.USER_NUMBER, number)
        logging.info(f'User number : "{number}"')

    def fill_date_of_birth(self, dob):
        """Selects the date of birth from the date picker."""
        try:
            # Ensure dob is a string and in the correct format
            if isinstance(dob, list):
                dob = dob[0]  # Extract the first element if dob is a list
            dob = str(dob).strip()  # Convert to string and remove leading/trailing spaces

            # Split into parts
            temp_day_month = dob.split(' ')
            if len(temp_day_month) < 2:
                logging.error(f"Invalid date format: {dob}. Expected 'DD MMMM YYYY'.")
                raise ValueError(f"Invalid date format: {dob}. Expected 'DD MMMM YYYY'.")

            # Extract day and month
            temp_day = temp_day_month[0].lstrip('0')  # Remove leading zero from the day
            temp_month = temp_day_month[1]  # Extract the month

            # Scroll and click the date picker
            scroll_into_view(self.driver, *self.DATE_OF_BIRTH)
            self.click(self.DATE_OF_BIRTH)

            # Navigate to the correct month and year
            month_year = ' '.join(temp_day_month[1:])  # Combine month and year
            self.navigate_to_month_year(month_year)

            # Select the day
            self.select_day(temp_day, temp_month)
            logging.info(f'Date of Birth : "{dob}"')
        except Exception as e:
            logging.error(f'Date of Birth Failed: "{e}"')
            raise

    def navigate_to_month_year(self, target_month_year):
        """Navigates to the target month and year in the date picker."""
        try:
            while self.get_current_month_year() != target_month_year:
                if target_month_year[-4:] > self.get_current_month_year()[-4:]:
                    self.click(self.RIGHT_ARROW)
                else:
                    self.click(self.LEFT_ARROW)
        except Exception as e:
            logging.error(f'Navigate to month and year Failed: "{e}"')
            raise

    def get_current_month_year(self):
        """Returns the current month and year displayed in the date picker."""
        try:
            return self.driver.find_element(*self.CURRENT_MONTH_YEAR).text
        except Exception as e:
            logging.error(f'Get current month and year Failed: "{e}"')
            raise

    def select_day(self, day, month):
        """Selects the day in the date picker."""
        try:
            days = self.driver.find_elements(*self.DAYS)
            for day_element in days:
                if day in day_element.get_attribute('aria-label') and month in day_element.get_attribute('aria-label'):
                    day_element.click()
                    return
        except Exception as e:
            logging.error(f'Select day Failed: "{e}"')
            raise

    def fill_subjects(self, subjects):
        """Fills the Subjects field."""
        try:
            subjects = str(subjects[0]).split(',')
            for subject in subjects:
                self.type(self.SUBJECTS_INPUT, subject)
                if self.is_element_visible(self.DROPDOWN):
                    select_dropdown_option(self.driver, self.DROPDOWN, subject, self.DROPDOWN_OPTIONS)
                    logging.info(f'Subject : "{subject}"')
                else:
                    logging.warning(f"Subjects Dropdown not found!")
        except Exception as e:
            logging.error(f'Subjects Failed: "{e}"')
            raise
    def select_hobbies(self, hobbies):
        """Selects hobbies."""
        try:
            hobbies = str(hobbies[0]).split(',')
            hobbies = [h.lower() for h in hobbies]
            for hobby in hobbies:
                hobby_locator = (By.XPATH, f'//label[text()="{hobby.capitalize()}"]')
                self.click(hobby_locator)
                logging.info(f'Hobby : "{hobby}"')
        except Exception as e:
            logging.error(f'Hobbies Failed: "{e}"')
            raise
    def upload_picture(self, file_path):
        """Uploads a picture."""
        try:
            self.driver.find_element(*self.UPLOAD_PICTURE).send_keys(file_path)
            logging.info(f'Picture uploaded')
        except Exception as e:
            logging.error(f'Upload picture Failed: "{e}"')
            raise
    def fill_current_address(self, address):
        """Fills the Current Address field."""
        try:
            self.type(self.CURRENT_ADDRESS, address)
            logging.info(f'Address : "{address}"')
        except Exception as e:
            logging.error(f'Fill address Failed: "{e}"')
            raise
    def select_state(self, state):
        """Selects a state."""
        try:
            scroll_into_view(self.driver, *self.STATE_INPUT)
            self.click(self.STATE_INPUT)
            state = str(state[0])
            if self.is_element_visible(self.DROPDOWN):
                select_dropdown_option(self.driver, self.DROPDOWN, state, self.DROPDOWN_OPTIONS)
                logging.info(f'State : "{state}"')
            else:
                logging.warning(f"State Dropdown not found!")
        except Exception as e:
            logging.error(f'Select state Failed: "{e}"')
            raise
    def select_city(self, city):
        """Selects a city."""
        try:
            self.click(self.CITY_INPUT)
            city = str(city[0])
            if self.is_element_visible(self.DROPDOWN):
                select_dropdown_option(self.driver, self.DROPDOWN, city, self.DROPDOWN_OPTIONS)
                logging.info(f'City : "{city}"')
            else:
                logging.warning(f"City Dropdown not found!")
        except Exception as e:
            logging.error(f'Select city Failed: "{e}"')
            raise
    def submit_form(self):
        """Submits the form."""
        try:
            self.click(self.SUBMIT_BUTTON)
            logging.info(f'Form Submitted')
        except Exception as e:
            logging.error(f'Submit form Failed: "{e}"')
            raise
    def navigate_to_practice_form(self):
        """Navigates to the Practice Form page."""
        try:
            scroll_into_view(self.driver, *self.FORMS_CARD)
            self.click(self.FORMS_CARD)
            self.driver.find_element(*self.PRACTICE_FORM).click()
        except Exception as e:
            logging.error(f'Navigate to practice form Failed: "{e}"')
            raise