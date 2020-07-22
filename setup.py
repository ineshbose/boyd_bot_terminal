from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="boyd_bot_glasgow",
    version="1.6.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Inesh Bose",
    description="University Timetable on your Terminal!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ineshbose/boyd_bot_terminal",
    keywords="glasgow university timetable",
    entry_points={"console_scripts": ["boyd_bot = boyd_bot.__main__:main",],},
)
