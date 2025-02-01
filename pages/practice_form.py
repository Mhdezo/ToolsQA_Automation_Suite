# page class for the Practice Form
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
from ToolsQA_Automation_Suite.utils.common_methods import (scrollIntoView,readExcelData,
                                                           selectDropdownOption, read_config, configure_logging,
                                                           initialize_driver, quitBrowser, openWebsite)

# Fill the form with the data
def fillForm(driver,config):
    try:
        # Scroll to the Forms element - ADs cover the element
        formElement = driver.find_element(By.XPATH, "//h5[normalize-space()='Forms']")
        scrollIntoView(driver, formElement)
        # Go to the Forms page
        formElement.click()
        # Show the Practice Form
        driver.find_element(By.XPATH, "//span[normalize-space()='Practice Form']").click()
        # Scroll to the beginning of the form
        formBeginElement = driver.find_element(By.XPATH, "//h5[normalize-space()='Student Registration Form']")
        scrollIntoView(driver, formBeginElement)
        
        # Read data from the Excel sheet form_data.xlsx
        dataFrame = readExcelData('Sheet1',config)
        # Find and Fill First Name field
        firstName = driver.find_element(By.XPATH,"//input[@id='firstName']")
        firstName.send_keys(dataFrame[firstName.get_attribute('id')])
        # Find and Fill Last Name field
        lastName = driver.find_element(By.XPATH,"//input[@id='lastName']")
        lastName.send_keys(dataFrame[lastName.get_attribute('id')])
        # Find and Fill User Email field
        userEmail = driver.find_element(By.XPATH,"//input[@id='userEmail']")
        userEmail.send_keys(dataFrame[userEmail.get_attribute('id')])
        # Find and Choose Gender
        genders = driver.find_elements(By.XPATH,"//div//label[contains(@for,'gender-radio')]")
        for gender in genders:
            if gender.text == dataFrame['Gender'][0]: # To get first element of the list 'Male'
                gender.click()
        # Find and Fill User Mobile Number field
        userNumber = driver.find_element(By.XPATH,"//input[@id='userNumber']")
        userNumber.send_keys(dataFrame[userNumber.get_attribute('id')])
        # Find and Pick the Date Of Birth
        dateOfBirthInput = driver.find_element(By.XPATH,"//input[@id='dateOfBirthInput']")
        requiredDOB = dataFrame[dateOfBirthInput.get_attribute('id')]
        monthYear = requiredDOB[0][requiredDOB[0].find(' ')+1:] # Get only month and year
        # To know which arrow we need to click compare with current year and required year
        scrollIntoView(driver,dateOfBirthInput)
        dateOfBirthInput.click()
        currentMonthYear = driver.find_element(By.XPATH,"//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']").text
        arrow = ''
        if monthYear[-4:] > currentMonthYear[-4:]:
            arrow = driver.find_element(By.XPATH,"//button[normalize-space()='Next Month']")
        elif monthYear[-4:] < currentMonthYear[-4:]:
            arrow = driver.find_element(By.XPATH,"//button[normalize-space()='Previous Month']")
        # Loop on the date picker till you find the required date
        while True:
            currentMonthYear = driver.find_element(By.XPATH,"//div[@class='react-datepicker__current-month react-datepicker__current-month--hasYearDropdown react-datepicker__current-month--hasMonthDropdown']").text
            if currentMonthYear == monthYear:
                days = driver.find_elements(By.XPATH,"//div[@class='react-datepicker__week']//div")
                tempDayMonth = str(requiredDOB[0])
                tempDayMonth = tempDayMonth.split(' ')
                tempDay = tempDayMonth[0].lstrip('0')
                tempMonth = tempDayMonth[1]
                # Loop on days divs to click on the required date
                for day in days:
                    # If tempDay is in the div label and month as well click on it and leave
                    if tempDay in day.get_attribute('aria-label') and tempMonth in day.get_attribute('aria-label'):
                        day.click()
                        break
                break
            else:
                arrow.click()
        # Fill Subjects
        subjectsInput = driver.find_element(By.XPATH, "//input[@id='subjectsInput']")
        subjects = dataFrame[subjectsInput.get_attribute('id')]
        subjects = str(subjects[0])
        subjects = subjects.split(',')
        for subject in subjects:
            subjectsInput.send_keys(subject)
            subjectDropdown = "//div[@id='subjectsContainer']//div[contains(@class,'css-26l3qy')]"
            subjectOptionsLocation = ".//div[contains(@id,'-option')]"
            selectDropdownOption(driver, subjectDropdown, subject, subjectOptionsLocation)
        # Check Hobbies
        hobbiesInput = driver.find_elements(By.XPATH, "//input[contains(@id,'hobbies-checkbox')]")
        hobbies = dataFrame[hobbiesInput[0].get_attribute('id')[:7]]
        hobbies = str(hobbies[0])
        hobbies = hobbies.split(',')
        # Use list comprehensions to lower the list
        hobbies = [h.lower() for h in hobbies]
        for hobbyInput in hobbiesInput:
            temp = hobbyInput.find_element(By.XPATH,'.//following-sibling::label')
            if temp.text.lower() in hobbies:
                temp.click()
        # Choose a picture
        pictureInput = driver.find_element(By.XPATH,"//input[@id='uploadPicture']")
        picture = dataFrame[pictureInput.get_attribute('id')]
        uploadFileFath = config.get("PATHS", "uploadfile")
        pictureInput.send_keys(uploadFileFath + picture[0])
        # Fill Current Address
        currentAddress = driver.find_element(By.XPATH,"//textarea[@id='currentAddress']")
        address = dataFrame[currentAddress.get_attribute('id')]
        currentAddress.send_keys(address)
        scrollIntoView(driver,currentAddress)
        # Select the State
        stateInput = driver.find_element(By.XPATH, "//div[@id='state']")
        state = dataFrame[stateInput.get_attribute('id')]
        state = str(state[0])
        stateInput.click()
        stateDropdown = "//div[@id='state']//div[contains(@class,'css-26l3qy')]"
        stateOptionsLocation = ".//div[contains(@id,'-option')]"
        selectDropdownOption(driver,stateDropdown,state,stateOptionsLocation)
        # Select the City
        cityInput = driver.find_element(By.XPATH, "//div[@id='city']")
        city = dataFrame[cityInput.get_attribute('id')]
        city = str(city[0])
        cityInput.click()
        cityDropdown = "//div[@id='city']//div[contains(@class,'css-26l3qy')]"
        cityOptionsLocation = ".//div[contains(@id,'-option')]"
        selectDropdownOption(driver, cityDropdown, city, cityOptionsLocation)
        # Submit the Form
        driver.find_element(By.ID,"submit").click()
        logging.info("Form submitted successfully.")
        # Success message
        # successMessage = 'Thanks for submitting the form'
        # submitButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"example-modal-sizes-title-lg")))
        # if successMessage.lower() == submitButton.text.lower():
        #     logging.info(f"Success message: {submitButton.text}")
        # else:
        #     logging.error("Success message not found.")
        # # Close the success message
        # closeButton = driver.find_element(By.ID,"closeLargeModal")
        # driver.execute_script("arguments[0].click();", closeButton)
    except Exception as e:
        logging.error(f"Error in form submission: {e}")
# Main Method
def main():
    try:
        config = read_config()
        configure_logging(config)
        logging.info("Test execution started.")
        dataFrame = readExcelData('Sheet2',config)
        browser = dataFrame['browser']
        websiteUrl = config.get("URLS", "website")
        # initialize driver
        driver = initialize_driver(browser[0],config)
        logging.info("Driver initialized successfully.")
        # Open the website
        openWebsite(driver,websiteUrl)
        logging.info("Website opened and ready for interaction.")
        # Wait for the page to load
        driver.implicitly_wait(10)
        # Fill the Form
        logging.info("Form submission initiated.")
        fillForm(driver,config)
        logging.info("Form filled and submitted successfully.")
        quitBrowser(driver)
        logging.info("Browser closed. Test execution completed.")
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()