from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from easygui import *

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


def get_present_element(locator, loc_text, w_time=15):
    WebDriverWait(driver, w_time).until(
        expected_conditions.presence_of_element_located((locator, loc_text))
    )
    return driver.find_element(locator, loc_text)


def get_present_elements(locator, loc_text, w_time=15):
    WebDriverWait(driver, w_time).until(
        expected_conditions.presence_of_element_located((locator, loc_text))
    )
    return driver.find_elements(locator, loc_text)


def date_range(y, m, d, h, min, dur_min=60):  # Argumenty wysyłane jako stringi
    dur_min = int(dur_min)
    return (y + "." + m + "." + d + " " + h + ":" + m,
            y + "." + m + "." + d + " " + str(dur_min // 60) + ":" + str(
                dur_min % 60))  # przedział czasowy w formacie: YYYY-MM-DD HH:MM


def select_database():
    pass

driver.get("http://pltyc-nextraceweb/")

databases = get_present_elements(By.CLASS_NAME, "list-group-item")
for database in databases:
    if "FAAR" in database.text:
        database.click()
        break

lt = get_present_element(By.XPATH, '//*[@id="report"]/button[2]')
lt.click()

date_range = date_range("2024", "07", "16", "10", "00", 180)

date_select = get_present_element(By.XPATH, '//*[@id="tx_StartDate"]')
date_select.clear()
date_select.send_keys(date_range[0] + Keys.TAB + date_range[1])

line_select = get_present_element(By.XPATH, '//*[@id="sl_Cell_chosen"]')
line_select.click()

lines = get_present_elements(By.CLASS_NAME, "active-result")
for line in lines:
    if "Final" in line.text:
        line.click()
        break

group_select = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]')
time.sleep(0.1)
group_select.click()
time.sleep(0.1)

groups = get_present_elements(By.CLASS_NAME, 'active-result')
for group in groups:
    print(group.text)

group_search = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]/div/div/input')
group_search.send_keys("Final" + Keys.ENTER)

export_csv = get_present_element(By.XPATH, '//*[@id="inputParams"]/table/tbody/tr[11]/td[2]/label[2]/input')
export_csv.click()

start_search = get_present_element(By.XPATH, '//*[@id="bt_Search"]')
start_search.click()

time.sleep(10)
driver.quit()
