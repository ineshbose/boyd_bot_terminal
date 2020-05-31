import os, requests
from icalendar import Calendar
import datetime, pytz, argparse
from getpass import getpass

tmzn = pytz.timezone('Europe/London')           # Used to localize time and compare datetimes
cal_url = "frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"       
                                                # This can be changed to any university's URL
uid = ""                                        # University UID
pw = ""                                         # University Password

cal = Calendar()


def login():
    """Logins in user with the provided credentials.

    A request fetches content from a URL with authentication, and `icalendar.Calendar` creates a calendar from that content.
    If the operation was successful, the user was successfully logged in. If not, `icalendar.Calendar` throws an exception
    since the content was not suitable to create a calendar which means the credentials were unable to fetch content through
    the request; therefore the login was unsuccessful.
    """
    global uid, pw
    if uid == "" and pw == "":
        print("Login credentials not provided.",
        "It's recommended that you add them in the script.")
        uid = input("UID: ")
        pw = getpass("Password: ")
    url = "https://{}:{}@{}".format(uid,pw,cal_url)
    r = requests.get(url)

    try:
        global cal
        cal = Calendar.from_ical(r.content)
        r.close()
    
    except:
        r.close()
        print("Invalid login credentials provided.")
        exit()


def format_event(event):
    """Formats calendar event in a presentable string.

    The events in `icalendar.Calendar` are in the form of a dictionary. This function creates a string containing all
    necessary details about the event in a readable manner (example: `datetime` is not readable) and returns it.

    Note: The formatting is according to how event conventions are for the University of Glasgow. For example, usually events
    are titled something like "OOSE2 (Laboratory) OOSE2 LB01" or "Computing Science - 1S (Lecture) CS1S Lecture.", therefore
    the unnecessary / repetitive words after "(Laboratory)" or "(Lecture)" are removed.

    Parameters
    ----------
    event :
        An event in icalendar.Calendar['vevent'].

    Returns
    -------
    str
        A formatted, readable string for the event.
    """
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' \
        + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n' \
            if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') \
                + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_date(date_entry=None):
    """Fetches events for a specific date.

    Iterates through all events in the calendar and returns events that start and end between the beginning of that
    date (00:00) and end of that date (23:59).

    Parameters
    ----------
    date_entry : str
        Datetime entry as a string
    """
    try:
        class_list = []
        if date_entry != None:
            day, month, year = map(int, date_entry.split('/'))
            date1 = datetime.datetime(year, month, day).replace(tzinfo=tmzn)
        else:
            date1 = datetime.datetime.now(tz=tmzn)
        date2 = date1.replace(hour=23, minute=59, second=59)
        print(date1)
        
        for event in cal.walk('vevent'):
            if event['dtstart'].dt > date1 and event['dtend'].dt < date2:
                print(format_event(event))
                class_list.append(event)
                if date_entry == None: break
        
        if class_list == []:
            print('There seem to be no classes!')
    except:
        print('Date entered in wrong format!')


def no_args():
    """Function for Menu

    If no argument is presented, display the menu for options.
    """
    print("\nWhat's up?\n1 - Today\n2 - On Specific Day\n3 - Up Next / Now")
    choice = input("Input: ")
    if choice == '1':
        read_date(datetime.datetime.now().strftime('%d/%m/%Y'))
    elif choice == '2':
        read_date(input('Enter a date in DD/MM/YYYY format: '))
    elif choice == '3':
        read_date()
    else:
        print("Invalid input.")


if __name__ == "__main__":
    login()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--today', help="read today's timetable", action="store_true")
    parser.add_argument('-d','--date', help="read specific day's timetable\nDate format: DD/YY/MMMM", type=str)
    parser.add_argument('-n','--next', help="read next class", action="store_true")
    args = parser.parse_args()
    if args.today:
        read_date(datetime.datetime.now().strftime('%d/%m/%Y'))
    elif args.date:
        read_date(args.date)
    elif args.next:
        read_date()
    else:
        no_args()