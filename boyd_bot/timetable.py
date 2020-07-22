import requests
from icalendar import Calendar
import datetime, pytz
from getpass import getpass
from fuzzywuzzy import fuzz

tmzn = pytz.timezone("UTC")
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"
fuzz_threshold = 36
cal = Calendar()


def login(uid=None, pw=None):
    if not (uid and pw):
        uid = input("University ID: ")
        pw = getpass("Password: ")
    try:
        global cal
        cal = Calendar.from_ical(requests.get(cal_url, auth=(uid, pw)).content)
    except ValueError:
        print("Invalid login credentials provided.")
        login()
    except Exception as e:
        raise Exception("Something went wrong. {}".format(e.__str__())) from None


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
        raise Exception("Date entered in invalid format!") from None