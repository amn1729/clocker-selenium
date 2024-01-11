from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import time
import os
import sys


class Color:
    ENDC = '\033[0m'
    GREEN = '\033[92m'
    GREY = '\33[90m'
    RED = '\033[91m'
    YELLOW = '\33[33m'


def colored(text: str, color: Color) -> str:
    """
    Returns colored text
    @param text as str
    @param color as Color
    @return str
    """
    return f'{color}{text}{Color.ENDC}'


class Clocker:
    """
    Clocker class with `config_path` as user-data-dir arg to the Chromedriver
    """

    def __init__(self, config_path: str):
        """
        @param config_path as str
        @return Clocker
        """
        options = webdriver.ChromeOptions()
        options.add_argument(r"--user-data-dir=" + config_path)
        options.add_experimental_option("excludeSwitches",
                                        ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options)
        
        self.CRM_URL = "https://crm.softsensor.ai/account/dashboard"
        self.CLOCK_IN_BTN_ID = "clock-in"
        self.SAVE_CLOCK_IN_BTN_ID = "save-clock-in"
        self.CLOCK_OUT_BTN_ID = "clock-out"
        self.LOCATION_BTN_SELECTOR = "button[data-id=location]"
        self.LOCATION_OPTION_ID = "bs-select-1-2"
        self.FROM_BTN_SELECTOR = "button[data-id=work_from_type]"
        self.FROM_OPTION_ID = "bs-select-2-1"

        print(colored(f"Created Clocker('{config_path}')", Color.GREEN))

    def clock_in(self):
        """
        Find and click the clock-in button, and load the save-clock-in Modal
        Submit the save-clock-in form by click save-clock-in button
        """
        print(colored("Finding Clock in button...", Color.YELLOW))
        elem = self.driver.find_element(By.ID, self.CLOCK_IN_BTN_ID)
        elem.click()
        # wait for the modal to load
        time.sleep(3)
        try:
            location_btn = self.driver.find_element(By.CSS_SELECTOR, self.LOCATION_BTN_SELECTOR)
            location_btn.click()
            print(colored("Clicked location button", Color.GREEN))
            time.sleep(0.6)
            location_option = self.driver.find_element(By.ID, self.LOCATION_OPTION_ID)
            location_option.click()
            print(colored("Clicked location option", Color.GREEN))

            from_btn = self.driver.find_element(By.CSS_SELECTOR, self.FROM_BTN_SELECTOR)
            from_btn.click()
            print(colored("Clicked from button", Color.GREEN))
            time.sleep(0.6)
            from_option = self.driver.find_element(By.ID, self.FROM_OPTION_ID)
            from_option.click()
            print(colored("Clicked from option", Color.GREEN))

            time.sleep(0.6)
            print(colored("Finding Save clock in button...", Color.YELLOW))
            elem = self.driver.find_element(By.ID, self.SAVE_CLOCK_IN_BTN_ID)
            elem.click()
            print(colored("Clicked save clock in button", Color.GREEN))
            os.system("echo 'IN' > ~/.config/clocker/state")
        except:
            print(colored("Could not found location button", Color.RED))

    def clock_out(self):
        """
        Find and click the clock-out button.
        """
        print(colored("Finding and clicking Clock out button...", Color.YELLOW))
        elem = self.driver.find_element(By.ID, self.CLOCK_OUT_BTN_ID)
        elem.click()
        print(colored("Clicked clock out button", Color.GREEN))
        os.system("echo 'OUT' > ~/.config/clocker/state")

    def load_dashboard(self) -> (bool, bool):
        """
        Load dashboard and returns (has_clock_in_btn, has_clock_out_btn).
        @return (bool, bool)
        """
        has_clock_in_btn, has_clock_out_btn = False, False
        print(colored("Loading Dashboard...", Color.YELLOW))
        self.driver.maximize_window()
        self.driver.get(self.CRM_URL)
        # wait 3 secs to load the dashboard
        time.sleep(3)

        try:
            print(colored("Finding Clock in button...", Color.YELLOW))
            elem = self.driver.find_element(By.ID, self.CLOCK_IN_BTN_ID)
            has_clock_in_btn = True
        except:
            print(colored("Could not found Clock in button", Color.RED))

        try:
            print(colored("Finding Clock out button...", Color.YELLOW))
            elem = self.driver.find_element(By.ID, self.CLOCK_OUT_BTN_ID)
            has_clock_out_btn = True
        except:
            print(colored("Could not found Clock out button", Color.RED))

        return (has_clock_in_btn, has_clock_out_btn)


def main():
    CONFIG_PATH = os.environ['HOME'] + '/.config/chromium'
    clocker = Clocker(CONFIG_PATH)
    has_clock_in_btn, has_clock_out_btn = clocker.load_dashboard()

    if has_clock_out_btn:
        clocker.clock_out()
        sys.exit()

    if has_clock_in_btn:
        clocker.clock_in()
        sys.exit()

if __name__ == "__main__":
    main()
