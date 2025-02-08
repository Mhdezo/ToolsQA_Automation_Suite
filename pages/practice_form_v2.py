# page class for the Practice Form
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
from utils.common_methods import scrollIntoView, selectDropdownOption
from pages.base_page import BasePage

class PracticeFormPage(BasePage):
    # Locators
    FORMS_CARD = (By.XPATH, "//h5[normalize-space()='Forms']")
    PRACTICE_FORM = (By.XPATH, "//div[@class='element-list collapse show']//li[@id='item-0']")
    BEGINNING_OF_FORM = (By.XPATH, "//h5[normalize-space()='Student Registration Form']")
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    USER_EMAIL = (By.ID, "userEmail")
    # GENDER_RADIO = (By.XPATH, "//label[contains(@for, 'gender-radio')]")
    USER_NUMBER = (By.ID, "userNumber")
    DATE_OF_BIRTH = (By.ID, "dateOfBirthInput")
    CURRENT_MONTH_YEAR = (By.XPATH,"//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']")
    RIGHT_ARROW = (By.XPATH,"//button[normalize-space()='Next Month']")
    LEFT_ARROW = (By.XPATH,"//button[normalize-space()='Previous Month']")
    DAYS = (By.XPATH,"//div[@class='react-datepicker__week']//div")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    DROPDOWN = (By.XPATH, "//div[contains(@class,'css-26l3qy')]")
    DROPDOWN_OPTIONS = (By.XPATH, "//div[contains(@id,'-option')]")
    # HOBBIES_CHECKBOX = (By.XPATH, "//input[contains(@id, 'hobbies-checkbox')]")
    # HOBBIES_LABELS = (By.XPATH, "//input[contains(@id, 'hobbies-checkbox')]//following-sibling::label")
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

    def fill_last_name(self, last_name):
        """Fills the Last Name field."""
        self.type(self.LAST_NAME, last_name)

    def fill_email(self, email):
        """Fills the Email field."""
        self.type(self.USER_EMAIL, email)

    def select_gender(self, gender):
        """Selects a gender."""
        gender_locator = (By.XPATH, f'//label[text()="{gender[0]}"]')
        self.click(gender_locator)

    def fill_mobile_number(self, number):
        """Fills the Mobile Number field."""
        self.type(self.USER_NUMBER, number)

    def fill_date_of_birth(self, dob):
        """
        Selects the date of birth from the date picker.
        :param dob: The date of birth in the format "DD MMMM YYYY" (e.g., "15 January 1990").
        """
        month_year = dob[0][dob[0].find(' ')+1:] # Get only month and year
        date_of_birth_locator = self.driver.find_element(*self.DATE_OF_BIRTH)
        scrollIntoView(self.driver,*self.DATE_OF_BIRTH)
        date_of_birth_locator.click()
        current_month_and_year = self.driver.find_element(*self.CURRENT_MONTH_YEAR).text
        arrow = ''
        if month_year[-4:] > current_month_and_year[-4:]:
            arrow = self.driver.find_element(*self.RIGHT_ARROW)
        elif month_year[-4:] < current_month_and_year[-4:]:
            arrow = self.driver.find_element(*self.LEFT_ARROW)
        # Loop on the date picker till you find the required date
        while True:
            current_month_and_year = self.driver.find_element(*self.CURRENT_MONTH_YEAR).text
            if current_month_and_year == month_year:
                days = self.driver.find_elements(*self.DAYS)
                temp_day_month = str(dob[0])
                temp_day_month = temp_day_month.split(' ')
                temp_day = temp_day_month[0].lstrip('0') # Remove leading zero from the da
                temp_month = temp_day_month[1]
                # Loop on days divs to click on the required date
                for day_element in days:
                    # If tempDay is in the div label and month as well click on it and leave
                    if temp_day in day_element.get_attribute('aria-label') and temp_month in day_element.get_attribute('aria-label'):
                        day_element.click()
                        break
                break
            else:
                arrow.click()

    def fill_subjects(self, subjects):
        """Fills the Subjects field."""
        subjects = str(subjects[0]).split(',')
        #subjects = subjects.split(',')
        for subject in subjects:
            self.type(self.SUBJECTS_INPUT, subject)
            # select from dropdown
            if self.is_element_visible(self.DROPDOWN):
                selectDropdownOption(self.driver,self.DROPDOWN,subject,self.DROPDOWN_OPTIONS)
            else:
                logging.warning(f"Subjects Dropdown not found!")

    def select_hobbies(self, hobbies):
        """Selects hobbies."""
        hobbies = str(hobbies[0]).split(',')
        # Use list comprehensions to lower the list
        hobbies = [h.lower() for h in hobbies]
        for hobby in hobbies:
            hobby_locator = (By.XPATH, f'//label[text()="{hobby.capitalize()}"]')
            self.click(hobby_locator)

    def upload_picture(self, file_path):
        """Uploads a picture."""
        self.driver.find_element(*self.UPLOAD_PICTURE).send_keys(file_path)

    def fill_current_address(self, address):
        """Fills the Current Address field."""
        self.type(self.CURRENT_ADDRESS, address)

    def select_state(self, state):
        """Selects a state."""
        scrollIntoView(self.driver, *self.STATE_INPUT)
        self.click(self.STATE_INPUT)
        state = str(state[0])
        # select from dropdown
        if self.is_element_visible(self.DROPDOWN):
            selectDropdownOption(self.driver, self.DROPDOWN, state, self.DROPDOWN_OPTIONS)
        else:
            logging.warning(f"Subjects Dropdown not found!")

    def select_city(self, city):
        """Selects a city."""
        self.click(self.CITY_INPUT)
        city = str(city[0])
        # select from dropdown
        if self.is_element_visible(self.DROPDOWN):
            selectDropdownOption(self.driver, self.DROPDOWN, city, self.DROPDOWN_OPTIONS)
        else:
            logging.warning(f"Subjects Dropdown not found!")

    def submit_form(self):
        """Submits the form."""
        self.click(self.SUBMIT_BUTTON)

    def navigate_to_practice_form(self):
        """Navigates to the Practice Form page."""
        # forms_card = self.driver.find_element(*self.FORMS_CARD)
        scrollIntoView(self.driver, *self.FORMS_CARD)
        self.click(self.FORMS_CARD)
        self.driver.find_element(*self.PRACTICE_FORM).click()

    def scroll_to_form_beginning(self):
        beginning_of_form = self.driver.find_element(*self.BEGINNING_OF_FORM)
        scrollIntoView(self.driver, beginning_of_form)

