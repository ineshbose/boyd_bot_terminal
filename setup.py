from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='boyd_bot_terminal',
    version="1.4.1",
    packages=find_packages(),
    install_requires=requirements,

    author='Inesh Bose',
    desription='University Timetable on your Terminal!',
    long_description=long_description,
    license='MIT',
    url='https://github.com/ineshbose/boyd_bot_terminal',

    entry_points={
        "console_scripts": [
            "boyd_bot = boyd_bot.timetable:main",
        ],
    }
)