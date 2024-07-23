from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime
from os import listdir, getcwd, replace, rename
from os.path import isfile, join, splitext, getctime
import pandas as pd
import sys

SERVICE = Service(executable_path="chromeDRIVER.exe")
DRIVER = webdriver.Chrome(service=SERVICE)
choices = {}
new_name = None
csv_choices = {}


def gui_and_log():
    if not ('settings_data.ini' in listdir(getcwd())): # NIE istnieje settings_data.in
        sys.exit("settings_data.ini not found, see GUIDE.txt")
    with open('settings_data.ini', "r") as file:
        lines = [line.rstrip().split() for line in file]
    for line in lines:
        choices.update({line[0].rstrip(':'): " ".join(line[1:])})


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

    group_search = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]/div/div/input')
    group_search.send_keys(group_name + Keys.ENTER)


def select_csv_download_move():
    export_csv = get_present_element(By.XPATH, '//*[@id="inputParams"]/table/tbody/tr[11]/td[2]/label[2]/input')
    export_csv.click()

    start_search = get_present_element(By.XPATH, '//*[@id="bt_Search"]')
    start_search.click()

    download_path = choices["dow_path"]
    time.sleep(2)
    only_csvs = [f for f in listdir(download_path) if isfile(join(download_path, f)) and splitext(f)[1] == ".csv"]
    times = [getctime(join(download_path, csv)) for csv in only_csvs]
    latest = only_csvs[times.index(max(times))]
    global new_name
    new_name = f"data_{datetime.now().strftime("%y%m%d%H%M%S")}.csv"
    rename(join(download_path, latest), join(download_path ,new_name))
    replace(join(download_path, new_name), join(getcwd(), new_name))


def trim_csv():
    if "preferred_data.ini" in listdir(getcwd()):
        with open('preferred_data.ini', "r") as file:
            lines = [line.rstrip().split() for line in file]
        for line in lines:
            if line[0] == "serials:":
                line[1:] = [int(s_n) for s_n in line[1:]] if line[1] != '*' else '*'
                csv_choices.update({line[0].rstrip(':'): line[1:]})
            else:
                csv_choices.update({line[0].rstrip(':'): " ".join(line[1:]).split(",")})

    else:  # nie ma pliku
        sys.exit("preferred_data.ini not found, see GUIDE.txt")

    df = pd.read_csv(new_name, sep=';')
    df["Serial"] = [int(x) for x in df["Serial"]]
    if '*' in csv_choices["serials"]:
        new_df = df[csv_choices["params"]].copy()
    else:
        new_df = df.loc[df['Serial'].isin(csv_choices["serials"]), csv_choices["params"]].copy()
    return new_df


if __name__ == "__main__":
    gui_and_log()

    DRIVER.get("http://pltyc-nextraceweb/")

    select_database(choices["baza_d"])

    select_date_range(choices["start"], choices["koniec"])

    select_line(choices["linia"])

    select_group(choices["grupa"])
    select_csv_download_move()

    DRIVER.quit()

    trim_csv().to_csv("trimmed_data.csv", sep=";", index=False)
