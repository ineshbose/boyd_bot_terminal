# Boyd Bot (Terminal) [![PyPI](https://img.shields.io/pypi/v/boyd_bot_glasgow?style=flat-square)](https://pypi.org/project/boyd-bot-glasgow/)
This repository is for the terminal (CLI) version of the Boyd Bot. <br />
This is how the bot started out, and is basically a stripped-down version of the [Flask version](https://github.com/ineshbose/boyd_bot_messenger) without needing [Facebook Messenger](https://www.facebook.com/messenger), [Dialogflow](https://dialogflow.com/) and [mongoDB](https://www.mongodb.com/).

## Usage
```
$ pip install boyd_bot_glasgow
$ boyd_bot -h
```

### To-Do
- [x] Use `sysargv` like `--today`
- [ ] Store credentials (**safely**) on user's machine therefore not requiring it again.
- [x] Installation on system to run from any directory