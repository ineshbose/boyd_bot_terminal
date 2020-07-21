import os, requests
from icalendar import Calendar
import datetime, pytz, argparse
from getpass import getpass
from fuzzywuzzy import fuzz

tmzn = pytz.timezone("UTC")
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"
fuzz_threshold = 36
uid = ""
pw = ""

cal = Calendar()
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--today", help="read today's timetable", action="store_true")
parser.add_argument("-n", "--next", help="read next class", action="store_true")
parser.add_argument("-d", "--date", help="read specific day's timetable")
parser.add_argument("-c", "--class_name", help="search for specific class")


def login():
    global uid, pw
    if uid == "" and pw == "":
        uid = input("University ID: ")
        pw = getpass("Password: ")
    try:
        global cal
        cal = Calendar.from_ical(requests.get(cal_url, auth=(uid, pw)).content)
    except ValueError:
        print("Invalid login credentials provided.")
        uid = ""
        pw = ""
        login()
    except Exception as e:
        print("Something went wrong. {}".format(e.__str__()))
        exit()


def format_event(event):
    return "\n{}\nfrom {} to {}\nat {}.\n".format(
        event["summary"].split(")")[0] + ")"
        if "(" in event["summary"]
        else event["summary"],
        event["dtstart"].dt.strftime("%I:%M%p"),
        event["dtend"].dt.strftime("%I:%M%p"),
        event["location"] if "location" in event else "No Location Found",
    )


def read(start_date=None, class_name=None):
    class_list = iterate(start_date, class_name)
    if not class_list:
        print("There seem to be no classes.")
    else:
        for event in class_list:
            print(format_event(event))


def iterate(start_date=None, class_name=None):

    class_list = []

    date1 = (
        start_date.replace(hour=0, minute=0, second=0, tzinfo=tmzn)
        if start_date != None
        else datetime.datetime.now(tz=tmzn)
    )

    date2 = date1.replace(hour=23, minute=59, second=59)

    for event in cal.walk("vevent"):
        if event["dtstart"].dt >= date1 and event["dtend"].dt <= date2:

            if not start_date:
                class_list.append(event)
                break

            if class_name:
                if (
                    fuzz.token_set_ratio(class_name.lower(), event["summary"].lower())
                    > fuzz_threshold
                ):
                    class_list.append(event)

            else:
                class_list.append(event)

    return class_list


def dateparse(date_entry):
    try:
        day, month, year = map(int, date_entry.split("/"))
        return datetime.datetime(year, month, day)
    except ValueError:
        print("Date entered in invalid format!")
        exit()


def no_args():
    print("\nWhat's up?\n1 - Today\n2 - On Specific Day\n3 - Up Next / Now")
    choice = input("Input: ")
    if choice == "1":
        read(datetime.datetime.now(tz=tmzn))
    elif choice == "2":
        read(dateparse(input("Enter date in DD/MM/YYYY format: ")))
    elif choice == "3":
        read()
    else:
        print("Invalid input.")


def main():

    sys_args = parser.parse_args()
    args = []
    login()

    if sys_args.today:
        args.append(datetime.datetime.now(tz=tmzn))
    elif sys_args.date:
        args.append(dateparse(sys_args.date))
    elif sys_args.next:
        args.append(None)
    else:
        return no_args()

    if sys_args.class_name:
        args.append(sys_args.class_name)

    read(*args)


if __name__ == "__main__":
    main()
