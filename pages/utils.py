class Locators:
    START_CHAT_BUTTON_ID = "com.google.android.apps.messaging:id/start_chat_fab"
    TO_TEXT_AREA_XPATH = "//android.widget.EditText[@resource-id='ContactSearchField']"
    CLICK_NUMBER_XPATH = (
        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
        "android.widget.FrameLayout/android.widget.FrameLayout/"
        "android.widget.FrameLayout/android.view.ViewGroup/android.view."
        "ViewGroup[2]/android.view.ViewGroup/androidx.compose.ui.platform."
        "ComposeView/android.view.View/android.view.View/android.view.View/"
        "android.view.View/android.view.View/android.view.View[2]/android.view.View"
    )
    MESSAGE_TEXT_AREA_ID = "com.google.android.apps.messaging:id/compose_message_text"
    SEND_BUTTON_XPATH = (
        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
        "android.widget.FrameLayout/android.widget.FrameLayout/"
        "android.widget.FrameLayout/android.view.ViewGroup/android.view."
        "ViewGroup[2]/android.view.ViewGroup/androidx.compose.ui.platform."
        "ComposeView/android.view.View/android.view.View/android.view.View/"
        "android.view.View[1]/android.view.View[3]/android.view.View[2]/"
        "android.widget.Button"
    )
    RECEIVED_MSG_INDEX1_XPATH = "//android.support.v7.widget.RecyclerView[@content-desc='Conversation list']/android.view.ViewGroup[1]"

    #UNIQUE_MSG_VALIDATION = "//android.widget.TextView[contains(@content-desc, '{unique_msg}')]"