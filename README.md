# Parsing news from websites :newspaper:
Sending updates is done in a pre-defined file in the Telegram channel called **'token.py'**

This project enables you to send updates to a Telegram channel through a user-defined file called **'token.py'**. The **'token.py'** file should include two essential variables: _'channel_id'_ (the channel identifier, including '@') and _'API_KEY'_ (the key required for interacting with the Telegram bot). Furthermore, the project maintains a basic database by storing the last sent news from each website in an automatically generated corresponding _'.txt'_ file.

## Project Files 📂

This project consists of three main files, but the 'token.py' file mentioned earlier needs to be created manually. Here's a brief overview of the files:

1. **main.py**: In 'main.py', you will find all the algorithms necessary for the correct functioning of the project.

2. **web_pages.py**: This file contains the information on how web page parsing is accomplished.

3. **token.py**: You need to create this file manually with the required variables as described above.

## Prerequisites 📚

:pushpin: Make sure you have the following Python modules installed to run this project:

- pyTelegramBotAPI
- bs4
- requests

:pushpin: In addition, the project utilizes built-in Python modules, including:

- time
- os
- logging

## Python Version 🐍

This project is written in Python 3.10
