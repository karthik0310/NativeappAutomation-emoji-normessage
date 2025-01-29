import allure
from pages.send_msg import SendMsg
from logs.custom_logger import Logger
from configurations.conftest import setup


@allure.feature("Messaging Feature")
@allure.story("Send and Verify Message")
class TestSendMsg:

    @allure.step("Sending and verifying a message between devices")
    def test_send_msg(self, setup):
        logger = Logger.get_logger()
        logger.info("Test case started")

        # Unpacking drivers
        driver1, driver2 = setup

        # Initializing the SendMsg object
        sendmsg_obj = SendMsg(driver1, driver2)

        # Step 1: Sending the message
        with allure.step("Sending a message from sender device"):
            unique_msg = sendmsg_obj.sending_msg()
            allure.attach(driver1.get_screenshot_as_png(), name="Sender_Message_Sent", attachment_type=allure.attachment_type.PNG)
            logger.info("Message sent successfully from sender device")

        # Step 2: Validating the message
        with allure.step("Validating the message on receiver device"):
            sendmsg_obj.verifying_msg(unique_msg)
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Message_Validated", attachment_type=allure.attachment_type.PNG)
            logger.info("Message validated successfully on receiver device")

        # Test case completion
        logger.info("Test case ended successfully")
