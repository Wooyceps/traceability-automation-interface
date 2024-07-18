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
choices = {}


def gui():
    title = "BAZA DANYCH"
    text = "Wprowadź tyski database np. FAAR, BMW, PSA"
    choices.update({"baza danych": enterbox(text, title)})

    title = "PRZEDZIAŁ CZASOWY 1"
    text = "Wprowadź:"
    input_list = ["Rok", "Miesiąc", "Dzień", "Godzina", "Minuta"]
    cur = datetime.now()
    default_list = [cur.year, cur.month, cur.day, cur.hour, cur.minute]
    date_lst = [int(element) for element in multenterbox(text, title, input_list, default_list)]
    start = datetime(date_lst[0], date_lst[1], date_lst[2], date_lst[3], date_lst[4])
    choices.update({
        "start": start.strftime("%Y-%m-%d %H:%M")
    })

    title = "PRZEDZIAŁ CZASOWY 2"
    text = "Wprowadź:"
    input_list = ["Ilośc godzin", "Ilośc minut"]
    default_list = ["1", "0"]
    time_lst = [int(element) for element in multenterbox(text, title, input_list, default_list)]
    choices.update({
        "koniec": (start + timedelta(hours=time_lst[0], minutes=time_lst[1])).strftime("%Y-%m-%d %H:%M")
    })

    title = "LINIA I GRUPA"
    text = "Wprowadź:"
    input_list = ["Linia", "Grupa"]
    l_g = multenterbox(text, title, input_list)
    choices.update({
        "linia": l_g[0],
        "grupa": l_g[1],
    })

    for k, v in choices.items():
        print(f"{k}: {v}")


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


def select_date_range(start, end):
    start_date = get_present_element(By.XPATH, '//*[@id="tx_StartDate"]')
    start_date.send_keys(start + Keys.TAB)
    end_date = get_present_element(By.XPATH, '//*[@id="tx_EndDate"]')
    end_date.send_keys(end + Keys.TAB)


def select_line(line_name):
    line_select = get_present_element(By.XPATH, '//*[@id="sl_Cell_chosen"]')
    time.sleep(0.1)
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

    group_search = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]/div/div/input')
    group_search.send_keys(group_name + Keys.ENTER)


def select_csv_and_download():
    export_csv = get_present_element(By.XPATH, '//*[@id="inputParams"]/table/tbody/tr[11]/td[2]/label[2]/input')
    export_csv.click()

    start_search = get_present_element(By.XPATH, '//*[@id="bt_Search"]')
    start_search.click()


if __name__ == "__main__":
    gui()

    DRIVER.get("http://pltyc-nextraceweb/")

    select_database(choices["baza danych"])

    select_date_range(choices["start"], choices["koniec"])

    select_line(choices["linia"])

    select_group(choices["grupa"])

    select_csv_and_download()

    time.sleep(10)
    DRIVER.quit()
