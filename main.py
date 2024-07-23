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
from easygui import msgbox

SERVICE = Service(executable_path="chromeDRIVER.exe")
DRIVER = webdriver.Chrome(service=SERVICE)
choices = {}
new_name = None
csv_choices = {}


def gui_and_log():
    try:
        with open('settings_data.ini', "r") as file:
            lines = [line.rstrip().split() for line in file]
        for line in lines:
            choices.update({line[0].rstrip(':'): " ".join(line[1:])})
    except:
        msgbox("Invalid/nonexistent settings_data.ini", "Error", "OK")
        sys.exit("settings_data.ini not found, see GUIDE.txt")


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
    try:
        databases = get_present_elements(By.CLASS_NAME, "list-group-item")
        for database in databases:
            if database_name in database.text:
                database.click()
                break
        lt = get_present_element(By.XPATH, '//*[@id="report"]/button[2]')
        lt.click()
    except:
        msgbox("Invalid database", "Error", "OK")
        sys.exit("invalid database, see GUIDE.txt")


def select_date_range(start, end):
    try:
        start_date = get_present_element(By.XPATH, '//*[@id="tx_StartDate"]')
        start_date.send_keys(start + Keys.TAB)
        end_date = get_present_element(By.XPATH, '//*[@id="tx_EndDate"]')
        end_date.send_keys(end + Keys.TAB)
    except:
        msgbox("Invalid date range", "Error", "OK")
        sys.exit("invalid date range, see GUIDE.txt")


def select_line(line_name):
    try:
        line_select = get_present_element(By.XPATH, '//*[@id="sl_Cell_chosen"]')
        time.sleep(0.1)
        line_select.click()
        lines = get_present_elements(By.CLASS_NAME, "active-result")
        for line in lines:
            if line_name in line.text:
                line.click()
                break
    except:
        msgbox("Invalid line", "Error", "OK")
        sys.exit("invalid line, see GUIDE.txt")


def select_group(group_name):
    try:
        group_select = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]')
        time.sleep(0.1)
        group_select.click()
        time.sleep(0.1)

        group_search = get_present_element(By.XPATH, '//*[@id="sl_Group_chosen"]/div/div/input')
        group_search.send_keys(group_name + Keys.ENTER)
    except:
        msgbox("Invalid group", "Error", "OK")
        sys.exit("invalid group, see GUIDE.txt")


def select_csv_download_move():
    try:
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
    except:
        msgbox("Unable to download, check dow_path in settings_data.ini", "Error", "OK")
        sys.exit("unable to download, see GUIDE.txt")


def trim_csv():
    try:
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
        new_df.to_csv(join(choices["targ_path"], "trimmed_data.csv"), sep=";", index=False)
    except IndexError:
        msgbox(f"Check preferred_data.ini for useless spaces/enters {new_name}", "Error", "OK")
        sys.exit(f"preferred_data.ini issue {new_name}, see GUIDE.txt")
    except:
        msgbox(f"Unable to reformat {new_name}", "Error", "OK")
        sys.exit(f"unable to reformat {new_name}, see GUIDE.txt")


def format_csv_for_minitab():
    df = pd.read_csv(join(choices["targ_path"], "trimmed_data.csv"), sep=";", index_col=False)
    for serial in csv_choices["serials"]:
        df.replace(to_replace=str(serial), value=("'" + str(serial)), inplace=True)
    dims = df.shape
    for row in range(dims[0]):
        for col in range(dims[1]):
            df.iloc[row, col] = str(df.iloc[row, col]).replace('.', ',')
    for ts in df["Timestamp"]:
        df.replace(to_replace=ts, value=datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f").strftime("%d.%m.%Y %H:%M:%S"),
                   inplace=True)
    df.to_csv(join(choices["targ_path"], "trimmed_data.csv"), sep=';', index=False)


if __name__ == "__main__":
    gui_and_log()

    DRIVER.get("http://pltyc-nextraceweb/")

    select_database(choices["baza_d"])

    select_date_range(choices["start"], choices["koniec"])

    select_line(choices["linia"])

    select_group(choices["grupa"])

    select_csv_download_move()

    DRIVER.quit()

    trim_csv()

    format_csv_for_minitab()

    msgbox(f"File acquired, trimmed and refactored for minitab.", "Success", "OK")