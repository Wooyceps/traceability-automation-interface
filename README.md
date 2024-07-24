# Traceability automation interface

### About the project

This project covers an automation and logging tool that allows user to search desired data easier and reformat the data to ones needs without the need to re-type all of settings each time.

Instead, it streams data form two .ini files, that contain all necessary choices user must make in order to acquire well tailored .csv file with needed information only.

### Prerequisites

In order for the `main.py` script to work certain requirements must be met:

- User must have python 3.12 version installed on his machine. you can download it [here](https://www.python.org/downloads/).
- Libraries from `requirements.txt` must be installed. This can be done easily by running `pip install -r requirements.txt` in project's directory terminal.
- There must be `chromedriver.exe` file in project directory. You can install latest one [here](https://googlechromelabs.github.io/chrome-for-testing/#stable) - look for your OS wersion of ***chromedriver***.
- Lastly, the two **.ini** files in the project directory must by filled as presented in ***GUIDE.txt***:
  - `settings_data.ini` specifying pre-csv-download settings
  - `preferred_data.ini` specifying serial numbers and parameters for downsizing the **.csv** file.

### Guidance

Main (if not only) reason app is not working properly, thus throws easygui "msgboxes" at you, is that you filled **.ini** files incorrectly.

**Pay great attention to spaces, commmas and carriage returns *("enters").***

All information on how to properly fill the preferences is contained in [.ini filling guide text file](GUIDE.txt)

### License

Project is under [MIT License](LICENSE)

### Issues

Feel free to post issues on Github or contact me via media posted below.

### Contact

- [mwooycik@gmail.com](mailto:mwooycik@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/micha%C5%82-w%C3%B3jcik-562213266/)
