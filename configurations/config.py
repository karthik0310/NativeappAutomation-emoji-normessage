
des_cap_device1 = {
    "platformName": "Android",
    "udid": "86NX00BUS",
    "deviceName": "Google_Pixel",
    "appPackage": "com.google.android.apps.messaging",
    "appActivity": "com.google.android.apps.messaging.ui.ConversationListActivity",
    "automationName": "UiAutomator2",
    "noReset": True,
    "fullReset": False,
    "newCommandTimeout": 3000,  # Increased timeout
    "deviceReadyTimeout": 3000,  # Added device ready timeout
    "appWaitDuration": 3000,  # Added wait time for the app
}

des_cap_device2 = {
             "platformName": "Android",
             "udid": "93CAY0971L",
             "deviceName": "Google_pixel",
             "appPackage": "com.google.android.apps.messaging",
             "appActivity": "com.google.android.apps.messaging.main.MainActivity",
             "automationName": "UiAutomator2",
             "noReset": True,
             "fullReset": False,
             "newCommandTimeout": 3000,  # Increased timeout
             "deviceReadyTimeout": 3000,  # Added device ready timeout
             "appWaitDuration": 3000,  # Added wait time for the app
}

url = "http://localhost:4723/wd/hub"