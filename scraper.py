import os, requests
from icalendar import Calendar, Event
import time, datetime, pytz
from getpass import getpass

cal = Calendar()
tmzn = pytz.UTC

def login():
    guid = input("GUID: ")
    passw = getpass()
    url = "https://{}:{}@frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics".format(guid,passw)
    r = requests.get(url)
    print("\nLogging in..\n")
    
    try:
        global cal
        cal = Calendar.from_ical(r.content)
        r.close()
        print("\nLogin successful!\n")
    
    except:
        r.close()
        print("\nInvalid Credentials. Try again.\n")
        login()


def format_event(event):
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n' if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_now():
    date1 = datetime.datetime.now()
    date2 = date1 + datetime.timedelta(days=1)
    for event in cal.walk('vevent'):
        if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
            print(format_event(event))
            break


def read_date(date_entry=datetime.datetime.now().strftime('%d/%m/%Y')):
    try:
        day, month, year = map(int, date_entry.split('/'))
        date1 = datetime.datetime(year, month, day)
        date2 = date1 + datetime.timedelta(days=1)
        for event in cal.walk('vevent'):
            if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
                print(format_event(event))
    except:
        print('Wrong format!')


if __name__ == "__main__": 
    login()
    quit="n"
    while quit.upper()!="Y":
        print("\nWhat's up?\n1 - Today\n2 - On Specific Day\n3 - Up Next / Now")
        choice = input("Input: ")
        if choice == '1':
            read_date()
        elif choice == '2':
            read_date(input('Enter a date in DD/MM/YYYY format: '))
        elif choice == '3':
            read_now()
        else:
            print("Invalid input.")
        quit=input("Quit? [Y/N]: ")