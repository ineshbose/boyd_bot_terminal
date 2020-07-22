# Boyd Bot (Terminal) [![PyPI](https://img.shields.io/pypi/v/boyd_bot_glasgow?style=flat-square)](https://pypi.org/project/boyd-bot-glasgow/)

This repository is for the terminal (CLI) version of the Boyd Bot. <br />
This is how the bot started out, and is basically a stripped-down version of the [Flask version](https://github.com/ineshbose/boyd_bot_messenger) without needing any external services.


## Usage

You can install this as a package from [PyPI](https://pypi.org/) and use the special command `boyd_bot`.

```sh
$ pip install boyd_bot_glasgow
$ boyd_bot -h
```

You can also clone this repository and install it or run the script.

```sh
$ git clone https://github.com/ineshbose/boyd_bot_terminal
$ cd boyd_bot_terminal
$ python setup.py install   # if you want to install
$ python boyd_bot           # if you want to run script
```


## Changing for your University

Does your university offer a(n) `.ics` file for students? Make changes in `timetable.py` to link the URL and also distribute it as a package by renaming it to `boyd_bot_XXXXX` where `XXXXX` can be your university name.


## Note

I understand that sometimes the code is not comprehensible and this might be due to added features or converting this into a package. Therefore, it would be great to go through the [commit history](https://github.com/ineshbose/boyd_bot_terminal/commits) and understand the program. I feel this [tree](https://github.com/ineshbose/boyd_bot_terminal/tree/7f95043688837209f43cdf4ffc6ae5544a2ec512) will be easier to understand. Good luck! 😄