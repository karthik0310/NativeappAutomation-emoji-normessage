import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from configurations.config import des_cap_device1, url, des_cap_device2
import subprocess


def get_connected_devices():
    """
    Fetches a list of connected devices using ADB.
    """
    try:
        result = subprocess.check_output(["adb", "devices"], stderr=subprocess.STDOUT, text=True)
        lines = result.strip().split("\n")
        devices = [line.split("\t")[0] for line in lines[1:] if "device" in line]
        return devices
    except Exception as e:
        print(f"Error fetching connected devices: {e}")
        return []


def initialize_drivers():
    """
    Initializes two drivers for the connected devices.
    """
    connected_devices = get_connected_devices()

    if len(connected_devices) == 0:
        raise Exception("No devices connected")

    # Assign first and second device IDs
    device1_id = connected_devices[0]
    device2_id = connected_devices[1] if len(connected_devices) > 1 else connected_devices[0]

    # Set Appium options for both devices
    options_device1 = AppiumOptions()
    options_device1.load_capabilities(des_cap_device1)
    options_device1.capabilities["udid"] = device1_id

    options_device2 = AppiumOptions()
    options_device2.load_capabilities(des_cap_device2)
    options_device2.capabilities["udid"] = device2_id

    # Start both drivers
    driver1 = webdriver.Remote(command_executor=url, options=options_device1)
    driver2 = None

    try:
        driver2 = webdriver.Remote(command_executor=url, options=options_device2)
    except Exception as e:
        print(f"Warning: Second driver initialization failed: {e}")

    return driver1, driver2


@pytest.fixture(scope="function")
def setup():
    """
    Pytest fixture to set up and tear down Appium drivers before and after each test.
    """
    driver1, driver2 = initialize_drivers()

    yield driver1, driver2  # Yield both drivers to the test case

    # Teardown: Quit drivers
    if driver1:
        driver1.quit()
    if driver2:
        driver2.quit()


def restart_drivers(driver1, driver2):
    """
    Properly restarts both drivers.
    """
    if driver1:
        driver1.quit()
    if driver2:
        driver2.quit()

    return initialize_drivers()  # Reinitialize both drivers
