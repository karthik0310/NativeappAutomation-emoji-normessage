import time
import random
import allure
from appium.webdriver.common.appiumby import AppiumBy
from logger import logger

from base.base_class import BaseClass
from utils.locators import Locators
from utils.data import  contact_number
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configurations.conftest import initialize_drivers
from configurations.conftest import restart_drivers
from logs.custom_logger import Logger

class MessageWorkflow(BaseClass):
    def __init__(self, driver1, driver2):
        """
        Initialize MessageWorkflow with two drivers:
        one for the sender and one for the receiver.
        """
        super().__init__(driver1)
        self.driver1 = driver1
        self.driver2 = driver2

    def send_message(self, message=None, message_type="text"):
        """
        Sends a message (text, emoji, or image).
        Steps:
        1️⃣ Start a chat
        2️⃣ Add the contact number
        3️⃣ Enter text/emoji OR select an image
        4️⃣ Click send button
        """
        with allure.step("Click 'Start Chat' Button"):
            try:
                self.click_element(AppiumBy.ID, Locators.START_CHAT_BUTTON_ID)
                self.take_screenshot("Start_Chat_Button_Clicked")
            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Start_Chat_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to click 'Start Chat' button: {e}")

        with allure.step("Add Contact Number"):
            try:
                self.clear_field(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH)
                receiver_contact_number = contact_number["Receiver_contact_number"]
                self.send_keys(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH, receiver_contact_number)
                self.click_element(AppiumBy.XPATH, Locators.CLICK_NUMBER_XPATH)
                self.take_screenshot("Contact_Number_Added")
            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Add_Contact_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to add contact number: {e}")

        with allure.step(f"Send {message_type} message"):
            try:
                if "image" in message_type:  # Allow sending both text and image
                    logger.info("Opening gallery to send an image...")
                    self.click_element(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID)  # Open media options
                    self.open_gallery()  # Open gallery
                    self.select_image()  # Select an image
                    self.take_screenshot("Image_Selected")

                if "text" in message_type or "emoji" in message_type:
                    logger.info("Typing message in input field...")
                    if message is None:
                        message = "Hello 👋"  # Default text if none is provided
                    self.clear_field(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID)
                    self.send_keys(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID, message)
                    self.take_screenshot("Message_Composed")

                # ✅ Click send button after selecting an image or entering text
                logger.info("Sending the message...")
                self.click_element(AppiumBy.XPATH, Locators.SEND_BUTTON_XPATH)
                self.take_screenshot("Message_Sent successfully ")

            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Message_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to send message ({message_type}): {e}")

        return message

    def verify_message(self, expected_message =None, message_type="text"):
        """
        Verifies that the sent message appears on the receiver's device.
        message_type should be "text" or "emoji" to use the correct XPath.
        """
        time.sleep(5)  # Wait for the message to sync
        try:
            if self.driver2:
                with allure.step("Verify Message on Receiver Device"):
                    # Click the conversation/message container
                    self.driver2.find_element(AppiumBy.XPATH, Locators.RECEIVED_MSG_INDEX1_XPATH).click()
                    self.take_screenshot("Receiver_Message_Screen")

                    # Choose the proper XPath based on message type
                    if message_type == "text":
                        xpath = f"//android.widget.TextView[contains(@content-desc, '{expected_message}')]"
                    elif message_type == "emoji":
                        xpath = f"//android.view.View[@resource-id='LottieAnimation' and contains(@content-desc, '{expected_message}')]"
                    elif message_type == "image":
                        xpath = "//android.widget.FrameLayout[contains(@content-desc, 'image')]"
                    else:
                        raise ValueError("Invalid message_type provided. Use 'text', 'emoji', or 'image'.")

                    # Wait for the element to appear
                    element = WebDriverWait(self.driver2, 10).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, xpath))
                    )

                    # For images, we just check if the element is found
                    if message_type == "image":
                    #     assert element is not None, "❌ Image not received"
                    #     self.take_screenshot("✅ Image_Received")
                    #     print("✅ Image successfully received.")
                    # else:
                        logger.info("Receiver  validation started ")
                        self.driver2.find_element(AppiumBy.XPATH, Locators.RECEIVED_MSG_INDEX1_XPATH).click()
                        logger.info("chat message is clicked on the receiver side")
                        received_msg = element.get_attribute("content-desc")
                        self.take_screenshot("Message_Received")
                        print(f"Expected: {expected_message} | Received: {received_msg}")
                        assert expected_message in received_msg, (
                            f"❌ Sent and received messages do not match. Expected: {expected_message}, Found: {received_msg}"
                        )
            else:
                with allure.step("Receiver device not connected. Verifying message on sender device"):
                    print("Receiver device not connected. Falling back to sender device.")
                    self.restart_driver()

                    if message_type == "text":
                        xpath = f"//android.widget.TextView[contains(@content-desc, '{expected_message}')]"
                    elif message_type == "emoji":
                        xpath = f"//android.view.View[@resource-id='LottieAnimation' and contains(@content-desc, '{expected_message}')]"
                    elif message_type == "image":
                        xpath = f"//android.widget.FrameLayout[@content-desc='Unselect this image attached at position 1 with double tap']/android.widget.TextView"
                    else:
                        raise ValueError("Invalid message_type provided. Use 'text' or 'emoji'.")

                    element = self.driver1.find_element(AppiumBy.XPATH, xpath)
                    received_msg = element.get_attribute("content-desc")
                    self.take_screenshot("Message_Validated_On_Sender_Device")
                    print(f"Expected: {expected_message} | Received: {received_msg}")
                    assert expected_message in received_msg, (
                        f"Sent and received messages do not match on sender device. Expected: {expected_message}, Found: {received_msg}"
                    )
        except Exception as e:
            allure.attach(self.driver1.get_screenshot_as_png(), name="Verification_Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify the message: {e}")

    def open_gallery(self):
        """
        Opens the gallery or image folder for selecting an image.
        """
        self.click_element(AppiumBy.XPATH, Locators.ATTACH_BUTTON_ID)  # Click attach
        self.click_element(AppiumBy.XPATH, Locators.GALLERY_OPTION_XPATH)  # Open gallery



    def select_image(self):
        """
        Selects the first image from the gallery.
        """
        self.click_element(AppiumBy.ID, Locators.FIRST_IMAGE_XPATH)  # Selects the first image
        #com.google.android.apps.messaging: id / local_media_item

    # def send_image(self):
    #     """
    #     Clicks the send button to send the selected image.
    #     """
    #     self.click_element(AppiumBy.XPATH, Locators.SEND_BUTTON_XPATH)  # Click send

    def verify_image(self, message_type="text"):
        if message_type == "image":
            with allure.step("Verifying received image on the second device"):
                # Click on the received message container
                self.driver2.find_element(AppiumBy.XPATH, Locators.RECEIVED_MSG_INDEX1_XPATH).click()
                logger.info("Chat message clicked on the receiver side")
                self.take_screenshot("Receiver_Message_Screen")

                # Locate the received image element
                try:
                    received_image = self.driver2.find_element(AppiumBy.XPATH, Locators.IMAGE_VALIDATION)
                    assert received_image is not None, "Image not received"
                    self.take_screenshot("Receiver_Image_Screen")
                except Exception as e:
                    logger.error(f"Error verifying image: {e}")
                    raise


if __name__ == "__main__":
    # ✅ Initialize drivers
    driver1, driver2 = initialize_drivers()

    # ✅ Ensure drivers are not None
    if driver1 is None or driver2 is None:
        raise Exception("Failed to initialize drivers.")

    # ✅ Create workflow instance
    workflow = MessageWorkflow(driver1, driver2)

    # ✅ Send text message
    text_message = f"Welcome_{int(time.time())}"
    sent_text = workflow.send_message(text_message)

    # ✅ Verify the sent message
    workflow.verify_message(sent_text, message_type="text")



    # For sending an emoji message:
    emojis = ["😀", "😂", "😍", "🥺", "😎", "🤔", "🤩", "😅", "🤗", "😜"]
    unique_emoji = random.choice(emojis)
    sent_emoji = workflow.send_message(unique_emoji)
    workflow.verify_message(sent_emoji, message_type="emoji")

    # ✅ Send an image
    # workflow.open_gallery()  # Open gallery
    # workflow.select_image()  # Select the first image
    #workflow.click_element(AppiumBy.XPATH, Locators.SEND_BUTTON_XPATH)  # Click send button

    # ✅ Send and Verify the sent image
    workflow.send_message(message_type="image")
    workflow.verify_image(message_type="image")

    # ✅ Quit drivers at the end
    driver1.quit()
    driver2.quit()