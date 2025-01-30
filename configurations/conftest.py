import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from configurations.config import des_cap_device1, url, des_cap_device2


def get_connected_devices():
    """
    Fetches a list of connected devices using ADB.
    """
    try:
        import subprocess
        result = subprocess.check_output(["adb", "devices"], stderr=subprocess.STDOUT, text=True)
        lines = result.strip().split("\n")
        devices = [line.split("\t")[0] for line in lines[1:] if "device" in line]
        return devices
    except Exception as e:
        print(f"Error fetching connected devices: {e}")
        return []


@pytest.fixture(scope="class")
def setup():
    # Get the list of connected devices
    connected_devices = get_connected_devices()

    if len(connected_devices) >= 1:
        # Both devices are connected or duplicate same device
        device1_id = connected_devices[0]
        device2_id = connected_devices[1] if len(connected_devices) > 1 else connected_devices[0]
    else:
        raise Exception("No devices connected")

    # Create AppiumOptions for both devices
    options_device1 = AppiumOptions()
    options_device1.load_capabilities(des_cap_device1)
    options_device1.capabilities["udid"] = device1_id

    options_device2 = AppiumOptions()
    options_device2.load_capabilities(des_cap_device2)
    options_device2.capabilities["udid"] = device2_id

    # Initialize drivers
    driver1 = webdriver.Remote(command_executor=url, options=options_device1)
    driver2 = None

    try:
        driver2 = webdriver.Remote(command_executor=url, options=options_device2)
    except Exception as e:
        print(f"Warning: Second driver initialization failed: {e}")

    yield driver1, driver2

    if driver1:
        driver1.quit()
    if driver2:
        driver2.quit()

    # Use options instead of desired_capabilities
    # driver1 = webdriver.Remote(command_executor=url, options=options_device1)
    # driver2 = webdriver.Remote(command_executor=url, options=options_device2)
    #
    # yield driver1, driver2
    # # Quit drivers after the test
    # driver1.quit()
    # driver2.quit()