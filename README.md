# Boyd Bot (Terminal)
This repository is for terminal version of the Boyd Bot.

## Set-Up
### Packages
[icalendar](https://github.com/SeleniumHQ/selenium) is the only package needed for this bot.
```
$ pip install icalendar
```
Rest of the packages are built-in.

### ChromeDriver
`chromedriver.exe` is added in the repository, however this will work for Windows. For macOS/Linux, it can be downloaded from [here](https://chromedriver.chromium.org/downloads). Replace the `chromedriver.exe` with the new one.

### Path (Optional, Recommended)
Linux users can enjoy using the script from any directory; they just need to add it to the PATH.

### To-Do
1. Store credentials on user's machine therefore not requiring it again.
2. Use `sysargv` like `--today`