import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from base.base_class import BaseClass
from .utils import Locators


class SendMsg(BaseClass):
    def __init__(self, driver1, driver2):
        """
        Initialize SendMsg with two drivers: one for sender and one for receiver.
        """
        super().__init__(driver1)
        self.driver2 = driver2

    def sending_msg(self):
        """
        Method to send a message from the sender's device.
        """
        # Step 1: Click "Start Chat" Button
        with allure.step("Click 'Start Chat' Button"):
            try:
                self.click_element(AppiumBy.ID, Locators.START_CHAT_BUTTON_ID)
                self.take_screenshot("Start_Chat_Button_Clicked")
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Start_Chat_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to click 'Start Chat' button: {e}")

        # Step 2: Add Sender Contact Number
        with allure.step("Add Sender Contact Number"):
            try:
                self.clear_field(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH)
                self.send_keys(AppiumBy.XPATH, Locators.TO_TEXT_AREA_XPATH,"+18014194233")
                self.click_element(AppiumBy.XPATH, Locators.CLICK_NUMBER_XPATH)

                self.take_screenshot("Contact_Number_Added")
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Add_Contact_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to add sender contact number: {e}")

        # Step 3: Compose and Send Message
        unique_msg = f"User_{int(time.time())}"
        with allure.step(f"Send unique message: {unique_msg}"):
            try:
                self.clear_field(AppiumBy.ID, "com.google.android.apps.messaging:id/compose_message_text")
                self.take_screenshot("Message_Composed" )
                self.send_keys(AppiumBy.ID, Locators.MESSAGE_TEXT_AREA_ID, unique_msg)
                self.take_screenshot("Message_Composed")
                # Updated XPath for send button. Adjust based on your UI element.
                self.click_element(AppiumBy.XPATH, Locators.SEND_BUTTON_XPATH )
            except Exception as e:
                allure.attach(self.driver.get_screenshot_as_png(), name="Compose_Message_Error",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to compose and send message: {e}")

        return unique_msg  # Return the unique message for verification
    time.sleep(5)

    def verifying_msg(self, unique_msg):
        """
        Method to verify the message on the receiver's device or fallback to the sender's device if only one is connected.
        """
        try:
            if self.driver2:
                # Step 4a: Verify Message on Receiver's Device
                with allure.step("Verify Message on Receiver Device"):
                    self.driver2.find_element(AppiumBy.XPATH,
                                              Locators.RECEIVED_MSG_INDEX1_XPATH).click()
                    self.take_screenshot("Receiver_Message_Screen")

                    # Dynamic XPath for the unique message
                    received_msg = self.driver2.find_element(
                        AppiumBy.XPATH, f"//android.widget.TextView[contains(@content-desc, '{unique_msg}')]"
                    ).text
                    assert unique_msg in received_msg, f"Sent and received messages do not match. Expected: {unique_msg}, Found: {received_msg}"
                    self.take_screenshot("Message_Received")
            else:
                # Step 4b: Fallback to Sender's Device for Validation
                with allure.step("Receiver device not connected. Verifying message on sender device"):
                    print("Receiver device not connected. Falling back to sender device.")

                    self.restart_driver1()
                    # Dynamic XPath for the unique message on the sender device
                    self.driver1.find_element(
                        AppiumBy.XPATH,
                        "//android.support.v7.widget.RecyclerView[@content-desc='Conversation list']/android.view.ViewGroup[1]"
                    ).click()
                    self.take_screenshot("Sender_Message_Screen")

                    received_msg = self.driver1.find_element(
                        AppiumBy.XPATH, f"//android.widget.TextView[contains(@content-desc, '{unique_msg}')]"
                    ).get_attribute("content-desc")
                    assert unique_msg in received_msg, f"Sent and received messages do not match on sender device. Expected: {unique_msg}, Found: {received_msg}"
                    self.take_screenshot("Message_Validated_On_Sender_Device")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Verification_Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify the message: {e}")
