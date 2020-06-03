import os, requests
from icalendar import Calendar
import datetime, pytz, argparse
from getpass import getpass
from dateparser import parse

tmzn = pytz.timezone('UTC')
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"       
uid = ""
pw = ""

cal = Calendar()
parser = argparse.ArgumentParser()
parser.add_argument('-t','--today', help="read today's timetable", action="store_true")
parser.add_argument('-n','--next', help="read next class", action="store_true")
parser.add_argument('-d','--date', help="read specific day's timetable")


def login():
    global uid, pw
    if uid == "" and pw == "":
        print("Login credentials not provided.",
        "It's recommended that you add them in the script.")
        uid = input("UID: ")
        pw = getpass("Password: ")
    r = requests.get(cal_url, auth=(uid,pw))

    try:
        global cal
        cal = Calendar.from_ical(r.content)
    
    except:
        print("Invalid login credentials provided.")
        exit()


def format_event(event):
    return "\n{}\nfrom {} to {}\nat {}.\n".format(event['summary'].split(')')[0]+')' 
    if '(' in event['summary'] else event['summary'], event['dtstart'].dt.strftime('%I:%M%p'),
    event['dtend'].dt.strftime('%I:%M%p'), event['location'])


def read_schedule(date_entry=None):
    class_list = []
    date1 = date_entry.replace(hour=0,minute=0,second=0,tzinfo=tmzn) \
        if date_entry != None else datetime.datetime.now(tz=tmzn)
    date2 = date1.replace(hour=23, minute=59, second=59)
    
    for event in cal.walk('vevent'):
        if event['dtstart'].dt > date1 and event['dtend'].dt < date2:
            print(format_event(event))
            class_list.append(event)
            if date_entry == None: break
    
    if class_list == []:
        print('There seem to be no classes!')


def no_args():
    print("\nWhat's up?\n1 - Today\n2 - On Specific Day\n3 - Up Next / Now")
    choice = input("Input: ")
    if choice == '1':
        read_schedule(datetime.datetime.now(tz=tmzn))
    elif choice == '2':
        read_schedule(parse(input("Enter date in DD/MM/YYYY format: ")))
    elif choice == '3':
        read_schedule()
    else:
        print("Invalid input.")


if __name__ == "__main__":
    args = parser.parse_args()
    login()
    if args.today:
        read_schedule(datetime.datetime.now(tz=tmzn))
    elif args.date:
        read_schedule(parse(args.date))
    elif args.next:
        read_schedule()
    else:
        no_args()