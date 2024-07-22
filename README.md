# Traceability automation interface

### About the project

This project covers an automation and logging tool that allows user to search desired data easier and reformat the data to ones needs without the need to re-type all of settings each time.

Instead, it streams data form two .ini files, that contain all necessary choices user must make in order to acquire well tailored .csv file with needed information only.

### Prerequisites

In order for the `main.py` script to work certain requirements must be met:

- User must have python 3.12 version installed on his machine.
- Libraries from `requirements.txt` must be installed. This can be done easily by running `pip install -r requirements.txt` in terminal.
- There must be `chromedriver.exe` file in project directory. You can install one here: [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/#stable)
- Lastly, there must be two **.ini** files in the project directory:
  - `settings_data.ini` specifying pre-csv-download settings
  - `preferred_data.ini` specifying serial numbers and parameters for downsizing the **.csv** file.

Instructions and examples on how to fill **.ini** files are covered in `GUIDE.txt` file.

### License

Project is under [MIT License](LICENSE)