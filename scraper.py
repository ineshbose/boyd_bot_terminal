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
    
    try:
        WebDriverWait(browser, 1).until(element_present)
        classes = browser.find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
        print("\nYou have..")
        
        for clas in classes:
            try:
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browser, 1).until(element_present)
                table = browser.find_element_by_class_name("dialogueTable")
                class_data = []
               
                for i in range(1,8):
                    class_data.append(browser.find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text) 
               
                print((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                browser.find_element_by_class_name("close.text-white").click()
            
            except exceptions.ElementNotInteractableException:
                browser.implicitly_wait(3)
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browser, 1).until(element_present)
                table = browser.find_element_by_class_name("dialogueTable")
                class_data = []
               
                for i in range(1,8):
                    class_data.append(browser.find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text) 
               
                print((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                browser.find_element_by_class_name("close.text-white").click()
            
            except:
                print("(Unable to fetch class)\n")
                continue
    
    except exceptions.TimeoutException:
        print("There seem to be no classes.")


def read_now():
    element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "fc-time-grid-event.fc-event.fc-start.fc-end"))
    
    try:
        WebDriverWait(browser, 1).until(element_present)
        classes = browser.find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
        print("\nUp next, you have..")
       
        for clas in classes:
            try:
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browser, 1).until(element_present)
                table = browser.find_element_by_class_name("dialogueTable")
                class_data = []
    
                for i in range(1,8):
                    class_data.append(browser.find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text) 
                
                tyme = str(datetime.datetime.now().date()) + " {}".format(class_data[4])
                classtime = datetime.datetime.strptime(tyme, '%Y-%m-%d %I:%M %p')
    
                if(datetime.datetime.now() <= classtime):
                    print((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                    break
                browser.find_element_by_class_name("close.text-white").click()
    
            except exceptions.ElementNotInteractableException:
                browser.implicitly_wait(3)
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browser, 1).until(element_present)
                table = browser.find_element_by_class_name("dialogueTable")
                class_data = []
    
                for i in range(1,8):
                    class_data.append(browser.find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text) 
                
                tyme = str(datetime.datetime.now().date()) + " {}".format(class_data[4])
                classtime = datetime.datetime.strptime(tyme, '%Y-%m-%d %I:%M %p')
    
                if(datetime.datetime.now() <= classtime):
                    print((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                    break
                browser.find_element_by_class_name("close.text-white").click()
            
            except:
                print("(Unable to fetch class)\n")
                continue
    
    except exceptions.TimeoutException:
        print("There seem to be no classes.")


def specific_day():
    date_entry = input('Enter a date in DD/MM/YYYY format: ')
    day, month, year = map(int, date_entry.split('/'))
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
        print("\nWhat's up?\n1 - Today\n2 - This Week\n3 - X days later\n4 - On Specific Day\n5 - Up Next / Now")
        choice = int(input("Input: "))
        if choice == 1:
            read_today()
        elif choice == 2:
            read_week()
        elif choice == 3:
            loop_days(int(input("How many days? ")))
        elif choice == 4:
            specific_day()
        elif choice == 5:
            read_now()
        else:
            print("Invalid input.")
        quit=input("Quit? [Y/N]: ")

    print("\nClosing browser..\n")
    browser.quit()


main()