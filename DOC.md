# Boyd Bot (Terminal)

```python
# This can be changed to any university's URL
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics" 

# Used to localize time and compare datetimes
tmzn = pytz.timezone('UTC')

# A threshold for string-matching
fuzz_threshold = 40

# Instance of icalendar.Calendar
cal = Calendar()
```


## `login(uid="", pw="")`

Logins in user with the provided credentials. <br>
A request fetches content from a URL with authentication, and `icalendar.Calendar` creates a calendar from that content. If the operation was successful, the user was successfully logged in. If not, `icalendar.Calendar` throws an exception since the content was not suitable to create a calendar which means the credentials were unable to fetch content through the request; therefore the login was unsuccessful.

|                         Parameters                        |   Returns  |
|-----------------------------------------------------------|------------|
| **`uid`:** the portal ID<br>**`pw`:** the portal password | **`None`** |



## `format_event(event)`

Formats calendar event in a presentable string. <br>
The events in `icalendar.Calendar` are in the form of a dictionary. This function creates a string containing all necessary details about the event in a readable manner (example: `datetime` is not readable) and returns it. <br>
**Note:** The formatting is according to how event conventions are for the University of Glasgow. For example, usually events are titled something like "OOSE2 (Laboratory) OOSE2 LB01" or "Computing Science - 1S (Lecture) CS1S Lecture.", therefore the unnecessary / repetitive words after "(Laboratory)" or "(Lecture)" are removed.


|                       Parameters                      |                    Returns                      |
|-------------------------------------------------------|-------------------------------------------------|
| **`event`:** the `icalendar.Calendar.event` to format | **`str`:** a string representation of the event |



## `read(start_date=None, class_name=None)`

Main function to be called from `timetable` and returns a message accordingly.

|                                                  Parameters                                                 |          Returns           |
|-------------------------------------------------------------------------------------------------------------|----------------------------|
| **`start_date`:** `date-time` start parameter if found<br>**`class_name`:** `class-name` parameter if found | **`list`:** list of events |



## `iterate(start_date, class_name)`

Iterates through all events in the calendar and returns events that start and end between the beginning of that date (00:00) and end of that date (23:59).

|                                         Parameters                                        |          Returns           |
|-------------------------------------------------------------------------------------------|----------------------------|
| **`start_date`:** `date-time` start parameter<br>**`class_name`:** `class-name` parameter | **`list`:** list of events |



## `dateparse(date_entry)`

Converts a string into `datetime` else raises error.

|             Parameters             |                   Returns                    |
|------------------------------------|----------------------------------------------|
| **`date_entry`:** `str` to convert | **`datetime`:** string converted to datetime |