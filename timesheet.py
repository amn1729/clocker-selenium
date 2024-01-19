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

        self.TIMESHEET_URL = "https://crm.softsensor.ai/account/timelogs/create"
        self.TASK_BTN_SELECTOR = "button[data-id=task_id2]"
        # self.TASK_BTN_ID = "task_id2"
        self.TASK_OPTION_ID = "bs-select-2-3"
        self.START_DATE_ID = "start_date"
        self.END_DATE_ID = "end_date"
        self.START_TIME_ID = "start_time"
        self.END_TIME_ID = "end_time"
        self.MEMO_ID = "memo"
        self.SAVE_BTN_ID = "save-timelog-form"

        print(colored(f"Created Clocker('{config_path}')", Color.GREEN))

    def load_timesheet(self) -> (bool, bool):
        """
        Load dashboard and returns (has_clock_in_btn, has_clock_out_btn).
        @return (bool, bool)
        """
        # today = datetime.date.today()
        # date = today.strftime('%d-%m-%Y')
        start_time = '10:30 AM'
        end_time = '07:30 PM'
        time.sleep(3)
        print(colored("Loading Timesheet...", Color.YELLOW))
        self.driver.maximize_window()
        self.driver.get(self.TIMESHEET_URL)
        # wait 3 secs to load the Timesheet_Url
        time.sleep(3)
        # try:
        task_btn = self.driver.find_element(
            By.CSS_SELECTOR, self.TASK_BTN_SELECTOR)
        task_btn.click()
        print(colored("Clicked task button", Color.GREEN))
        time.sleep(0.6)
        task_option = self.driver.find_element(By.ID, self.TASK_OPTION_ID)
        task_option.click()
        print(colored("Clicked task option", Color.GREEN))
        time.sleep(3)

        # date = "18-01-2024"
        # print(colored(f"Setting dates to {date}...", Color.YELLOW))
        # start_date_input = self.driver.find_element(By.ID, self.START_DATE_ID)
        # start_date_input.send_keys(Keys.CONTROL, 'a')
        # start_date_input.send_keys(date)
        # end_date_input = self.driver.find_element(By.ID, self.END_DATE_ID)
        # end_date_input.send_keys(Keys.CONTROL, 'a')
        # end_date_input.send_keys(date)

        # 2 elements of each
        hour_els = self.driver.find_elements(By.NAME, "hour")
        minutes_els = self.driver.find_elements(By.NAME, "minute")
        meridian_els = self.driver.find_elements(By.NAME, "meridian")

        for idx, el in enumerate(zip(hour_els, minutes_els, meridian_els)):
            is_start = idx == 0
            hour, minute, meridian = el

            time_input = self.driver.find_element(
                By.ID, self.START_TIME_ID if is_start else self.END_TIME_ID)
            time_input.click()
            time.sleep(0.5)

            hour.click()
            time.sleep(0.5)
            hour.send_keys(10 if is_start else '07')

            minute.click()
            time.sleep(0.5)
            minute.send_keys(30)

            if is_start:
                meridian.click()
                time.sleep(0.5)
                meridian.send_keys('AM')

        print(colored("Setting memo ...", Color.YELLOW))
        memo_input = self.driver.find_element(By.ID, self.MEMO_ID)
        memo_input.click()
        memo_input.send_keys('Working on Scheduler')

        save_btn = self.driver.find_element(By.ID, self.SAVE_BTN_ID)
        save_btn.click()
# except:
        #     print(colored("Could not Update info", Color.RED))


def main():
    CONFIG_PATH = os.environ['HOME'] + '/.config/chromium'
    clocker = Clocker(CONFIG_PATH)
    clocker.load_timesheet()


if __name__ == "__main__":
    main()
