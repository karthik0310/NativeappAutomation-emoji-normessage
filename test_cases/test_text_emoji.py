import random
import allure
from pages.message_workflow import MessageWorkflow  # ✅ Updated import
from logs.custom_logger import Logger
from configurations.conftest import setup
import time

@allure.feature("Messaging Feature")
@allure.story("Send and Verify Message")
class TestSendMsg:

    @allure.step("Sending and verifying a message between devices")
    def test_send_msg(self, setup):
        logger = Logger.get_logger()
        logger.info("Text message test case started")

        driver1, driver2 = setup
        msg_workflow = MessageWorkflow(driver1, driver2)
        logger.info("Drivers initialized for message workflow")

        with allure.step("Sending a message from sender device"):
            unique_msg = f"Welcome_{int(time.time())}"  # Unique message
            msg_workflow.send_message(unique_msg)
            allure.attach(driver1.get_screenshot_as_png(), name="Sender_Message_Sent",
                          attachment_type=allure.attachment_type.PNG)
            logger.info(f"Message '{unique_msg}' sent successfully from sender device")

        with allure.step("Validating the message on receiver device"):
            msg_workflow.verify_message(unique_msg, message_type="text")
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Message_Validated",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Text message validated successfully on receiver device")

        logger.info("Text message test case ended successfully")

    @allure.step("Sending and verifying an emoji message between devices")
    def test_send_emoji(self, setup):
        logger = Logger.get_logger()
        logger.info("Emoji test case started")

        driver1, driver2 = setup
        msg_workflow = MessageWorkflow(driver1, driver2)
        logger.info("Drivers initialized for emoji workflow")

        with allure.step("Sending an emoji from sender device"):
            unique_emoji = random.choice(["😀", "😂", "😍", "🥺", "😎", "🤔", "🤩", "😅", "🤗", "😜"])
            msg_workflow.send_message(unique_emoji)
            allure.attach(driver1.get_screenshot_as_png(), name="Sender_Emoji_Sent",
                          attachment_type=allure.attachment_type.PNG)
            logger.info(f"Emoji '{unique_emoji}' sent successfully from sender device")

        with allure.step("Validating the emoji message on receiver device"):
            msg_workflow.verify_message(unique_emoji, message_type="emoji")
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Emoji_Validated",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Emoji message validated successfully on receiver device")

        logger.info("Emoji test case ended successfully")

    @allure.step("Sending and verifying an Image between devices")
    def test_send_image(self, setup):
        logger = Logger.get_logger()
        logger.info("Image message test case started")

        driver1, driver2 = setup
        msg_workflow = MessageWorkflow(driver1, driver2)
        logger.info("Drivers initialized for Image message workflow")

        with allure.step("Starting a new chat for validating image form message"):
            logger.info("Chat Opened for Image sending")
            msg_workflow.send_message(message_type="image")  # ✅ Opens chat correctly
            allure.attach(driver1.get_screenshot_as_png(), name="Chat_Opened",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Image sent successfully from sender device")


        with allure.step("Validating the image on receiver device"):
            msg_workflow.verify_message(message_type="image")  # ✅ Verify image reception
            allure.attach(driver2.get_screenshot_as_png(), name="Receiver_Image_Validated",
                          attachment_type=allure.attachment_type.PNG)
            logger.info("Image message validated successfully on receiver device")

        logger.info("Image message test case ended successfully")
