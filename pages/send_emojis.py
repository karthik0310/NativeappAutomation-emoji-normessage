import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from base.base_class import BaseClass
from utils.locators import Locators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class SendEmj(BaseClass):
    def __init__(self, driver1, driver2):
        """
        Initialize SendEmj with two drivers: one for sender and one for receiver.
        """
        super().__init__(driver1)
        self.driver1 = driver1
        self.driver2 = driver2

    def sending_emj(self):
        """
        Method to send an emoji message from the sender's device.
        """
        with allure.step("Click 'Start Chat' Button"):
            try:
                self.click_element(AppiumBy.ID, Locators.START_CHAT_BUTTON_ID)
                self.take_screenshot("Start_Chat_Button_Clicked")
            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Start_Chat_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to click 'Start Chat' button: {e}")

        with allure.step("Add Sender Contact Number"):
            try:
                self.clear_field(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH)
                self.send_keys(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH, "+18014194233")
                self.click_element(AppiumBy.XPATH, Locators.CLICK_NUMBER_XPATH)
                self.take_screenshot("Contact_Number_Added")
            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Add_Contact_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to add sender contact number: {e}")

        # List of emojis to choose from
        emojis = ["😀", "😂", "😍", "🥺", "😎", "🤔", "🤩", "😅", "🤗", "😜"]

        # Select a random emoji
        unique_emoji = random.choice(emojis)

        print(unique_emoji)

        with allure.step(f"Send emoji message: {unique_emoji}"):
            try:
                self.clear_field(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID)
                self.send_keys(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID, unique_emoji)
                self.take_screenshot("Emoji_Composed")
                self.click_element(AppiumBy.XPATH, Locators.SEND_BUTTON_XPATH)
            except Exception as e:
                allure.attach(self.driver1.get_screenshot_as_png(), name="Compose_Emoji_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to compose and send emoji: {e}")

        return unique_emoji  # Return the sent emoji message for verification

    #time.sleep(10)
    def verifying_msg(self, unique_emoji):
        """
        Method to verify the emoji message on the receiver's device.
        """
        time.sleep(10)

        try:
            if self.driver2:
                with allure.step("Verify Emoji on Receiver Device"):
                    self.driver2.find_element(AppiumBy.XPATH, Locators.RECEIVED_MSG_INDEX1_XPATH).click()
                    self.take_screenshot("Receiver_Message_Screen")

                    #dynamic xpath for unique emojis
                    # Wait until the emoji element appears
                    emoji_element = WebDriverWait(self.driver2, 10).until(
                        EC.presence_of_element_located((AppiumBy.XPATH,
                                                        f"//android.view.View[@resource-id='LottieAnimation' and contains(@content-desc, '{unique_emoji}')]"))
                    )

                    # Get the emoji from content-desc
                    received_msg = emoji_element.get_attribute("content-desc")

                    # Debugging - Print content-desc of all android.view.View elements
                    elements = self.driver2.find_elements(AppiumBy.XPATH, "//android.view.View")
                    for elem in elements:
                        print("Found element with content-desc:", elem.get_attribute("content-desc"))

                    # Take a final screenshot
                    self.take_screenshot("Emoji_Received")

                    assert unique_emoji in received_msg, f"Sent and received messages do not match. Expected: {unique_emoji}, Found: {received_msg}"
                    self.take_screenshot("Message_Received")

            else:
                with allure.step("Receiver device not connected. Verifying emoji on sender device"):
                    print("Receiver device not connected. Falling back to sender device.")

                    self.restart_drivers()

                    self.driver1.find_element(AppiumBy.XPATH, Locators.EMOJI_XPATH).click()
                    self.take_screenshot("Sender_Message_Screen")

                    received_msg = self.driver1.find_element(
                        AppiumBy.XPATH, f"//android.widget.TextView[contains(@content-desc, '{unique_emoji}')]"
                    ).get_attribute("content-desc")  # ✅ Fix: Ensure correct attribute usage

                    assert unique_emoji in received_msg, \
                        f"Sent and received emoji messages do not match on sender device. Expected: {unique_emoji}, Found: {received_msg}"

                    self.take_screenshot("Emoji_Validated_On_Sender_Device")

        except Exception as e:
            allure.attach(self.driver1.get_screenshot_as_png(), name="Verification_Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify the emoji message: {e}")

