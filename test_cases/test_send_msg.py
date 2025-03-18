import random
import allure
from pages.send_msg import SendMsg
from pages.send_emojis import SendEmj  # ✅ Import SendEmj
from logs.custom_logger import Logger
from configurations.conftest import setup

@allure.feature("Messaging Feature")
@allure.story("Send and Verify Message")
class TestSendMsg:

    @allure.step("Sending and verifying a message between devices")
    def test_send_msg(self, setup):
        logger = Logger.get_logger()
        logger.info("Test case started")

        driver1, driver2 = setup
        sendmsg_obj = SendMsg(driver1, driver2)
        logger.info("drivers are unpacked successfully")

        with allure.step("Sending a message from sender device"):
            logger.info("Sending a unique message form sender side")
            unique_msg = sendmsg_obj.sending_msg()
            allure.attach(driver1.get_screenshot_as_png(), name="Sender_Message_Sent",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Message sent successfully from sender device")

        with allure.step("Validating the message on receiver device"):
            logger.info("Received the unique message form the sender")
            sendmsg_obj.verifying_msg(unique_msg)
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Message_Validated",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Unique Message validated successfully on receiver device")

        logger.info("Test case ended successfully")

    @allure.step("Sending and verifying an emoji message between devices")
    def test_send_emoji(self, setup):
        logger = Logger.get_logger()
        logger.info("Emoji test case started")

        driver1, driver2 = setup
        sendemj_obj = SendEmj(driver1, driver2)
        logger.info("Drivers are unpacking for the second time for sending emoji workflow")

        with allure.step("Sending an emoji from sender device"):
            unique_emoji = sendemj_obj.sending_emj()  # ✅ Fix: No redundant emoji selection
            allure.attach(driver1.get_screenshot_as_png(), name="Sender_Emoji_Sent",
                          attachment_type=allure.attachment_type.PNG)
            logger.info(f"Emoji '{unique_emoji}' sent successfully from sender device")


        with allure.step("Validating the emoji message on receiver device"):
            logger.info("Unique emoji are received form the sender ")
            sendemj_obj.verifying_msg(unique_emoji)  # ✅ Fix: Ensure correct emoji validation
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Emoji_Validated",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Emoji message validated successfully on receiver device")

        logger.info("Emoji test case ended successfully")

