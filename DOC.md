# Boyd Bot (Terminal)

```python
# Used to localize time and compare datetimes
tmzn = pytz.timezone('UTC')

# This can be changed to any university's URL
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"       

# University UID
uid = ""

# University Password
pw = ""
```


## `login()`
```python
def login():
    """Logins in user with the provided credentials.

    A request fetches content from a URL with authentication, and `icalendar.Calendar` creates a calendar from that content.
    If the operation was successful, the user was successfully logged in. If not, `icalendar.Calendar` throws an exception
    since the content was not suitable to create a calendar which means the credentials were unable to fetch content through
    the request; therefore the login was unsuccessful.
    """
    try:
        # login
    
    except:
        # login failed
```


## `format_event()`
```python
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
    return "{}\nfrom {} to {}\nat {}.\n\n".format(event['summary'].split(')')[0]+')' 
    if '(' in event['summary'] else event['summary'], event['dtstart'].dt.strftime('%I:%M%p'),
    event['dtend'].dt.strftime('%I:%M%p'), event['location'])
```


## `read_schedule()`
```python
def read_schedule(date_entry=None):
    """Fetches events for a specific date.

    Iterates through all events in the calendar and returns events that start and end between the beginning of that
    date (00:00) and end of that date (23:59).

    Parameters
    ----------
    date_entry : datetime
        Datetime entry
    """
    class_list = []
    # read timetable
```

## `no_args()` (deprecated)
```python
def no_args():
    """Function for Menu

    If no argument is presented, display the menu for options.
    """
    # present menu and take input
    # if input = 1: do something
    # else: invalid input
```