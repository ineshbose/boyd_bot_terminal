import pytz
import requests
from icalendar import Calendar
from datetime import datetime
from getpass import getpass
from fuzzywuzzy import fuzz


class Timetable:
    def __init__(self, cal_url, tmzn="UTC", fuzz_threshold=36):
        self.cal_url = cal_url
        self.tmzn = pytz.timezone(tmzn)
        self.fuzz_threshold = fuzz_threshold
        self.cal = Calendar()

    def login(self, uid=None, pw=None):
        if not (uid and pw):
            uid = input("University ID: ")
            pw = getpass("Password: ")
        try:
            self.cal = Calendar.from_ical(requests.get(self.cal_url, auth=(uid, pw)).content)
        except ValueError:
            print("Invalid login credentials provided.")
            self.login()
        except Exception as e:
            raise Exception("Something went wrong. {}".format(e.__str__())) from None

    def format_event(self, event):
        return "\n{}\nfrom {} to {}\nat {}.\n".format(
            event["summary"].split(")")[0] + ")"
            if "(" in event["summary"]
            else event["summary"],
            event["dtstart"].dt.strftime("%I:%M%p"),
            event["dtend"].dt.strftime("%I:%M%p"),
            event.get("location", "No Location Found"),
        )

    def read(self, start_date=None, class_name=None):
        class_list = self.iterate(start_date, class_name)
        if not class_list:
            print("There seem to be no classes.")
        else:
            for event in class_list:
                print(self.format_event(event))

    def iterate(self, start_date, class_name):

        class_list = []
        date1 = (
            start_date.replace(hour=0, minute=0, second=0, tzinfo=self.tmzn)
            if start_date
            else datetime.now(tz=self.tmzn)
        )

        date2 = date1.replace(hour=23, minute=59, second=59)

        for event in self.cal.walk("vevent"):
            if event["dtstart"].dt >= date1 and event["dtend"].dt <= date2:

                if not start_date:
                    class_list.append(event)
                    break

                if class_name:
                    if (
                        fuzz.token_set_ratio(
                            class_name.lower(), event["summary"].lower()
                        )
                        > self.fuzz_threshold
                    ):
                        class_list.append(event)

                else:
                    class_list.append(event)

        return class_list

    def dateparse(self, date_entry):
        try:
            day, month, year = map(int, date_entry.split("/"))
            return datetime(year, month, day)
        except ValueError:
            raise Exception("Date entered in invalid format!") from None
