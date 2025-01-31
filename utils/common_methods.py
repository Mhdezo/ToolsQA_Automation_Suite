# reusable utility functions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException
import sys
import logging
import openpyxl
import configparser
import os

# Configure logging
def configure_logging(config):
    log_file_path = config.get("PATHS", "logfile")
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
# Initialize WebDriver
def initialize_driver(browser,config):
    try:
        if browser.lower() == "chrome":
            chromedriverPath = config.get("PATHS", "chromedriver")
            service = ChromeService(executable_path=chromedriverPath)
            driver = webdriver.Chrome(service=service)
        elif browser.lower() == "edge":
            edgedriverPath = config.get("PATHS", "edgedriver")
            service = EdgeService(executable_path=edgedriverPath)
            driver = webdriver.Edge(service=service)
        elif browser.lower() == "firefox":
            firefoxdriverPath = config.get("PATHS", "firefoxdriver")
            service = FirefoxService(executable_path=firefoxdriverPath)
            driver = webdriver.Firefox(service=service)
        else:
            raise ValueError("Unsupported browser")
        driver.maximize_window()
        return driver
    except Exception as e:
        logging.error(f"Error initializing driver: {e}")
        sys.exit(1)
# Scroll to the element
def scrollIntoView(driver,element):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
    except Exception as e:
        logging.warning(f"Could not scroll to element: {e}")
# Open the website and maximize the window
def openWebsite(driver,websiteUrl):
    driver.get(websiteUrl)
    driver.maximize_window()
# Helper to select dropdown options
def selectDropdownOption(driver, dropdownLocator, value,optionLocation):
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, dropdownLocator))
        )
        options = dropdown.find_elements(By.XPATH, optionLocation)
        for option in options:
            if option.text.lower() == value.lower():
                option.click()
                return
        logging.warning(f"Option {value} not found in dropdown.")
    except TimeoutException:
        logging.error("Dropdown not found or not clickable.")
# Read Excel data
def readExcelData(sheetName,config):
    excelFilePath = config.get("PATHS", "excelfile")
    workBook = openpyxl.load_workbook(excelFilePath)  # load the workBook
    sheet = workBook[sheetName]  # Point to the desired sheet
    columnsNumber = sheet.max_column  # Get number of columns in the sheet those filled with the data
    rowsNumber = sheet.max_row  # Get number of Rows in the sheet those filled with the data
    dataFrame = {}  # Dictionary to store the data of the sheet
    # Fetch the data
    for col in range(1, columnsNumber + 1):
        cellValue = []
        for row in range(2, rowsNumber + 1):
            cellValue.append(sheet.cell(row, col).value)
        dataFrame[sheet.cell(1, col).value] = cellValue
    return dataFrame
# Quit the browser
def quitBrowser(driver):
    driver.quit()
# Returns the absolute path to the project root directory.
def get_project_root():
    # Navigate up the directory tree until you find the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, "README.md")):  # Use a unique file to identify the root
        current_dir = os.path.dirname(current_dir)
    return current_dir # Returns: str: The path to the project root directory.
# Reads the configuration from config.ini.
def read_config():
    config = configparser.ConfigParser()
    project_root = get_project_root()
    config_path = os.path.join(project_root, "config", "config.ini")
    config.read(config_path)
    return config # Returns: configparser.ConfigParser: The configuration object.