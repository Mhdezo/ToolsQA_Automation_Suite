# pytest fixture
import pytest
from utils.common_methods import initialize_driver, read_config

@pytest.fixture(scope="module")
def browser(config):
    """Fixture to initialize and close the browser."""
    config = read_config()
    driver = initialize_driver(config.get("TEST", "browser"), config)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def config():
    """Fixture to read the configuration file."""
    return read_config()