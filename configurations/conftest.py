import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from configurations.config import des_cap_device1, url, des_cap_device2

@pytest.fixture(scope="class")
def setup():
    # Create AppiumOptions for both devices
    options_device1 = AppiumOptions()
    options_device1.load_capabilities(des_cap_device1)

    options_device2 = AppiumOptions()
    options_device2.load_capabilities(des_cap_device2)

    # Initialize driver1
    driver1 = webdriver.Remote(command_executor=url, options=options_device1)

    try:
        # Try to initialize driver2
        driver2 = webdriver.Remote(command_executor=url, options=options_device2)
    except Exception as e:
        # If driver2 cannot be initialized, set it to None and log a warning
        driver2 = None
        print(f"Warning: Only one device is connected. Second driver initialization failed: {e}")

    # Yield the drivers
    yield driver1, driver2

    # Quit drivers after tests
    if driver1:
        driver1.quit()
    if driver2:
        driver2.quit()

    # Use options instead of desired_capabilities
    # driver1 = webdriver.Remote(command_executor=url, options=options_device1)
    # driver2 = webdriver.Remote(command_executor=url, options=options_device2)
    #
    # yield driver1, driver2
    # # Quit drivers after the test
    # driver1.quit()
    # driver2.quit()