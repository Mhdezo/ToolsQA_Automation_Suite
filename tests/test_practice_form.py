# test script
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ToolsQA_Automation_Suite.utils.common_methods import initialize_driver, quitBrowser,readExcelData, read_config
from ToolsQA_Automation_Suite.pages.practice_form import fillForm
from selenium.webdriver.common.by import By
from configparser import ConfigParser

# Load Configuration
config = read_config()
@pytest.fixture(scope="function")
def setup():
    driver = None
    try:
        browser = config.get("PATHS", "chromedriver")
        driver = initialize_driver("chrome",config)
        yield driver
    finally:
        if driver:
            quitBrowser(driver)
@pytest.fixture
def test_data():
    return readExcelData("Sheet1",config)

def test_form_submission(setup,test_data):
    driver = setup
    website_url = config.get("URLS", "website")

    driver.get(website_url)
    driver.implicitly_wait(10)
    fillForm(driver,config)
    try:
        success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"example-modal-sizes-title-lg"))).text
        assert success_message == "Thanks for submitting the form", "Form submission failed"
    except Exception as e:
        pytest.fail(f"Test failed due to: {e}")
