from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime, timedelta
from easygui import *

SERVICE = Service(executable_path="chromeDRIVER.exe")
DRIVER = webdriver.Chrome(service=SERVICE)


def get_present_element(locator, loc_text, w_time=15):
    WebDriverWait(DRIVER, w_time).until(
        expected_conditions.presence_of_element_located((locator, loc_text))
    )
    return DRIVER.find_element(locator, loc_text)


def get_present_elements(locator, loc_text, w_time=15):
    WebDriverWait(DRIVER, w_time).until(
        expected_conditions.presence_of_element_located((locator, loc_text))
    )
    return DRIVER.find_elements(locator, loc_text)


def select_database(database_name):
    databases = get_present_elements(By.CLASS_NAME, "list-group-item")
    for database in databases:
        if database_name in database.text:
            database.click()
            break
    lt = get_present_element(By.XPATH, '//*[@id="report"]/button[2]')
    lt.click()


def select_date_range(y, m, d, h, min, dur_h=1, dur_min=0):
    date = datetime(y, m, d, h, min)
    start = date.strftime("%Y.%m.%d %H:%M")
    end = (date + timedelta(hours=dur_h, minutes=dur_min)).strftime("%Y.%m.%d %H:%M")
    print(f"date range: from {start} to {end}")    # DEBUG
    date_select = get_present_element(By.XPATH, '//*[@id="tx_StartDate"]')
    date_select.clear()
    date_select.send_keys(start + Keys.TAB + end)


def select_line(line_name):
    line_select = get_present_element(By.XPATH, '//*[@id="sl_Cell_chosen"]')
    line_select.click()
    lines = get_present_elements(By.CLASS_NAME, "active-result")
    for line in lines:
        if line_name in line.text:
            line.click()
            break


def select_group(group_name):
    group_select = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]')
    time.sleep(0.1)
    group_select.click()
    time.sleep(0.1)
    groups = get_present_elements(By.CLASS_NAME, 'active-result')

    print("Groups:")
    for group in groups:
        print(group.text)

    group_search = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]/div/div/input')
    group_search.send_keys(group_name + Keys.ENTER)


def select_csv_and_download():
    export_csv = get_present_element(By.XPATH, '//*[@id="inputParams"]/table/tbody/tr[11]/td[2]/label[2]/input')
    export_csv.click()

    start_search = get_present_element(By.XPATH, '//*[@id="bt_Search"]')
    # start_search.click()


DRIVER.get("http://pltyc-nextraceweb/")

select_database("FAAR")

select_date_range(2024, 7, 16, 10, 0, 1, 20)

select_line("Final")

select_group("Final")

select_csv_and_download()

time.sleep(3)
DRIVER.quit()
