import os
from selenium import webdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, datetime
from getpass import getpass

URL = "https://www.gla.ac.uk/apps/timetable/#/login"
chromedriver = path = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'
weekdayMapping = {"MONDAY":0, "TUESDAY":1, "WEDNESDAY":2, "THURSDAY":3, "FRIDAY":4}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
browser = webdriver.Chrome(chromedriver, options=options)

def login():
    browser.get(URL)
    browser.find_element_by_id("guid").send_keys(input("GUID: "))
    browser.find_element_by_id("password").send_keys(getpass())
    print("\nLogging in..\n")
    browser.find_element_by_xpath("//*[@id='app']/div/main/button").click()
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div[1]/a"))
        WebDriverWait(browser, 4).until(element_present)
        browser.find_element_by_xpath("//*[@id='app']/div/div[1]/div[1]/a").click()
        if browser.current_url == "https://www.gla.ac.uk/apps/timetable/#/timetable":
            print("\nLogin successful!\n")
    except exceptions.UnexpectedAlertPresentException as e:
        print("\nInvalid credentials! Try again.\n")
        browser.refresh()
        login()
    except exceptions.NoSuchElementException as load:
        print("\nSomething went wrong. Maybe the connection was too slow. Try again.\n")
        browser.refresh()
        login()

def read_today():
    element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "fc-time-grid-event.fc-event.fc-start.fc-end"))
    WebDriverWait(browser, 1).until(element_present)
    classes = browser.find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
    if classes == []:
        print("Either there are no classes, or something went wrong.")
    else:
        print("\nYou have..")
        for clas in classes:
            try:
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browser, 1).until(element_present)
                table = browser.find_element_by_class_name("dialogueTable")
                print(table.text, "\n")
                browser.find_element_by_class_name("close.text-white").click()
            except exceptions.ElementNotInteractableException as e:
                print("(Unable to fetch class)\n")
                continue

def specific_day():
    date_entry = input('Enter a date in DD-MM-YYYY format: ')
    day, month, year = map(int, date_entry.split('-'))
    date1 = datetime.date(year, month, day)
    loop_days((date1 - datetime.date.today()).days)

def loop_days(n):
    for i in range(n):
        browser.find_element_by_class_name("fc-next-button.fc-button.fc-button-primary").click()
    read_today()
    browser.find_element_by_class_name("fc-today-button.fc-button.fc-button-primary").click()

def read_week():
    element_present = EC.visibility_of_element_located((By.CLASS_NAME, "fc-listWeek-button.fc-button.fc-button-primary"))
    WebDriverWait(browser, 1).until(element_present)
    browser.find_element_by_class_name("fc-listWeek-button.fc-button.fc-button-primary").click()
    element_present = EC.visibility_of_element_located((By.CLASS_NAME, "fc-list-table"))
    WebDriverWait(browser, 1).until(element_present)
    week = browser.find_element_by_class_name("fc-list-table")
    data = week.text
    days = []
    days.append(data.split("Tuesday")[0])
    days.append(data.split("Tuesday")[1].split("Wednesday")[0])
    days.append(data.split("Wednesday")[1].split("Thursday")[0])
    days.append(data.split("Thursday")[1].split("Friday")[0])
    days.append(data.split("Friday")[1])
    print(days[weekdayMapping[input("\nWhat day this week? ").upper()]])
    browser.find_element_by_class_name("fc-timeGridDay-button.fc-button.fc-button-primary").click()

def main():
    print("\nHello! Give me a minute to initialize..\n")
    login()
    quit="n"
    while quit.upper()!="Y":
        print("\nWhat's up?\n1 - Today\n2 - This Week\n3 - X days later\n4 - On Specific Day")
        choice = int(input("Input: "))
        if choice == 1:
            read_today()
        elif choice == 2:
            read_week()
        elif choice == 3:
            loop_days(int(input("How many days? ")))
        elif choice == 4:
            specific_day()
        else:
            print("Invalid input.")
        quit=input("Quit? [Y/N]: ")

    print("\nClosing browser..\n")
    browser.quit()

main()