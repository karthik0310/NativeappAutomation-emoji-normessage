import allure
import pytest
from pages.send_msg import SendMsg
from logs.custom_logger import Logger
from utilities.api_client import ApiClient

@allure.feature("Messaging Feature with API Integration")
class TestSendMsg:

    @pytest.fixture(scope="class", autouse=True)
    def setup_api_client(self):
        """
        Setup API client before running the tests.
        """
        self.api_client = ApiClient(base_url="http://api.example.com")
        self.api_client.reset_environment()  # Optional: Reset the environment

    @allure.story("Send Message via UI and Verify via API")
    def test_send_msg_ui_verify_api(self, setup):
        """
        Test case to send a message using the UI and validate it via API.
        """
        driver1, driver2 = setup
        logger = Logger.get_logger()

        # Step 1: Send message using Appium
        sendmsg_obj = SendMsg(driver1, driver2)
        unique_msg = sendmsg_obj.sending_msg()
        allure.attach(driver1.get_screenshot_as_png(), name="Message_Sent", attachment_type=allure.attachment_type.PNG)
        logger.info("Message sent successfully using UI.")

        # Step 2: Validate message via API
        with allure.step("Validate message via API"):
            messages = self.api_client.fetch_messages(receiver="receiver@example.com")
            assert unique_msg in [msg["content"] for msg in messages], "Message not found in API response."
            allure.attach(str(messages), name="API_Response", attachment_type=allure.attachment_type.JSON)
            logger.info("Message validated successfully via API.")

    @allure.story("Send Message via API and Verify via UI")
    def test_send_msg_api_verify_ui(self, setup):
        """
        Test case to send a message using the API and validate it via the UI.
        """
        driver1, driver2 = setup
        logger = Logger.get_logger()

        # Step 1: Send message using API
        unique_msg = f"User_{int(time.time())}"
        response = self.api_client.send_message(sender="sender@example.com", receiver="receiver@example.com", message=unique_msg)
        allure.attach(str(response), name="API_Response", attachment_type=allure.attachment_type.JSON)
        logger.info("Message sent successfully using API.")

        # Step 2: Validate message via Appium
        sendmsg_obj = SendMsg(driver1, driver2)
        with allure.step("Validate message via UI"):
            sendmsg_obj.verifying_msg(unique_msg)
            allure.attach(driver2.get_screenshot_as_png(), name="Message_Validated", attachment_type=allure.attachment_type.PNG)
            logger.info("Message validated successfully via UI.")
