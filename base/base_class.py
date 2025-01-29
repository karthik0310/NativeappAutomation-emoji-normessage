import os
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BaseClass:
    """Base class for common Selenium and Appium utilities."""

    def __init__(self, driver):
        """Initialize BaseClass with a driver instance."""
        if not driver:
            raise ValueError("Driver instance is required.")
        self.driver = driver

    def take_screenshot(self, filename: str) -> None:
        """Takes a screenshot and saves it with a timestamp."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "./screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the directory exists
        screenshot_path = os.path.join(screenshot_dir, f"{filename}_{timestamp}.png")
        try:
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")

    def get_element(self, locator_type: str, locator_value: str) -> WebElement:
        """Waits for an element to be present and returns it."""
        try:
            wait = WebDriverWait(self.driver, 30)
            locator = {
                "id": AppiumBy.ID,
                "xpath": AppiumBy.XPATH,
                "css selector": AppiumBy.CSS_SELECTOR,
                "link text": AppiumBy.LINK_TEXT,
            }.get(locator_type.lower())

            if not locator:
                raise ValueError(f"Unsupported locator type: {locator_type}")

            element = wait.until(EC.presence_of_element_located((locator, locator_value)))
            logger.info(f"Element located: {locator_value}")
            return element
        except Exception as e:
            logger.error(f"Error locating element by {locator_type}={locator_value} | Exception: {e}")
            self.take_screenshot("get_element_error")
            raise

    def click_element(self, locator_type: str, locator_value: str) -> None:
        """Clicks on the element located by the given locator."""
        try:
            element = self.get_element(locator_type, locator_value)
            element.click()
            logger.info(f"Clicked element: {locator_value}")
        except Exception as e:
            logger.error(f"Error clicking element: {locator_value} | Exception: {e}")
            self.take_screenshot("click_element_error")
            raise

    def send_keys(self, locator_type: str, locator_value: str, text: str) -> None:
        """Sends text to the input field located by the given locator."""
        try:
            element = self.get_element(locator_type, locator_value)
            element.clear()
            element.send_keys(text)
            logger.info(f"Sent text '{text}' to element: {locator_value}")
        except Exception as e:
            logger.error(f"Error sending text to element: {locator_value} | Exception: {e}")
            self.take_screenshot("send_keys_error")
            raise

    def get_text(self, locator_type: str, locator_value: str) -> str:
        """Retrieves text from the element located by the given locator."""
        try:
            element = self.get_element(locator_type, locator_value)
            text = element.text
            logger.info(f"Retrieved text: {text}")
            return text
        except Exception as e:
            logger.error(f"Error retrieving text from element: {locator_value} | Exception: {e}")
            self.take_screenshot("get_text_error")
            raise

    def is_displayed(self, locator_type: str, locator_value: str) -> bool:
        """Checks if the element is displayed."""
        try:
            element = self.get_element(locator_type, locator_value)
            displayed = element.is_displayed()
            logger.info(f"Element displayed status: {displayed}")
            return displayed
        except Exception as e:
            logger.error(f"Error checking display status for element: {locator_value} | Exception: {e}")
            self.take_screenshot("is_displayed_error")
            return False

    def clear_field(self, locator_type: str, locator_value: str) -> None:
        """Clears the text in an input field."""
        try:
            element = self.get_element(locator_type, locator_value)
            element.clear()
            logger.info(f"Cleared text from element: {locator_value}")
        except Exception as e:
            logger.error(f"Error clearing text from element: {locator_value} | Exception: {e}")
            self.take_screenshot("clear_field_error")
            raise

    def get_attribute(self, locator_type: str, locator_value: str, attribute: str) -> str:
        """Gets the value of a specified attribute of an element."""
        try:
            element = self.get_element(locator_type, locator_value)
            attr_value = element.get_attribute(attribute)
            logger.info(f"Attribute '{attribute}' value: {attr_value}")
            return attr_value
        except Exception as e:
            logger.error(f"Error retrieving attribute '{attribute}' for element: {locator_value} | Exception: {e}")
            self.take_screenshot("get_attribute_error")
            raise

    def retry_operation(self, func, retries: int = 3, delay: int = 2):
        """Retries a function in case of failure."""
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                logger.warning(f"Retry {attempt + 1}/{retries} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
        raise Exception("All retries failed.")


