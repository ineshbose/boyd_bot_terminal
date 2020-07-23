import argparse
import keyring
from datetime import datetime
from getpass import getpass
from boyd_bot import timetable


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--today", help="read today's timetable", action="store_true")
parser.add_argument("-n", "--next", help="read next class", action="store_true")
parser.add_argument("-d", "--date", help="read specific day's timetable")
parser.add_argument("-c", "--class_name", help="search for specific class")
parser.add_argument("-l", "--login", help="store credentials", action="store_true")


def no_args():

    print("\nWhat's up?\n1 - Today\n2 - On Specific Day\n3 - Up Next / Now")
    choice = input("Input: ")
    valid_input = {
        "1": lambda: datetime.now(),
        "2": lambda: timetable.dateparse(input("Enter date in DD/MM/YYYY format: ")),
        "3": lambda: None,
    }

    if choice in valid_input:
        timetable.read(valid_input[choice]())
    else:
        print("Invalid input.")


def main():

    sys_args = parser.parse_args()
    args = []

    if sys_args.login:
        uid = input("University ID: ")
        pw = getpass("Password: ")

        with open(".uni_id.txt", "w+") as f:
            f.write(uid)

        keyring.set_password("boyd_bot", uid, pw)

    try:
        with open(".uni_id.txt") as f:
            uid = f.read()
    except FileNotFoundError:
        uid = None

    pw = keyring.get_password("boyd_bot", uid)

    timetable.login(uid, pw)

    if sys_args.today:
        args.append(datetime.now())

    elif sys_args.date:
        args.append(timetable.dateparse(sys_args.date))

    elif sys_args.next:
        args.append(None)

    else:
        return no_args()

    if sys_args.class_name:
        args.append(sys_args.class_name)

    timetable.read(*args)


if __name__ == "__main__":
    main()
